"""create models

Revision ID: 25dfdff87b9c
Revises: 82fb74cc343b
Create Date: 2024-11-29 23:17:28.526840

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "25dfdff87b9c"
down_revision: Union[str, None] = "82fb74cc343b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "orders", sa.Column("product_id", sa.String(length=36), nullable=False)
    )
    op.add_column(
        "orders", sa.Column("user_id", sa.String(length=36), nullable=False)
    )
    op.create_foreign_key(
        op.f("fk_orders_product_id_products"),
        "orders",
        "products",
        ["product_id"],
        ["uuid"],
    )
    op.create_foreign_key(
        op.f("fk_orders_user_id_users"),
        "orders",
        "users",
        ["user_id"],
        ["uuid"],
    )
    op.drop_column("orders", "user")
    op.drop_column("orders", "product")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "orders",
        sa.Column(
            "product", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "orders",
        sa.Column("user", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(
        op.f("fk_orders_user_id_users"), "orders", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_orders_product_id_products"), "orders", type_="foreignkey"
    )
    op.drop_column("orders", "user_id")
    op.drop_column("orders", "product_id")
    # ### end Alembic commands ###
