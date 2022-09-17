"""empty message

Revision ID: 78a2c75f7d4f
Revises: a762cbd34380
Create Date: 2022-09-16 18:52:53.003142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78a2c75f7d4f'
down_revision = 'a762cbd34380'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('live_service_call', sa.Column('energy', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('live_service_call', 'energy')
    # ### end Alembic commands ###
