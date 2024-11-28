"""create models

Revision ID: 6a29328a63ab
Revises: 7fbabd5bb0f9
Create Date: 2024-11-28 17:51:27.425717

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6a29328a63ab"
down_revision: Union[str, None] = "7fbabd5bb0f9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("role", sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "role")
    # ### end Alembic commands ###