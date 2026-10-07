"""Add the subject dimension.

Every existing question is Logic, so the column is backfilled to 'logic' before
it is made non-nullable. Blueprint rows carry their own subject inside the JSON
and need no schema change.
"""
from alembic import op
import sqlalchemy as s
revision='0002'
down_revision='0001'
branch_labels=None
depends_on=None

def upgrade():
    op.add_column('questions',s.Column('subject',s.String(20),nullable=True))
    op.execute("UPDATE questions SET subject='logic' WHERE subject IS NULL")
    with op.batch_alter_table('questions') as batch:
        batch.alter_column('subject',existing_type=s.String(20),nullable=False)
    op.create_index('ix_questions_subject','questions',['subject'])

def downgrade():
    op.drop_index('ix_questions_subject',table_name='questions')
    op.drop_column('questions','subject')
