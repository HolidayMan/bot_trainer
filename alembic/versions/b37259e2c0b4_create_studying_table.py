"""create studying table

Revision ID: b37259e2c0b4
Revises: 306683caf906
Create Date: 2019-11-13 14:15:38.014535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b37259e2c0b4'
down_revision = '306683caf906'
branch_labels = None
depends_on = None


def upgrade():
     op.create_table(
        'studying',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('state', sa.Integer),
        sa.Column('user_id', sa.Integer, nullable=False, unique=True),
    )


def downgrade():
    op.drop_table('studying')
