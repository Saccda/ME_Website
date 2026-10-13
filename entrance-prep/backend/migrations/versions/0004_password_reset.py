"""Store the one-time codes that let someone reset a forgotten password.

Codes are kept hashed and single-use, with an attempt counter, because six
digits is a small space to guess at. Nothing is backfilled: before this table
existed nobody could reset anything.
"""
from alembic import op
import sqlalchemy as s
revision='0004'
down_revision='0003'
branch_labels=None
depends_on=None

def upgrade():
    op.create_table('password_resets',
        s.Column('id',s.String(36),primary_key=True),
        s.Column('user_id',s.String(36),s.ForeignKey('users.id'),nullable=False),
        s.Column('code_hash',s.String(64),nullable=False),
        s.Column('expires',s.DateTime(timezone=True),nullable=False),
        s.Column('used',s.Boolean(),nullable=False,server_default=s.false()),
        s.Column('attempts',s.Integer(),nullable=False,server_default='0'),
        s.Column('created',s.DateTime(timezone=True),nullable=False))
    op.create_index('ix_password_resets_user_id','password_resets',['user_id'])

def downgrade():
    op.drop_index('ix_password_resets_user_id',table_name='password_resets')
    op.drop_table('password_resets')
