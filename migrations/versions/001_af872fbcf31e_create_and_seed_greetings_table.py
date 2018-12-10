"""create and seed greetings table

Revision ID: af872fbcf31e
Revises: 
Create Date: 2018-12-07 12:33:39.481767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af872fbcf31e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    greeting = op.create_table('greeting',
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('text', sa.String(), nullable=True),
    )
    op.bulk_insert(greeting,
        [{'text': 'Hello from database!'}])

def downgrade():
    op.drop_table('greeting')
