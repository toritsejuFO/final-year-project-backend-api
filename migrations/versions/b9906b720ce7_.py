"""empty message

Revision ID: b9906b720ce7
Revises: 618da61d803b
Create Date: 2019-11-09 17:51:07.487844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9906b720ce7'
down_revision = '618da61d803b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lecturers_lectures_second_2018_2019',
    sa.Column('lecturer_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['lecturer_id'], ['lecturers.id'], ),
    sa.PrimaryKeyConstraint('lecturer_id', 'course_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lecturers_lectures_second_2018_2019')
    # ### end Alembic commands ###