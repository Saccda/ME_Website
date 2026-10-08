"""Initial schema. Cross-database JSON fields hold immutable content snapshots."""
from alembic import op
import sqlalchemy as s
revision='0001'
down_revision=None
branch_labels=None
depends_on=None
def upgrade():
    op.create_table('users',s.Column('id',s.String(36),primary_key=True),s.Column('email',s.String(254),nullable=False,unique=True),s.Column('name',s.String(100),nullable=False),s.Column('password',s.Text,nullable=False),s.Column('role',s.String(20),nullable=False))
    op.create_table('auth_sessions',s.Column('token_hash',s.String(64),primary_key=True),s.Column('user_id',s.String(36),s.ForeignKey('users.id'),nullable=False),s.Column('expires',s.DateTime(timezone=True),nullable=False))
    op.create_table('login_failures',s.Column('id',s.String(36),primary_key=True),s.Column('key',s.String(64),nullable=False),s.Column('created',s.DateTime(timezone=True),nullable=False));op.create_index('ix_login_failures_key','login_failures',['key'])
    op.create_table('questions',s.Column('id',s.String(36),primary_key=True),s.Column('domain',s.String(30),nullable=False),s.Column('skill',s.String(50),nullable=False),s.Column('difficulty',s.String(20),nullable=False),s.Column('status',s.String(20),nullable=False),s.Column('content',s.JSON,nullable=False),s.Column('source',s.JSON,nullable=False),s.Column('validation',s.JSON,nullable=False),s.Column('version',s.Integer,nullable=False),s.Column('created',s.DateTime(timezone=True),nullable=False))
    for name in ('domain','skill','difficulty','status'):op.create_index('ix_questions_'+name,'questions',[name])
    op.create_table('audit_events',s.Column('id',s.String(36),primary_key=True),s.Column('user_id',s.String(36),s.ForeignKey('users.id'),nullable=False),s.Column('entity_id',s.String(36),nullable=False),s.Column('action',s.String(40),nullable=False),s.Column('detail',s.JSON,nullable=False),s.Column('created',s.DateTime(timezone=True),nullable=False));op.create_index('ix_audit_events_entity_id','audit_events',['entity_id'])
    op.create_table('blueprints',s.Column('id',s.String(36),primary_key=True),s.Column('name',s.String(120),nullable=False),s.Column('minutes',s.Integer,nullable=False),s.Column('rows',s.JSON,nullable=False),s.Column('published',s.Boolean,nullable=False),s.Column('creator_id',s.String(36),s.ForeignKey('users.id'),nullable=False))
    op.create_table('attempts',s.Column('id',s.String(36),primary_key=True),s.Column('user_id',s.String(36),s.ForeignKey('users.id'),nullable=False),s.Column('mode',s.String(20),nullable=False),s.Column('title',s.String(120),nullable=False),s.Column('snapshots',s.JSON,nullable=False),s.Column('answers',s.JSON,nullable=False),s.Column('revision',s.Integer,nullable=False),s.Column('started',s.DateTime(timezone=True),nullable=False),s.Column('deadline',s.DateTime(timezone=True)),s.Column('submitted',s.DateTime(timezone=True)));op.create_index('ix_attempts_user_id','attempts',['user_id'])
def downgrade():
    for name in ('attempts','blueprints','audit_events','questions','login_failures','auth_sessions','users'):op.drop_table(name)
