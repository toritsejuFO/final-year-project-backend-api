"""Add units to course model

Revision ID: 7a44a937f5b7
Revises: 3e4649d3af3d
Create Date: 2019-09-09 14:14:18.670495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a44a937f5b7'
down_revision = '3e4649d3af3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('courses', sa.Column('units', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('courses', 'units')
    # ### end Alembic commands ###