"""empty message

Revision ID: 2976eef9d9dc
Revises: da777a35f274
Create Date: 2024-04-02 17:55:43.782982

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2976eef9d9dc'
down_revision: Union[str, None] = 'da777a35f274'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
