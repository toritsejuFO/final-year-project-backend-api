"""empty message

Revision ID: eee31a5bf1a6
Revises: b9906b720ce7
Create Date: 2019-11-09 17:54:02.008390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eee31a5bf1a6'
down_revision = 'b9906b720ce7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lecturers_lectures_second_2018_2019', sa.Column('count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lecturers_lectures_second_2018_2019', 'count')
    # ### end Alembic commands ###