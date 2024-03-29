"""empty message

Revision ID: fa6cc75e6bc1
Revises: 7ecfa3632f0f
Create Date: 2022-06-18 16:22:05.656740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa6cc75e6bc1'
down_revision = '7ecfa3632f0f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('live_service_call',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('time_delta', sa.Float(), nullable=True),
    sa.Column('service_instance', sa.String(length=100), nullable=True),
    sa.Column('service_type', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('live_service_status',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('cpu_perc', sa.Float(), nullable=True),
    sa.Column('service_instance', sa.String(length=100), nullable=True),
    sa.Column('service_type', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('live_service_status')
    op.drop_table('live_service_call')
    # ### end Alembic commands ###
