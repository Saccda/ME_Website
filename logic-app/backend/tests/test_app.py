import os
os.environ["DATABASE_URL"]="sqlite:///./test-logic.db"
os.environ["DEMO_MODE"]="true"
os.environ['AUTH_MODE']='credentials'
from datetime import timedelta
from io import BytesIO
from zipfile import ZipFile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from app.main import app
from app.models import Base, engine, SessionLocal, Question, Attempt, now
from app.generator import generate
from app.validation import validate
from app.catalog import DOMAINS, LEVELS

@pytest.fixture
def clients():
    Base.metadata.drop_all(engine)
    with TestClient(app,headers={"X-App-Request":"1"}) as teacher, TestClient(app,headers={"X-App-Request":"1"}) as student:
        assert teacher.post('/api/auth/login',json={"email":"teacher@demo.local","password":"teacher-demo-2026"}).status_code==200
        assert student.post('/api/auth/login',json={"email":"student@demo.local","password":"student-demo-2026"}).status_code==200
        yield teacher,student

def test_student_access_and_no_key_leakage(clients):
    teacher,student=clients
    assert student.get('/api/questions').status_code==403
    assert student.post('/api/questions/generate',json={"domain":"patterns","difficulty":"Foundation"}).status_code==403
    a=student.post('/api/attempts',json={"mode":"exam","count":4,"options":5}).json()
    for q in a['questions']:
        assert len(q['content']['options'])==5
        assert not {'correct','explanation','validator','math','source'} & q['content'].keys()
        assert 'source' not in q
        assert all(set(o)=={'id','text'} for o in q['content']['options'])

def test_immediate_vs_delayed_feedback(clients):
    teacher,student=clients
    for mode in ['practice','exam']:
        a=student.post('/api/attempts',json={"mode":mode,"count":2}).json()
        q=a['questions'][0]
        response=student.post(f"/api/attempts/{a['id']}/answer",json={"question_id":q['id'],"option_id":"A"})
        assert response.status_code==200
        assert ('feedback' in response.json()['questions'][0]) == (mode=='practice')
        repeat=student.post(f"/api/attempts/{a['id']}/answer",json={"question_id":q['id'],"option_id":"B"})
        assert repeat.status_code==(409 if mode=='practice' else 200)
        submitted=student.post(f"/api/attempts/{a['id']}/submit").json()
        assert all('feedback' in q for q in submitted['questions'])
        assert submitted['score'] is not None
        assert student.post(f"/api/attempts/{a['id']}/answer",json={"question_id":q['id'],"option_id":"B"}).status_code==409

def test_review_transition_edit_revision_and_snapshot(clients):
    teacher,student=clients
    a=student.post('/api/attempts',json={"mode":"practice","count":1}).json()
    qid=a['questions'][0]['id']
    q=next(q for q in teacher.get('/api/questions').json() if q['id']==qid)
    original=a['questions'][0]['content']['stem']
    c=q['content']; c['stem']="Updated wording. "+c['stem']
    edited=teacher.patch('/api/questions/'+qid,json={"version":q['version'],"content":c}).json()
    assert edited['status']=='draft'
    assert teacher.patch('/api/questions/'+qid,json={"version":q['version'],"content":c}).status_code==409
    assert student.get('/api/attempts/'+a['id']).json()['questions'][0]['content']['stem']==original
    assert teacher.post(f'/api/questions/{qid}/review',json={"version":edited['version'],"action":"approve","attested":True}).status_code==409
    review=teacher.post(f'/api/questions/{qid}/review',json={"version":edited['version'],"action":"review"}).json()
    assert teacher.post(f'/api/questions/{qid}/review',json={"version":review['version'],"action":"approve"}).status_code==422
    approved=teacher.post(f'/api/questions/{qid}/review',json={"version":review['version'],"action":"approve","attested":True}).json()
    assert approved['status']=='approved'
    assert len(teacher.get(f'/api/questions/{qid}/history').json())>=4

def test_deterministic_rejects_key_tampering_and_bad_options(clients):
    teacher,_=clients
    q=teacher.post('/api/questions/generate',json={"domain":"patterns","difficulty":"Challenge","count":1}).json()[0]
    c=q['content'];c['correct']=next(o['id'] for o in c['options'] if o['id']!=c['correct'])
    updated=teacher.patch('/api/questions/'+q['id'],json={"version":q['version'],"content":c}).json()
    assert not updated['validation']['passed']
    review=teacher.post(f"/api/questions/{q['id']}/review",json={"version":updated['version'],"action":"review"}).json()
    assert teacher.post(f"/api/questions/{q['id']}/review",json={"version":review['version'],"action":"approve","attested":True}).status_code==422

def test_expiration_and_attempt_ownership(clients):
    teacher,student=clients
    a=student.post('/api/attempts',json={"mode":"exam","count":1}).json()
    assert teacher.get('/api/attempts/'+a['id']).status_code==404
    with SessionLocal() as db:
        record=db.get(Attempt,a['id']);record.deadline=now()-timedelta(seconds=1);db.commit()
    assert student.post(f"/api/attempts/{a['id']}/answer",json={"question_id":a['questions'][0]['id'],"option_id":"A"}).status_code==409
    result=student.get('/api/attempts/'+a['id']).json()
    assert result['submitted'] and result['score']==0

def test_blueprint_exact_counts_and_capacity(clients):
    teacher,student=clients
    body={"name":"Test mock","minutes":1,"published":True,"rows":[{"domain":"patterns","difficulty":"Practice","options":4,"count":1},{"domain":"deduction","difficulty":"Challenge","options":5,"count":1}]}
    response=teacher.post('/api/blueprints',json=body);assert response.status_code==200
    a=student.post('/api/attempts',json={"mode":"mock","blueprint_id":response.json()['id']}).json()
    assert len(a['questions'])==2
    assert len({q['id'] for q in a['questions']})==2
    assert sorted(q['domain'] for q in a['questions'])==['deduction','patterns']
    body['rows'][0]['count']=50
    assert teacher.post('/api/blueprints',json=body).status_code==422
    assert student.post('/api/blueprints',json=body).status_code==403

def test_approved_only_and_server_scoring(clients):
    teacher,student=clients
    q=teacher.post('/api/questions/generate',json={"domain":"patterns","difficulty":"Foundation","count":1}).json()[0]
    for _ in range(4):
        a=student.post('/api/attempts',json={"mode":"practice","domain":"patterns","difficulty":"Foundation","count":1}).json()
        assert a['questions'][0]['id']!=q['id']
    qid=a['questions'][0]['id']
    key=next(q for q in teacher.get('/api/questions').json() if q['id']==qid)['content']['correct']
    assert student.post(f"/api/attempts/{a['id']}/answer",json={"question_id":qid,"option_id":key,"score":100}).status_code==422
    student.post(f"/api/attempts/{a['id']}/answer",json={"question_id":qid,"option_id":key})
    assert student.post(f"/api/attempts/{a['id']}/submit").json()['score']==1
    stats=student.get('/api/analytics').json(); assert stats['correct']==1 and stats['questions']==1

def test_exports_are_private_teacher_only_and_complete(clients):
    teacher,student=clients
    qs=teacher.get('/api/questions').json()[:3]
    for format in ['docx','pdf']:
        body={"ids":[q['id'] for q in qs],"format":format,"kind":"solutions"}
        assert student.post('/api/export',json=body).status_code==403
        r=teacher.post('/api/export',json=body);assert r.status_code==200
        if format=='pdf': assert r.content.startswith(b'%PDF')
        else:
            xml=ZipFile(BytesIO(r.content)).read('word/document.xml').decode()
            assert 'LearningExpress' not in xml
            assert 'Answer:' in xml
            assert qs[0]['content']['correct'] in xml

def test_export_renders_mathematics_as_equations(clients):
    teacher,_=clients
    with SessionLocal() as db:
        q=db.scalar(select(Question).where(Question.status=='approved'))
        q.content={**q.content,'stem':'Find $v$ when $a = 2$ and $t = 5$.','math':r'x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}'}
        db.commit();qid=q.id
    body={"ids":[qid],"format":"docx","kind":"solutions"}
    r=teacher.post('/api/export',json=body);assert r.status_code==200
    xml=ZipFile(BytesIO(r.content)).read('word/document.xml').decode()
    # Word equations, not literal LaTeX: a paper printed with "$" is unusable.
    assert '<m:oMath' in xml and '<m:rad' in xml and '<m:f>' in xml
    assert '$' not in xml and '\\frac' not in xml
    pdf=teacher.post('/api/export',json={**body,'format':'pdf'});assert pdf.status_code==200
    assert pdf.content.startswith(b'%PDF')

def test_latex_converts_for_word_and_for_print():
    from app.mathtext import latex_to_omml, latex_to_unicode, inline_to_unicode
    from xml.etree import ElementTree
    for latex in [r'v = u + at',r'E_k = \frac{1}{2}mv^2',r'\sqrt[3]{27}',r'\sum_{i=1}^{n} i^2',
                  r'\theta = 90\degree',r'a_{n+1}=a_n+5',r'\left(\frac{a}{b}\right)^2',r'\unknown',r'']:
        ElementTree.fromstring(latex_to_omml(latex))  # well formed, never raises
        assert '\\' not in latex_to_unicode(latex)
    assert latex_to_unicode(r'E_k = \frac{1}{2}mv^2')=='Eₖ = (1)/(2)mv²'
    assert inline_to_unicode('speed $v^2$ here')=='speed v² here'

def test_student_data_is_teacher_only_and_counts_real_work(clients):
    teacher,student=clients
    a=student.post('/api/attempts',json={"mode":"practice","count":2,"options":4}).json()
    for q in a['questions']:
        student.post(f"/api/attempts/{a['id']}/answer",json={"question_id":q['id'],"option_id":q['content']['options'][0]['id']})
    student.post(f"/api/attempts/{a['id']}/submit")

    # A student must not be able to read the cohort's data.
    assert student.get('/api/students').status_code==403
    assert student.get('/api/students/export.csv').status_code==403

    rows=teacher.get('/api/students').json()
    mine=next(r for r in rows if r['email']=='student@demo.local')
    assert mine['sessions']==1 and mine['answered']==2 and mine['accuracy'] is not None
    assert sum(s['answered'] for s in mine['subjects'])==2

    sheet=teacher.get('/api/students/export.csv')
    assert sheet.status_code==200 and 'text/csv' in sheet.headers['content-type']
    assert 'student@demo.local' in sheet.text and 'Accuracy %' in sheet.text

    detail=teacher.get(f"/api/students/{mine['id']}").json()
    assert len(detail['sessions'])==1 and detail['sessions'][0]['total']==2
    assert detail['topics'] and sum(t['answered'] for t in detail['topics'])==2
    # Teachers are not students, and must not appear as one.
    me=teacher.get('/api/auth/me').json()
    assert teacher.get(f"/api/students/{me['id']}").status_code==404

def test_bulk_approval_touches_only_machine_proved_questions(clients):
    import sys as _sys
    from pathlib import Path as _Path
    _sys.path.insert(0,str(_Path(__file__).resolve().parents[1]/"tools"))
    import approve_verified
    with SessionLocal() as db:
        for q in db.scalars(select(Question)): q.status="draft"
        db.commit()
    approve_verified.run(apply=True)
    with SessionLocal() as db:
        questions=list(db.scalars(select(Question)))
    approved=[q for q in questions if q.status=="approved"]
    pending=[q for q in questions if q.status!="approved"]
    assert approved and pending
    # The whole point: a question nobody and nothing checked stays a draft.
    assert all((q.validation or {}).get("method")=="deterministic" for q in approved)
    assert all((q.validation or {}).get("method")=="editorial" for q in pending)
    assert all(validate(q.content)["passed"] for q in approved)

def test_csrf_invalid_option_and_registration_role(clients):
    teacher,student=clients
    assert student.post('/api/attempts',json={"mode":"practice"},headers={"Origin":"https://evil.example"}).status_code==403
    assert student.post('/api/attempts',json={"mode":"practice"},headers={"X-App-Request":""}).status_code==403
    a=student.post('/api/attempts',json={"mode":"practice","count":1,"options":4}).json()
    assert student.post(f"/api/attempts/{a['id']}/answer",json={"question_id":a['questions'][0]['id'],"option_id":"E"}).status_code==422
    assert student.post('/api/auth/register',json={"name":"Test","email":"test@example.com","password":"a-safe-password","role":"teacher"}).status_code==422
    r=student.post('/api/auth/register',json={"name":"Test","email":"test@example.com","password":"a-safe-password"});assert r.json()['role']=='student'

def test_real_seed_is_draft_only(monkeypatch):
    Base.metadata.drop_all(engine)
    monkeypatch.setenv('DEMO_MODE','false')
    monkeypatch.setenv('TEACHER_EMAIL','reviewer@example.com')
    monkeypatch.setenv('TEACHER_PASSWORD','review-this-content-first')
    with TestClient(app) as c:
        with SessionLocal() as db:
            assert all(q.status=='draft' for q in db.scalars(select(Question)))

def test_blueprint_update_can_withdraw_from_students(clients):
    teacher,student=clients
    bp=teacher.get('/api/blueprints').json()[0]
    body={k:v for k,v in bp.items() if k!='id'};body['published']=False
    assert teacher.patch('/api/blueprints/'+bp['id'],json=body).status_code==200
    assert all(b['id']!=bp['id'] for b in student.get('/api/blueprints').json())
    assert student.post('/api/attempts',json={'mode':'mock','blueprint_id':bp['id']}).status_code==404

def test_malformed_editor_and_bounded_spec(clients):
    teacher,_=clients
    q=teacher.get('/api/questions').json()[0]
    c=q['content'].copy();c['options']=[1,2,3,4]
    assert teacher.patch('/api/questions/'+q['id'],json={'version':q['version'],'content':c}).status_code==422
    c=generate('patterns','Foundation',4,3);c['validator']['terms']=[1]*100000
    assert not validate(c)['passed']

def test_demo_seed_has_unique_stems_per_option_count(clients):
    teacher,_=clients
    questions=teacher.get('/api/questions').json()
    keys=[(q['domain'],q['difficulty'],len(q['content']['options']),q['content']['stem']) for q in questions]
    assert len(set(keys))==len(keys)==len(DOMAINS)*len(LEVELS)*3

def test_mathematics_answers_are_recomputed_not_asserted(clients):
    teacher,_=clients
    maths=teacher.get('/api/questions',params={'subject':'math'}).json()
    assert maths and all(q['subject']=='math' for q in maths)
    # The point of the subject: a machine proves every one of these.
    assert all(q['validation']['method']=='deterministic' and q['validation']['passed'] for q in maths)
    assert all(q['validation']['proof'].startswith('Recomputed') for q in maths)
    logic=teacher.get('/api/questions',params={'subject':'logic'}).json()
    assert logic and all(q['subject']=='logic' for q in logic)

def test_compute_validator_rejects_a_tampered_maths_key(clients):
    from app.generator import generate
    content=generate('triangles','Exam Level',4,4242,'text',None)
    assert validate(content)['passed']
    other=next(o for o in content['options'] if o['id']!=content['correct'])
    assert not validate({**content,'correct':other['id']})['passed']
    # And a distractor that happens to equal the answer is refused as ambiguous.
    keyed=next(o for o in content['options'] if o['id']==content['correct'])
    clash=[{**o,'text':keyed['text']} if o['id']==other['id'] else o for o in content['options']]
    assert not validate({**content,'options':clash})['passed']

def test_open_workspace_requires_no_login_and_preserves_both_identities(clients,monkeypatch):
    monkeypatch.setenv('AUTH_MODE','open')
    with TestClient(app,headers={'X-App-Request':'1'}) as visitor:
        student=visitor.post('/api/workspace',json={}).json()
        assert student['role']=='student'
        assert visitor.get('/api/attempts').status_code==200
        assert visitor.post('/api/auth/login',json={'email':'teacher@demo.local','password':'teacher-demo-2026'}).status_code==404
        a=visitor.post('/api/attempts',json={'mode':'practice','count':1}).json()
        teacher=visitor.post('/api/workspace',json={'role':'teacher'}).json()
        assert teacher['role']=='teacher' and teacher['id']!=student['id']
        assert visitor.get('/api/questions').status_code==200
        assert visitor.get('/api/attempts/'+a['id']).status_code==404
        restored=visitor.post('/api/workspace',json={'role':'student'}).json()
        assert restored['id']==student['id']
        assert visitor.get('/api/attempts/'+a['id']).status_code==200
        assert visitor.post('/api/workspace',json={}).json()['id']==student['id']

def test_open_visitors_do_not_share_progress(clients,monkeypatch):
    monkeypatch.setenv('AUTH_MODE','open')
    with TestClient(app,headers={'X-App-Request':'1'}) as a,TestClient(app,headers={'X-App-Request':'1'}) as b:
        assert a.post('/api/workspace',json={}).json()['id']!=b.post('/api/workspace',json={}).json()['id']
        attempt=a.post('/api/attempts',json={'mode':'practice','count':1}).json()
        assert b.get('/api/attempts/'+attempt['id']).status_code==404
        assert b.get('/api/attempts').json()==[]

def test_open_setup_needs_no_teacher_credentials(monkeypatch):
    Base.metadata.drop_all(engine)
    monkeypatch.setenv('AUTH_MODE','open');monkeypatch.setenv('DEMO_MODE','false')
    monkeypatch.delenv('TEACHER_EMAIL',raising=False);monkeypatch.delenv('TEACHER_PASSWORD',raising=False)
    with TestClient(app,headers={'X-App-Request':'1'}) as visitor:
        assert visitor.post('/api/workspace',json={'role':'teacher'}).status_code==200
        assert all(q['status']=='draft' for q in visitor.get('/api/questions').json())

@pytest.mark.parametrize('domain',[d['id'] for d in DOMAINS])
def test_template_families(domain):
    for level in LEVELS:
        for options in (4,5):
            for seed in range(60):
                c=generate(domain,level,options,seed)
                assert validate(c)['passed']

def test_validation_handles_ambiguity():
    c=generate('deduction','Foundation',4,5)
    c['validator']['rules']=[]
    assert not validate(c)['passed']
    c=generate('patterns','Foundation',4,5)
    c['options'][1]['text']=c['options'][0]['text']
    assert not validate(c)['passed']

def test_textbook_source_filter_and_edit_verification(clients):
    teacher,student=clients
    q=teacher.get('/api/questions').json()[0]
    with SessionLocal() as db:
        record=db.get(Question,q['id'])
        record.source={**record.source,'kind':'textbook-excerpt','question_number':999,'book_key_verified':True}
        db.commit()
    a=student.post('/api/attempts',json={'mode':'practice','count':1,'origin':'textbook','options':len(q['content']['options'])}).json()
    assert a['questions'][0]['id']==q['id']
    assert 'question 999' in a['questions'][0]['attribution']
    assert 'source' not in a['questions'][0]
    assert teacher.post('/api/questions/'+q['id']+'/review',json={'version':q['version'],'action':'regenerate'}).status_code==422
    edited=teacher.patch('/api/questions/'+q['id'],json={'version':q['version'],'content':q['content']}).json()
    assert edited['status']=='draft'
    assert edited['source']['kind']=='adapted-textbook'
    assert edited['source']['book_key_verified'] is False
