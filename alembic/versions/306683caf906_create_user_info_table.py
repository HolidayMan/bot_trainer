"""create user_info table

Revision ID: 306683caf906
Revises: 
Create Date: 2019-10-05 22:50:45.747356

"""
from alembic import op
import sqlalchemy as sa
from datetime import timezone

# revision identifiers, used by Alembic.
revision = '306683caf906'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_info',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(64), nullable=False, unique=False),
        sa.Column('surname', sa.String(64), nullable=False, unique=False),
        sa.Column('registration_date', sa.DateTime, nullable=True, unique=False),
        sa.Column('age', sa.Integer(), nullable=False, unique=False),
        sa.Column('planning_time', sa.Time(), nullable=False, unique=False),
        sa.Column('question1', sa.String(64), nullable=False, unique=False),
        sa.Column('question2', sa.String(64), nullable=False, unique=False),
        sa.Column('question3', sa.String(64), nullable=False, unique=False),
        sa.Column('question4', sa.String(64), nullable=False, unique=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), nullable=False)
    )


def downgrade():
   op.drop_table('user_info')
