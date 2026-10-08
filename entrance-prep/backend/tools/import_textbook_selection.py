"""Explicit, idempotent import of a small checked selection from an owner-supplied PDF.

Requires the private selection JSON and exact reference PDF; neither is bundled.
Verifies transcription, printed answer key, and independent structured answer.
Nothing is automatically imported at startup or copied from the full book.
"""
import argparse, hashlib, json, re, sys, unicodedata, uuid
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.models import SessionLocal, Question, User, Audit
from app.catalog import SOURCE
from app.validation import validate
from sqlalchemy import select
from pypdf import PdfReader

def normalized(text):
    text=unicodedata.normalize('NFKC',text)
    text=re.sub(r'(?<=\w)-\s*\n\s*(?=\w)','',text)
    for broken,word in [('W h a t','What'),('W hat','What')]:text=text.replace(broken,word)
    return re.sub(r'\s+','',text).casefold()

def verify_transcription(entry,reader):
    number=entry['question_number'];c=entry['content']
    page=reader.pages[entry['pdf_question_page']-1].extract_text() or ''
    match=re.search(rf'(?ms)^\s*{number}\.\s*(.*?)(?=^\s*{number+1}\.\s|^–QUESTIONS|\Z)',page)
    if not match:raise ValueError(f'Question {number} is not on its declared source page.')
    pieces=re.split(r'(?m)^\s*([a-e])\.\s*',match[1])
    if normalized(pieces[0])!=normalized(c['stem']):raise ValueError(f'Question {number}: transcription differs from the PDF stem.')
    original=[(pieces[i].upper(),pieces[i+1]) for i in range(1,len(pieces)-1,2)]
    if len(original)!=len(c['options']) or any(oid!=o['id'] or normalized(text)!=normalized(o['text']) for (oid,text),o in zip(original,c['options'])):
        raise ValueError(f'Question {number}: original choices or order changed.')
    key_page=reader.pages[entry['pdf_key_page']-1].extract_text() or ''
    key=re.search(rf'(?m)^\s*{number}\.\s*([a-e])\.',key_page)
    if not key or key[1].upper()!=c['correct']:raise ValueError(f'Question {number}: answer conflicts with the printed key.')
    checked=validate(c)
    if not checked['passed'] or checked['method']!='deterministic':raise ValueError(f'Question {number}: independent check failed: {checked}')
    return checked

def import_selection(selection,pdf):
    payload=json.loads(Path(selection).read_text(encoding='utf-8'))
    checksum=hashlib.sha256(Path(pdf).read_bytes()).hexdigest()
    if checksum!=payload['pdf_sha256']:raise ValueError('Reference PDF checksum differs from the checked source.')
    entries=payload['questions']
    if not 1<=len(entries)<=7:raise ValueError('This importer is bounded to a small selection of at most seven questions.')
    reader=PdfReader(pdf)
    reports=[verify_transcription(entry,reader) for entry in entries]
    inserted=0
    with SessionLocal() as db:
        teacher=db.scalar(select(User).where(User.role=='teacher'))
        if not teacher:raise ValueError('Initialize the app before importing.')
        for entry,report in zip(entries,reports):
            qid=str(uuid.uuid5(uuid.NAMESPACE_URL,f"learningexpress:1576855341:selection-v1:{entry['question_number']}"))
            if db.get(Question,qid):continue
            source={**SOURCE,'kind':'textbook-excerpt','basis':'Original stem and original choices transcribed from the user-supplied PDF; layout/OCR spacing normalized. Explanation and distractor rationales are newly authored.',
                    'sets':entry['set'],'question_number':entry['question_number'],'pdf_question_page':entry['pdf_question_page'],'pdf_key_page':entry['pdf_key_page'],'printed_question_page':entry['printed_question_page'],'printed_key_page':entry['printed_key_page'],
                    'pdf_sha256':checksum,'book_key_verified':True,'checked_at':datetime.now(timezone.utc).isoformat(),
                    'verification':'Transcription + printed key + independent deterministic solution all agree. This is not a blanket guarantee for generated questions.'}
            report={**report,'book_key_verified':True,'transcription_verified':True,'note':'Printed key and independent rule agree. Difficulty is a local rubric. Teacher edits require review again.'}
            db.add(Question(id=qid,domain=entry['domain'],difficulty=entry['difficulty'],skill=entry['skill'],status='approved',content=entry['content'],source=source,validation=report,version=1))
            db.add(Audit(id=str(uuid.uuid4()),user_id=teacher.id,entity_id=qid,action='checked_textbook_import',detail={'question_number':entry['question_number'],'printed_key_matched':True,'independent_rule_passed':True,'transcription_matched':True,'authorization':'User requested a small textbook selection for student practice.'}))
            inserted+=1
        db.commit()
    return {'added':inserted,'checked':len(entries),'question_numbers':[e['question_number'] for e in entries]}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--selection',required=True);parser.add_argument('--pdf',required=True);args=parser.parse_args()
    print(json.dumps(import_selection(args.selection,args.pdf)))
