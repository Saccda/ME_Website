import csv, hashlib, io, os, random, uuid
from contextlib import asynccontextmanager
from datetime import timedelta
from typing import Literal
from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict, field_validator
from sqlalchemy import select, func, update, delete
from sqlalchemy.exc import IntegrityError
from .catalog import DOMAINS, LOGIC_DOMAINS, LEVELS, LEVEL_GUIDE, SOURCE, SOURCES, SUBJECTS, SUBJECT_OF, DOMAIN_BY_ID, GENERATED_SUBJECTS
from .models import Base, engine, SessionLocal, User, AuthSession, LoginFailure, Question, Audit, Blueprint, Attempt, now, POOL_TOTAL
from .security import db_session, current_user, teacher, hash_password, verify, new_session, utc, auth_mode
from .generator import generate
from .validation import validate

def uid(): return str(uuid.uuid4())

def audit(db,user,entity,action,detail):
    db.add(Audit(id=uid(),user_id=user.id,entity_id=entity,action=action,detail=detail))

def make_question(domain, difficulty, option_count=4, seed=None, presentation="text", skill=None):
    content=generate(domain,difficulty,option_count,seed,presentation,skill)
    subject=SUBJECT_OF[domain]
    source={**SOURCES[subject],"sets":DOMAIN_BY_ID[domain]["sets"],"template":"original-v1","generation_seed":seed}
    return Question(id=uid(),subject=subject,domain=domain,skill=content.pop("skill"),difficulty=difficulty,status="draft",content=content,source=source,validation=validate(content),version=1)

def initialize():
    if os.getenv('DB_AUTO_CREATE','true').lower()=='true': Base.metadata.create_all(engine)
    with SessionLocal() as db:
        demo=os.getenv("DEMO_MODE", "false").lower()=="true"
        # Stripped, because these come from an env file where a stray space
        # after "=" is easy to leave behind. Sign-in strips the address it looks
        # up, so an account created with one could never be signed in to.
        email=(os.getenv("TEACHER_EMAIL", "teacher@demo.local" if demo else "") or "").strip()
        password=(os.getenv("TEACHER_PASSWORD", "teacher-demo-2026" if demo else "") or "").strip()
        if auth_mode()=='open' and not db.scalar(select(User).where(User.role=='teacher')) and not (email and password):
            db.add(User(id=uid(),email='system@workspace.invalid',name='Teacher workspace',password=hash_password(uuid.uuid4().hex),role='teacher'));db.commit()
        if auth_mode()!='open' and not demo and not db.scalar(select(User).where(User.role=='teacher')) and (not email or not password):
            raise RuntimeError('Set TEACHER_EMAIL and TEACHER_PASSWORD for the initial teacher account, or explicitly enable DEMO_MODE for local evaluation.')
        if email and password and not db.scalar(select(User).where(User.email==email.lower())):
            if len(password)<12: raise RuntimeError("Teacher password must have at least 12 characters")
            db.add(User(id=uid(),email=email.lower(),name="Teacher",password=hash_password(password),role="teacher"))
        if auth_mode()!='open':
            # A no-login workspace cookie lasts 30 days and may carry the teacher
            # role, so it would survive the switch to sign-in and keep answer-key
            # access. Close those sessions; the guest rows and their attempts stay.
            guests=[row for row in db.scalars(select(User.id).where(User.email.like('%@guest.invalid')))]
            if guests:
                db.execute(delete(AuthSession).where(AuthSession.user_id.in_(guests)))
                db.commit()
        if demo and not db.scalar(select(User).where(User.email=="student@demo.local")):
            db.add(User(id=uid(),email="student@demo.local",name="Student",password=hash_password("student-demo-2026"),role="student"))
        db.commit()
        # Seeded one subject at a time, so a subject added after a database was
        # first filled is seeded on the next start without touching what is there.
        teacher_user=db.scalar(select(User).where(User.role=="teacher"))
        seeded={(q.content["stem"],len(q.content["options"])) for q in db.scalars(select(Question))}
        added=False
        for si,subject in enumerate(GENERATED_SUBJECTS):
            if db.scalar(select(func.count()).select_from(Question).where(Question.subject==subject)): continue
            for di,d in enumerate([x for x in DOMAINS if x["subject"]==subject]):
                for li,l in enumerate(LEVELS):
                    for n in range(3):
                        for retry in range(40):
                            q=make_question(d["id"],l,4 if n!=2 else 5,si*500000+10000+di*1000+li*100+n+retry*17000,"diagram" if d["id"]=="deduction" else "text")
                            signature=(q.content['stem'],len(q.content['options']))
                            if signature not in seeded: break
                        else: continue
                        seeded.add(signature)
                        # Sample bank is opt-in for demo. Real installations require local teacher review.
                        if demo and q.validation["passed"]:
                            q.status="approved"
                        db.add(q)
                        added=True
                        if teacher_user: audit(db,teacher_user,q.id,"demo_seed_approved" if demo else "seed_draft",{"version":1,"note":"Original starter content. Demo approval only; real deployment seeds remain drafts."})
        if added:
            if demo and teacher_user and not db.scalar(select(func.count()).select_from(Blueprint)):
                db.add(Blueprint(id=uid(),name="Logic readiness · 14 questions",minutes=25,rows=[{"domain":d["id"],"difficulty":"Practice","count":2,"options":4} for d in LOGIC_DOMAINS],published=True,creator_id=teacher_user.id))
            db.commit()

@asynccontextmanager
async def lifespan(app):
    # Endpoints are synchronous, so each runs on a worker thread and holds one
    # database connection for its whole life. With more threads than connections
    # a request takes a thread, waits for a connection it cannot get, and fails.
    # Matching the two makes a busy server queue rather than return errors.
    from anyio import to_thread
    to_thread.current_default_thread_limiter().total_tokens = POOL_TOTAL
    initialize()
    yield

app=FastAPI(title="Mechanical Engineering @ RUPP · Entrance Prep",version="1.0.0",lifespan=lifespan)

@app.middleware("http")
async def guards(request, call_next):
    if request.method in ("POST","PATCH","PUT","DELETE"):
        origin=request.headers.get("origin")
        allowed=os.getenv("APP_ORIGINS","http://localhost:3000,http://127.0.0.1:3000").split(",")
        if request.headers.get("x-app-request")!="1" or (origin and origin not in allowed):
            return JSONResponse(status_code=403,content={"detail":"Request origin could not be verified."})
        if int(request.headers.get("content-length","0"))>3500000:
            return JSONResponse(status_code=413,content={"detail":"Request exceeds upload limit."})
    response=await call_next(request)
    response.headers["Cache-Control"]="no-store"
    response.headers["X-Content-Type-Options"]="nosniff"
    response.headers["Referrer-Policy"]="same-origin"
    return response

class StrictModel(BaseModel):
    model_config=ConfigDict(extra="forbid")

class Credentials(StrictModel):
    email: str = Field(min_length=3,max_length=254)
    password: str = Field(min_length=1,max_length=256)

class Registration(Credentials):
    name: str = Field(min_length=1,max_length=100)

def user_public(u): return {"id":u.id,"name":u.name,"email":u.email,"role":u.role}

@app.get("/api/health")
def health(): return {"ok":True,"demo":os.getenv("DEMO_MODE","false").lower()=="true","auth_mode":auth_mode()}

class WorkspaceBody(StrictModel):
    role: Literal['student','teacher'] | None = None

@app.post('/api/workspace')
def workspace(body:WorkspaceBody,request:Request,response:Response,db=Depends(db_session)):
    """No-credentials browser identity; replace this boundary with trusted ME-site identity later.
    Open-mode role selection is a workspace choice, not an authorization boundary.
    """
    if auth_mode()!='open': raise HTTPException(403,'The official website must provide an authenticated session for this installation.')
    token=request.cookies.get('logic_session','')
    session=db.get(AuthSession,hashlib.sha256(token.encode()).hexdigest())
    previous=db.get(User,session.user_id) if session and utc(session.expires)>now() else None
    guest=previous if previous and previous.email.endswith('@guest.invalid') else None
    visitor=guest.email.split('@')[0].rsplit('-',1)[0] if guest else uid()
    role=body.role or (guest.role if guest else 'student')
    email=f'{visitor}-{role}@guest.invalid'
    u=db.scalar(select(User).where(User.email==email))
    if not u:
        u=User(id=uid(),email=email,name='Learner' if role=='student' else 'Teacher workspace',password=hash_password(uuid.uuid4().hex),role=role)
        db.add(u);db.commit()
    if guest:
        session.user_id=u.id;session.expires=now()+timedelta(days=30);db.commit()
        response.set_cookie('logic_session',token,httponly=True,samesite='strict',secure=os.getenv('COOKIE_SECURE','false').lower()=='true',max_age=2592000,path='/')
    else: new_session(db,u,response,max_age=2592000)
    return user_public(u)

@app.get("/api/catalog")
def catalog(): return {"subjects":[{k:v for k,v in s.items() if k!="source"} for s in SUBJECTS],"domains":[{k:v for k,v in d.items() if k!="sets"} for d in DOMAINS],"levels":LEVELS,"level_guide":LEVEL_GUIDE}

@app.post("/api/auth/login")
def login(body:Credentials,request:Request,response:Response,db=Depends(db_session)):
    if auth_mode()=='open': raise HTTPException(404,'Sign-in is disabled. Open a workspace instead.')
    key=hashlib.sha256(body.email.lower().encode()).hexdigest()
    failures=db.scalar(select(func.count()).select_from(LoginFailure).where(LoginFailure.key==key,LoginFailure.created>now()-timedelta(minutes=15)))
    if failures>=10: raise HTTPException(429,"Too many attempts. Try again in 15 minutes.")
    u=db.scalar(select(User).where(User.email==body.email.lower().strip()))
    if not u or not verify(body.password,u.password):
        db.add(LoginFailure(id=uid(),key=key)); db.commit()
        raise HTTPException(401,"Email or password is incorrect.")
    new_session(db,u,response)
    return user_public(u)

@app.post("/api/auth/register")
def register(body:Registration,response:Response,db=Depends(db_session)):
    if auth_mode()=='open': raise HTTPException(404,'Registration is disabled. Open a workspace instead.')
    if len(body.password)<12: raise HTTPException(422,"Use a password with at least 12 characters.")
    if "@" not in body.email or " " in body.email: raise HTTPException(422,"Enter a valid email address.")
    u=User(id=uid(),email=body.email.lower().strip(),name=body.name.strip(),password=hash_password(body.password),role="student")
    db.add(u)
    try: db.commit()
    except IntegrityError:
        db.rollback(); raise HTTPException(409,"This email is already registered.")
    new_session(db,u,response)
    return user_public(u)

@app.get("/api/auth/me")
def me(u=Depends(current_user)): return user_public(u)

@app.post("/api/auth/logout")
def logout(request:Request,response:Response,db=Depends(db_session)):
    session=db.get(AuthSession,hashlib.sha256(request.cookies.get("logic_session","").encode()).hexdigest())
    if session: db.delete(session); db.commit()
    response.delete_cookie("logic_session",path="/")
    return {"ok":True}

def question_public(q):
    return {"id":q.id,"subject":q.subject,"domain":q.domain,"difficulty":q.difficulty,"skill":q.skill,"status":q.status,"version":q.version,"content":q.content,"source":q.source,"validation":q.validation}

def safe_content(c):
    return {k:v for k,v in c.items() if k in ("stem","presentation","asset","asset_alt","diagram")} | {"options":[{"id":x["id"],"text":x["text"]} for x in c["options"]]}

def snapshot(q):
    attribution=None
    if q.source.get('kind') in ('textbook-excerpt','adapted-textbook'):
        prefix='Adapted from' if q.source['kind']=='adapted-textbook' else 'From'
        attribution=f"{prefix} LearningExpress, 501 Challenging Logic and Reasoning Problems, 2nd ed., question {q.source.get('question_number')}."
    return {"id":q.id,"version":q.version,"subject":q.subject,"domain":q.domain,"difficulty":q.difficulty,"skill":q.skill,"content":q.content,'attribution':attribution}

@app.get("/api/questions")
def questions(subject:str|None=None,domain:str|None=None,difficulty:str|None=None,skill:str|None=None,status:str|None=None,search:str="",u=Depends(teacher),db=Depends(db_session)):
    query=select(Question).order_by(Question.created.desc())
    for field,val in [(Question.subject,subject),(Question.domain,domain),(Question.difficulty,difficulty),(Question.skill,skill),(Question.status,status)]:
        if val: query=query.where(field==val)
    result=[question_public(q) for q in db.scalars(query).all()]
    if search: result=[q for q in result if search.lower() in q["content"]["stem"].lower()]
    return result

class Generation(StrictModel):
    domain: str
    difficulty: Literal["Foundation","Practice","Exam Level","Challenge"]
    options: Literal[4,5]=4
    count:int=Field(default=5,ge=1,le=30)
    presentation:Literal["text","diagram"]="text"
    skill:str|None=None

@app.post("/api/questions/generate")
def generation(body:Generation,u=Depends(teacher),db=Depends(db_session)):
    if body.domain not in [d["id"] for d in DOMAINS]: raise HTTPException(422,"Unknown domain")
    result=[]
    signatures={(q.content['stem'],len(q.content['options'])) for q in db.scalars(select(Question).where(Question.domain==body.domain,Question.difficulty==body.difficulty))}
    for _ in range(body.count):
        for retry in range(100):
            try: q=make_question(body.domain,body.difficulty,body.options,random.SystemRandom().randint(1,2**30),body.presentation,body.skill)
            except ValueError as e: raise HTTPException(422,str(e))
            signature=(q.content['stem'],len(q.content['options']))
            if signature not in signatures: break
        else: raise HTTPException(422,'This bounded template family has no remaining unique questions for the requested count. Generate fewer, change the skill/level, or author a new question.')
        signatures.add(signature)
        db.add(q); audit(db,u,q.id,"generated",{"version":1}); result.append(question_public(q))
    db.commit()
    return result

class QuestionEdit(StrictModel):
    version:int
    content:dict

class OptionBody(StrictModel):
    id: Literal['A','B','C','D','E']
    text: str = Field(max_length=4000)
    rationale: str = Field(max_length=4000)
    error: str = Field(max_length=100)

class DiagramBody(StrictModel):
    kind: Literal['flow','stations','cycle']
    labels: list[str] = Field(min_length=1,max_length=12)

class ContentBody(StrictModel):
    stem: str = Field(max_length=16000)
    options: list[OptionBody] = Field(min_length=4,max_length=5)
    correct: Literal['A','B','C','D','E']
    explanation: str = Field(max_length=16000)
    math: str | None = Field(default=None,max_length=2000)
    presentation: Literal['text','image','diagram']
    asset: str | None = Field(default=None,max_length=2800000)
    asset_alt: str = Field(default='',max_length=1000)
    diagram: DiagramBody | None = None
    validator: dict | None = None

@app.patch("/api/questions/{qid}")
def edit(qid:str,body:QuestionEdit,u=Depends(teacher),db=Depends(db_session)):
    q=db.get(Question,qid)
    if not q: raise HTTPException(404,"Question not found")
    if q.version!=body.version: raise HTTPException(409,"Question changed. Reload before editing.")
    try: body.content=ContentBody.model_validate(body.content).model_dump()
    except ValueError: raise HTTPException(422,"Question fields must contain text, 4/5 complete options, and supported media settings.")
    if len(str(body.content))>3000000: raise HTTPException(413,"Question exceeds content limit")
    report=validate(body.content)
    source=q.source
    if source.get('kind') in ('textbook-excerpt','adapted-textbook'):
        source={**source,'kind':'adapted-textbook','book_key_verified':False,'basis':'Teacher-edited adaptation of a textbook question; the original key check no longer certifies this revision.'}
    changed=db.execute(update(Question).where(Question.id==qid,Question.version==body.version).values(content=body.content,source=source,validation=report,status="draft",version=body.version+1))
    if changed.rowcount!=1: raise HTTPException(409,"Concurrent edit. Reload.")
    audit(db,u,qid,"edited",{"version":body.version+1,"previous_content":q.content,"previous_status":q.status})
    db.commit(); db.expire_all()
    return question_public(db.get(Question,qid))

class ReviewAction(StrictModel):
    action:Literal["review","approve","reject","regenerate"]
    version:int
    note:str=Field(default="",max_length=2000)
    attested:bool=False

@app.post("/api/questions/{qid}/review")
def review(qid:str,body:ReviewAction,u=Depends(teacher),db=Depends(db_session)):
    q=db.get(Question,qid)
    if not q: raise HTTPException(404,"Question not found")
    if q.version!=body.version: raise HTTPException(409,"Question changed. Reload.")
    transitions={"review":("draft","rejected"),"approve":("review",),"reject":("draft","review","approved"),"regenerate":("draft","review","rejected","approved")}
    if q.status not in transitions[body.action]: raise HTTPException(409,"Invalid workflow transition.")
    report=validate(q.content)
    content=q.content
    source=q.source
    if body.action=="approve" and (not report["passed"] or not body.attested):
        raise HTTPException(422,"Fix validation issues and confirm that you reviewed the wording, answer, and distractors.")
    if body.action=="reject" and not body.note.strip(): raise HTTPException(422,"Add a rejection reason.")
    if body.action=="regenerate":
        if q.source.get('kind') in ('textbook-excerpt','adapted-textbook'): raise HTTPException(422,'Textbook selections are fixed transcriptions. Use Generation studio to create an original question instead.')
        seed=random.SystemRandom().randint(1,2**30)
        content=generate(q.domain,q.difficulty,len(q.content["options"]),seed,q.content["presentation"] if q.content["presentation"]!="image" else "text",q.skill)
        source={**q.source,'generation_seed':seed}
        content.pop("skill"); report=validate(content)
    status={"review":"review","approve":"approved","reject":"rejected","regenerate":"draft"}[body.action]
    changed=db.execute(update(Question).where(Question.id==qid,Question.version==body.version).values(content=content,source=source,validation=report,status=status,version=body.version+1))
    if changed.rowcount!=1: raise HTTPException(409,"Concurrent review. Reload.")
    audit(db,u,qid,body.action,{"version":body.version+1,"note":body.note,"attested":body.attested,"previous_content":q.content,"previous_status":q.status})
    db.commit(); db.expire_all()
    return question_public(db.get(Question,qid))

@app.get("/api/questions/{qid}/history")
def history(qid:str,u=Depends(teacher),db=Depends(db_session)):
    return [{"action":a.action,"detail":a.detail,"at":utc(a.created).isoformat()} for a in db.scalars(select(Audit).where(Audit.entity_id==qid).order_by(Audit.created.desc()))]

class BlueprintRow(StrictModel):
    domain:str
    difficulty:Literal["Foundation","Practice","Exam Level","Challenge"]
    count:int=Field(ge=1,le=50)
    options:Literal[4,5]=4
    skill:str|None=None

class BlueprintBody(StrictModel):
    name:str=Field(min_length=1,max_length=120)
    minutes:int=Field(ge=1,le=180)
    rows:list[BlueprintRow]=Field(min_length=1,max_length=28)
    published:bool=False

def pool(db,row):
    query=select(Question).where(Question.status=="approved",Question.domain==row["domain"],Question.difficulty==row["difficulty"])
    if row.get("skill"): query=query.where(Question.skill==row["skill"])
    return [q for q in db.scalars(query).all() if len(q.content["options"])==row["options"]]

def resolve_blueprint(db,rows):
    chosen=[]; used=set()
    for r in rows:
        candidates=[q for q in pool(db,r) if q.id not in used]
        if len(candidates)<r["count"]: raise HTTPException(422,f"Not enough approved {r['options']}-option questions in {r['domain']} / {r['difficulty']}: need {r['count']}, available {len(candidates)}.")
        selected=random.SystemRandom().sample(candidates,r["count"])
        chosen.extend(selected); used.update(q.id for q in selected)
    if len(chosen)>100: raise HTTPException(422,"Mock exams are limited to 100 questions.")
    random.SystemRandom().shuffle(chosen)
    return chosen

@app.post("/api/blueprints")
def create_blueprint(body:BlueprintBody,u=Depends(teacher),db=Depends(db_session)):
    rows=[r.model_dump() for r in body.rows]
    if any(r["domain"] not in [d["id"] for d in DOMAINS] for r in rows): raise HTTPException(422,"Unknown domain")
    if body.published: resolve_blueprint(db,rows)
    b=Blueprint(id=uid(),name=body.name,minutes=body.minutes,rows=rows,published=body.published,creator_id=u.id)
    db.add(b); audit(db,u,b.id,"blueprint_created",body.model_dump()); db.commit()
    return {"id":b.id}

@app.get("/api/blueprints")
def blueprints(u=Depends(current_user),db=Depends(db_session)):
    bs=db.scalars(select(Blueprint)).all()
    return [{"id":b.id,"name":b.name,"minutes":b.minutes,"rows":b.rows,"published":b.published} for b in bs if u.role=="teacher" or b.published]

@app.patch('/api/blueprints/{bid}')
def edit_blueprint(bid:str,body:BlueprintBody,u=Depends(teacher),db=Depends(db_session)):
    b=db.get(Blueprint,bid)
    if not b: raise HTTPException(404,'Blueprint not found')
    rows=[r.model_dump() for r in body.rows]
    if any(r['domain'] not in [d['id'] for d in DOMAINS] for r in rows): raise HTTPException(422,'Unknown domain')
    if body.published: resolve_blueprint(db,rows)
    audit(db,u,bid,'blueprint_updated',{'previous':{'name':b.name,'minutes':b.minutes,'rows':b.rows,'published':b.published},'updated':body.model_dump()})
    b.name=body.name;b.minutes=body.minutes;b.rows=rows;b.published=body.published;db.commit()
    return {'id':bid}

@app.get("/api/availability")
def availability(u=Depends(current_user),db=Depends(db_session)):
    result=[]
    for q in db.scalars(select(Question).where(Question.status=="approved")):
        key={"subject":q.subject,"domain":q.domain,"difficulty":q.difficulty,"skill":q.skill,"options":len(q.content["options"]),'origin':'textbook' if q.source.get('kind') in ('textbook-excerpt','adapted-textbook') else 'original'}
        entry=next((x for x in result if all(x[k]==v for k,v in key.items())),None)
        if entry: entry["count"]+=1
        else: result.append({**key,"count":1})
    return result

class AttemptStart(StrictModel):
    mode:Literal["practice","exam","mock"]
    subject:str|None=None
    domain:str|None=None
    difficulty:str|None=None
    skill:str|None=None
    options:Literal[4,5]=4
    count:int=Field(default=5,ge=1,le=50)
    minutes:int=Field(default=15,ge=1,le=180)
    blueprint_id:str|None=None
    origin:Literal['all','original','textbook']='all'

def attempt_view(a):
    finished=a.submitted is not None
    questions=[]
    for q in a.snapshots:
        c=q["content"]; answer=a.answers.get(q["id"])
        feedback=finished or (a.mode=="practice" and answer is not None)
        public={k:v for k,v in q.items() if k!="content"}
        public["content"]=safe_content(c)
        if feedback:
            public["feedback"]={"correct":c["correct"],"explanation":c["explanation"],"math":c.get("math"),"options":c["options"],"is_correct":answer==c["correct"]}
        questions.append(public)
    return {"id":a.id,"mode":a.mode,"title":a.title,"started":utc(a.started).isoformat(),"deadline":utc(a.deadline).isoformat() if a.deadline else None,"submitted":utc(a.submitted).isoformat() if finished else None,"answers":a.answers,"questions":questions,"score":sum(a.answers.get(q["id"])==q["content"]["correct"] for q in a.snapshots) if finished else None,"server_time":now().isoformat()}

@app.post("/api/attempts")
def start(body:AttemptStart,u=Depends(current_user),db=Depends(db_session)):
    if body.mode=="mock":
        b=db.get(Blueprint,body.blueprint_id)
        if not b or (not b.published and u.role!="teacher"): raise HTTPException(404,"Published blueprint not found.")
        qs=resolve_blueprint(db,b.rows); minutes=b.minutes; title=b.name
    else:
        query=select(Question).where(Question.status=="approved")
        for field,val in [(Question.subject,body.subject),(Question.domain,body.domain),(Question.difficulty,body.difficulty),(Question.skill,body.skill)]:
            if val: query=query.where(field==val)
        available=[q for q in db.scalars(query) if len(q.content["options"])==body.options and (body.origin=='all' or ('textbook' if q.source.get('kind') in ('textbook-excerpt','adapted-textbook') else 'original')==body.origin)]
        if len(available)<body.count: raise HTTPException(422,f"Only {len(available)} approved questions match. Reduce the count or broaden your filters.")
        qs=random.SystemRandom().sample(available,body.count); minutes=body.minutes; title="Focused practice" if body.mode=="practice" else "Exam practice"
    a=Attempt(id=uid(),user_id=u.id,mode=body.mode,title=title,snapshots=[snapshot(q) for q in qs],answers={},started=now(),deadline=now()+timedelta(minutes=minutes) if body.mode!="practice" else None)
    db.add(a); db.commit()
    return attempt_view(a)

def owned_attempt(db,aid,u):
    a=db.scalar(select(Attempt).where(Attempt.id==aid,Attempt.user_id==u.id).with_for_update())
    if not a: raise HTTPException(404,"Attempt not found")
    if not a.submitted and a.deadline and utc(a.deadline)<=now():
        db.execute(update(Attempt).where(Attempt.id==a.id,Attempt.submitted.is_(None)).values(submitted=now(),revision=Attempt.revision+1))
        db.commit();db.refresh(a)
    return a

@app.get("/api/attempts")
def attempts(u=Depends(current_user),db=Depends(db_session)):
    return [{"id":a.id,"title":a.title,"mode":a.mode,"submitted":bool(a.submitted),"started":utc(a.started).isoformat(),"count":len(a.snapshots)} for a in db.scalars(select(Attempt).where(Attempt.user_id==u.id).order_by(Attempt.started.desc()))]

@app.get("/api/attempts/{aid}")
def get_attempt(aid:str,u=Depends(current_user),db=Depends(db_session)):
    return attempt_view(owned_attempt(db,aid,u))

class Answer(StrictModel):
    question_id:str
    option_id:Literal["A","B","C","D","E"]

@app.post("/api/attempts/{aid}/answer")
def answer(aid:str,body:Answer,u=Depends(current_user),db=Depends(db_session)):
    a=owned_attempt(db,aid,u)
    if a.submitted: raise HTTPException(409,"Attempt is already finished. Reload to see results.")
    q=next((q for q in a.snapshots if q["id"]==body.question_id),None)
    if not q or body.option_id not in [o["id"] for o in q["content"]["options"]]: raise HTTPException(422,"Invalid question or option.")
    if a.mode=="practice" and body.question_id in a.answers: raise HTTPException(409,"Practice answers are final after feedback.")
    changed=db.execute(update(Attempt).where(Attempt.id==aid,Attempt.revision==a.revision,Attempt.submitted.is_(None)).values(answers={**a.answers,body.question_id:body.option_id},revision=a.revision+1))
    if changed.rowcount!=1: raise HTTPException(409,'Another tab changed this attempt. Reload before answering.')
    db.commit();db.refresh(a)
    return attempt_view(a)

@app.post("/api/attempts/{aid}/submit")
def submit(aid:str,u=Depends(current_user),db=Depends(db_session)):
    a=owned_attempt(db,aid,u)
    if not a.submitted:
        changed=db.execute(update(Attempt).where(Attempt.id==aid,Attempt.revision==a.revision,Attempt.submitted.is_(None)).values(submitted=now(),revision=a.revision+1))
        if changed.rowcount!=1: raise HTTPException(409,'Another tab changed this attempt. Reload before submitting.')
        db.commit();db.refresh(a)
    return attempt_view(a)

@app.get("/api/analytics")
def analytics(u=Depends(current_user),db=Depends(db_session)):
    query=select(Attempt).where(Attempt.submitted.is_not(None))
    if u.role!="teacher": query=query.where(Attempt.user_id==u.id)
    else: query=query.join(User,User.id==Attempt.user_id).where(User.role=='student')
    attempts=db.scalars(query).all(); groups={}; errors={}; answered=0; correct=0
    for a in attempts:
        for q in a.snapshots:
            selected=a.answers.get(q["id"]); c=q["content"]; ok=selected==c["correct"]
            answered+=1; correct+=int(ok)
            for key in ["domain","difficulty"]:
                k=(key,q[key]); g=groups.setdefault(k,{"kind":key,"label":q[key],"total":0,"correct":0})
                g["total"]+=1; g["correct"]+=int(ok)
            if not ok:
                tag=next((o["error"] for o in c["options"] if o["id"]==selected),"unanswered")
                errors[tag]=errors.get(tag,0)+1
    return {"scope":"All students" if u.role=="teacher" else "Your completed attempts","attempts":len(attempts),"questions":answered,"correct":correct,"groups":list(groups.values()),"errors":[{"label":k,"count":v} for k,v in sorted(errors.items(),key=lambda x:-x[1])],"note":"Observed distractor choices are indicators of possible misconceptions, not diagnoses."}

def student_rows(db):
    """Per-student totals, counting completed attempts only."""
    done={}
    for a in db.scalars(select(Attempt).where(Attempt.submitted.is_not(None))):
        done.setdefault(a.user_id,[]).append(a)
    rows=[]
    for s in db.scalars(select(User).where(User.role=='student').order_by(User.name)):
        mine=done.get(s.id,[]); answered=correct=0; subjects={}
        for a in mine:
            for q in a.snapshots:
                hit=int(a.answers.get(q["id"])==q["content"]["correct"])
                answered+=1; correct+=hit
                # Attempts taken before subjects existed carry no subject.
                key=q.get("subject") or "logic"
                g=subjects.setdefault(key,{"subject":key,"answered":0,"correct":0})
                g["answered"]+=1; g["correct"]+=hit
        last=max((utc(a.submitted) for a in mine),default=None)
        rows.append({"id":s.id,"name":s.name,"email":s.email,
                     "anonymous":s.email.endswith("@guest.invalid"),
                     "registered":utc(s.created).isoformat() if s.created else None,
                     "sessions":len(mine),"answered":answered,"correct":correct,
                     "accuracy":round(correct/answered*100) if answered else None,
                     "last_active":last.isoformat() if last else None,
                     "subjects":sorted(subjects.values(),key=lambda x:x["subject"])})
    return rows

@app.get("/api/students")
def students(u=Depends(teacher),db=Depends(db_session)):
    return student_rows(db)

# Declared before /api/students/{sid}, or "export.csv" matches as an id.
@app.get("/api/students/export.csv")
def students_csv(u=Depends(teacher),db=Depends(db_session)):
    # Anonymous open-mode workspaces are browser sessions, not students, and
    # carry no name or address worth exporting.
    rows=[r for r in student_rows(db) if not r["anonymous"]]
    out=io.StringIO(); writer=csv.writer(out)
    writer.writerow(["Name","Email","Registered","Completed sessions","Questions answered","Correct","Accuracy %","Last active"])
    for r in rows:
        writer.writerow([r["name"],r["email"],r["registered"] or "",r["sessions"],r["answered"],
                         r["correct"],"" if r["accuracy"] is None else r["accuracy"],r["last_active"] or ""])
    # Exporting names and addresses is a disclosure of personal data; record it.
    audit(db,u,uid(),"students_export",{"students":len(rows)}); db.commit()
    return Response(content=out.getvalue(),media_type="text/csv",
                    headers={"Content-Disposition":'attachment; filename="students.csv"'})

@app.get("/api/students/{sid}")
def student_detail(sid:str,u=Depends(teacher),db=Depends(db_session)):
    s=db.get(User,sid)
    if not s or s.role!="student": raise HTTPException(404,"Student not found.")
    sessions=[]; topics={}
    for a in db.scalars(select(Attempt).where(Attempt.user_id==sid,Attempt.submitted.is_not(None)).order_by(Attempt.submitted.desc())):
        score=sum(a.answers.get(q["id"])==q["content"]["correct"] for q in a.snapshots)
        sessions.append({"id":a.id,"title":a.title,"mode":a.mode,"score":score,
                         "total":len(a.snapshots),"submitted":utc(a.submitted).isoformat()})
        for q in a.snapshots:
            hit=int(a.answers.get(q["id"])==q["content"]["correct"])
            g=topics.setdefault(q["domain"],{"domain":q["domain"],"subject":q.get("subject") or "logic","answered":0,"correct":0})
            g["answered"]+=1; g["correct"]+=hit
    return {"id":s.id,"name":s.name,"email":s.email,
            "registered":utc(s.created).isoformat() if s.created else None,
            "sessions":sessions,"topics":sorted(topics.values(),key=lambda x:-x["answered"])}

class ExportBody(StrictModel):
    ids:list[str]=Field(min_length=1,max_length=100)
    format:Literal["docx","pdf"]
    kind:Literal["paper","key","solutions"]="paper"
    title:str=Field(default="Entrance preparation · Mechanical Engineering @ RUPP",max_length=120)

@app.post("/api/export")
def export(body:ExportBody,u=Depends(teacher),db=Depends(db_session)):
    from .exports import render_export
    questions=[]
    for qid in body.ids:
        q=db.get(Question,qid)
        if not q or q.status!="approved": raise HTTPException(422,"Exports require approved questions.")
        questions.append(q)
    raw,mime=render_export(questions,body.format,body.kind,body.title)
    audit(db,u,uid(),"export",body.model_dump()); db.commit()
    return Response(content=raw,media_type=mime,headers={"Content-Disposition":f'attachment; filename="rupp-entrance-prep-{body.kind}.{body.format}"'})
