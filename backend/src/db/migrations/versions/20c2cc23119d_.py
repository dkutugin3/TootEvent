"""empty message

Revision ID: 20c2cc23119d
Revises: 023520e24b5b
Create Date: 2024-04-19 22:04:03.562302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20c2cc23119d'
down_revision: Union[str, None] = '023520e24b5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('genre', sa.JSON(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('location', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('preferences', sa.JSON(), nullable=True),
    sa.Column('is_moderator', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('number_of_tickets', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['events.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bookings')
    op.drop_table('users')
    op.drop_table('events')
    # ### end Alembic commands ###