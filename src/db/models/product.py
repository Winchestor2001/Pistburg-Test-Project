from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base, BaseMixin

if TYPE_CHECKING:
    from src.db import Category, Order


class Product(Base, BaseMixin):
    name: Mapped[str] = mapped_column()
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    image: Mapped[str] = mapped_column(nullable=True)

    category_id: Mapped[str] = mapped_column(ForeignKey('categorys.uuid'))
    category: Mapped['Category'] = relationship(back_populates='products')

    orders: Mapped["Order"] = relationship(back_populates="product")

    def __str__(self):
        return self.name
