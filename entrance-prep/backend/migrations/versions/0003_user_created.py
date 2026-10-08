"""Record when an account was created.

Left nullable and not backfilled: accounts that already existed have no true
registration date, and filling one in would misreport when a cohort signed up.
"""
from alembic import op
import sqlalchemy as s
revision='0003'
down_revision='0002'
branch_labels=None
depends_on=None

def upgrade():
    op.add_column('users',s.Column('created',s.DateTime(timezone=True),nullable=True))

def downgrade():
    op.drop_column('users','created')
