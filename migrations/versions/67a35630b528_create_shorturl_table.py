"""Create shorturl table

Revision ID: 67a35630b528
Revises: 
Create Date: 2018-12-11 14:15:30.628670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67a35630b528'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shorturl',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('shortcode', sa.String(length=6), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('lastRedirect', sa.DateTime(), nullable=False),
    sa.Column('redirectCount', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('shortcode')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shorturl')
    # ### end Alembic commands ###
