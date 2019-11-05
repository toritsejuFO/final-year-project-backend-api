"""empty message

Revision ID: 922f6d22518b
Revises: 5d948e7cfff4
Create Date: 2019-11-05 23:23:36.616108

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '922f6d22518b'
down_revision = '5d948e7cfff4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assigned_courses_second_2018_2019',
    sa.Column('lecturer_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['lecturer_id'], ['lecturers.id'], ),
    sa.PrimaryKeyConstraint('lecturer_id', 'course_id')
    )
    op.create_table('students_exam_second_2018_2019',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('student_id', 'course_id')
    )
    op.drop_table('assgined_courses_second_2018_2019')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assgined_courses_second_2018_2019',
    sa.Column('lecturer_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('course_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], name='assgined_courses_second_2018_2019_ibfk_1'),
    sa.ForeignKeyConstraint(['lecturer_id'], ['lecturers.id'], name='assgined_courses_second_2018_2019_ibfk_2'),
    sa.PrimaryKeyConstraint('lecturer_id', 'course_id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.drop_table('students_exam_second_2018_2019')
    op.drop_table('assigned_courses_second_2018_2019')
    # ### end Alembic commands ###
