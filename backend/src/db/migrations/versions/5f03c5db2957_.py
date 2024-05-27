"""empty message

Revision ID: 5f03c5db2957
Revises: 20c2cc23119d
Create Date: 2024-04-19 23:28:42.150805

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5f03c5db2957"
down_revision: Union[str, None] = "20c2cc23119d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tickets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("booking_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["booking_id"],
            ["bookings.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("bookings", sa.Column("is_payed", sa.Boolean(), nullable=False))
    op.alter_column("bookings", "user_id", existing_type=sa.INTEGER(), nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("bookings", "user_id", existing_type=sa.INTEGER(), nullable=True)
    op.drop_column("bookings", "is_payed")
    op.drop_table("tickets")
    # ### end Alembic commands ###
