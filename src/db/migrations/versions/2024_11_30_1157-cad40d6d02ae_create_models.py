"""create models

Revision ID: cad40d6d02ae
Revises: 25dfdff87b9c
Create Date: 2024-11-30 11:57:07.619740

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cad40d6d02ae"
down_revision: Union[str, None] = "25dfdff87b9c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "carts",
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("uuid", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("obj_state", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.uuid"],
            name=op.f("fk_carts_product_id_products"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.uuid"], name=op.f("fk_carts_user_id_users")
        ),
        sa.PrimaryKeyConstraint("uuid", name=op.f("pk_carts")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("carts")
    # ### end Alembic commands ###
