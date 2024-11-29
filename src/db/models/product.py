from decimal import Decimal

from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, BaseMixin


class Product(Base, BaseMixin):
    name: Mapped[str] = mapped_column()
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    image: Mapped[str] = mapped_column(nullable=True)

    def __str__(self):
        return self.name
