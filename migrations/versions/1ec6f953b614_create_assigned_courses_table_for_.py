"""Create assigned courses table for second_18

Revision ID: 1ec6f953b614
Revises: cf0b68ddc7de
Create Date: 2019-08-21 17:18:46.932155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ec6f953b614'
down_revision = 'cf0b68ddc7de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assgined_courses_second_2018_2018',
    sa.Column('lecturer_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['lecturer_id'], ['lecturers.id'], ),
    sa.PrimaryKeyConstraint('lecturer_id', 'course_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('assgined_courses_second_2018_2018')
    # ### end Alembic commands ###
