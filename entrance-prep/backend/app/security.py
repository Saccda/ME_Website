import hashlib, hmac, os, secrets
from datetime import timedelta, timezone
from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from .models import AuthSession, SessionLocal, User, now

def hash_password(password: str):
    salt = secrets.token_hex(16)
    return salt + ":" + hashlib.scrypt(password.encode(), salt=salt.encode(), n=16384, r=8, p=1).hex()

def verify(password: str, stored: str):
    salt, expected = stored.split(":")
    return hmac.compare_digest(hashlib.scrypt(password.encode(), salt=salt.encode(), n=16384, r=8, p=1).hex(), expected)

def db_session():
    with SessionLocal() as db:
        yield db

def utc(value):
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value

def auth_mode():
    return os.getenv('AUTH_MODE','open').lower()

def current_user(request: Request, db=Depends(db_session)):
    token = request.cookies.get("logic_session", "")
    session = db.get(AuthSession, hashlib.sha256(token.encode()).hexdigest())
    if not session or utc(session.expires) < now():
        raise HTTPException(401, "Reopen your workspace to continue." if auth_mode()=='open' else "Your website session is required.")
    return db.get(User, session.user_id)

def teacher(user=Depends(current_user)):
    if user.role != "teacher":
        raise HTTPException(403, "Teacher access required.")
    return user

def new_session(db, user, response, max_age=43200):
    token = secrets.token_urlsafe(48)
    db.add(AuthSession(token_hash=hashlib.sha256(token.encode()).hexdigest(), user_id=user.id, expires=now()+timedelta(seconds=max_age)))
    db.commit()
    response.set_cookie("logic_session", token, httponly=True, samesite="strict", secure=os.getenv("COOKIE_SECURE", "false").lower()=="true", max_age=max_age, path="/")
