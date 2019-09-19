"""Increase fingerprint template size in db

Revision ID: 0205bd762564
Revises: 7a44a937f5b7
Create Date: 2019-09-19 20:18:12.984658

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0205bd762564'
down_revision = '7a44a937f5b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('fingerprint', sa.String(length=1112), nullable=True))
    op.drop_index('ix_students_fingerprint_template', table_name='students')
    op.create_unique_constraint(None, 'students', ['fingerprint'])
    op.drop_column('students', 'fingerprint_template')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('fingerprint_template', mysql.VARCHAR(length=1112), nullable=True))
    op.drop_constraint(None, 'students', type_='unique')
    op.create_index('ix_students_fingerprint_template', 'students', ['fingerprint_template'], unique=True)
    op.drop_column('students', 'fingerprint')
    # ### end Alembic commands ###