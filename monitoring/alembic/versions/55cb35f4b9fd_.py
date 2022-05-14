"""empty message

Revision ID: 55cb35f4b9fd
Revises: fb0bb5a4b6f7
Create Date: 2022-05-12 10:27:25.552883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55cb35f4b9fd'
down_revision = 'fb0bb5a4b6f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workloads',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ts_init', sa.DateTime(), nullable=True),
    sa.Column('ts_end', sa.DateTime(), nullable=True),
    sa.Column('days_count', sa.Integer(), nullable=True),
    sa.Column('day_duration', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('workloads')
    # ### end Alembic commands ###