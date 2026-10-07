import os
from datetime import datetime, timezone
from sqlalchemy import create_engine, String, Integer, Text, JSON, DateTime, ForeignKey, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

def now():
    return datetime.now(timezone.utc)

class Base(DeclarativeBase):
    pass

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./logic.db")
# The pool has to be at least as large as the request thread pool, or threads
# queue for a connection and time out. The shipped default of 5 + 10 overflow
# collapsed under a cohort of 250 students signing in at once: 55% of requests
# failed with QueuePool timeouts. Sized above the 40-thread default here, and
# adjustable per deployment -- PostgreSQL's own max_connections must stay above
# (pool_size + max_overflow) x number of workers.
POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "20"))
MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))
POOL_TOTAL = POOL_SIZE + MAX_OVERFLOW
engine = create_engine(
    DATABASE_URL,
    pool_size=POOL_SIZE,
    max_overflow=MAX_OVERFLOW,
    pool_timeout=int(os.getenv("DB_POOL_TIMEOUT", "30")),
    pool_recycle=1800,
    pool_pre_ping=True,
    **({"connect_args": {"check_same_thread": False}} if DATABASE_URL.startswith("sqlite") else {}),
)
if engine.dialect.name == "sqlite":
    @event.listens_for(engine, "connect")
    def sqlite_setup(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA journal_mode=WAL")
        # SQLite serialises writers; without this a concurrent write fails at
        # once instead of waiting its turn.
        connection.execute("PRAGMA busy_timeout=10000")
SessionLocal = sessionmaker(engine, expire_on_commit=False)

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(Text)
    role: Mapped[str] = mapped_column(String(20))
    # Nullable: accounts that existed before this column was added have no
    # honest value, and inventing one would misreport when a cohort signed up.
    created: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=now, nullable=True)

class AuthSession(Base):
    __tablename__ = "auth_sessions"
    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    expires: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class LoginFailure(Base):
    __tablename__ = "login_failures"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    key: Mapped[str] = mapped_column(String(64), index=True)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)

class Question(Base):
    __tablename__ = "questions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    subject: Mapped[str] = mapped_column(String(20), index=True, default="logic")
    domain: Mapped[str] = mapped_column(String(30), index=True)
    skill: Mapped[str] = mapped_column(String(50), index=True)
    difficulty: Mapped[str] = mapped_column(String(20), index=True)
    status: Mapped[str] = mapped_column(String(20), index=True, default="draft")
    content: Mapped[dict] = mapped_column(JSON)
    source: Mapped[dict] = mapped_column(JSON)
    validation: Mapped[dict] = mapped_column(JSON)
    version: Mapped[int] = mapped_column(Integer, default=1)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)

class Audit(Base):
    __tablename__ = "audit_events"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    entity_id: Mapped[str] = mapped_column(String(36), index=True)
    action: Mapped[str] = mapped_column(String(40))
    detail: Mapped[dict] = mapped_column(JSON)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)

class Blueprint(Base):
    __tablename__ = "blueprints"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    minutes: Mapped[int] = mapped_column(Integer)
    rows: Mapped[list] = mapped_column(JSON)
    published: Mapped[bool] = mapped_column(default=False)
    creator_id: Mapped[str] = mapped_column(ForeignKey("users.id"))

class Attempt(Base):
    __tablename__ = "attempts"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    mode: Mapped[str] = mapped_column(String(20))
    title: Mapped[str] = mapped_column(String(120))
    snapshots: Mapped[list] = mapped_column(JSON)
    answers: Mapped[dict] = mapped_column(JSON, default=dict)
    revision: Mapped[int] = mapped_column(Integer, default=0)
    started: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    submitted: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
