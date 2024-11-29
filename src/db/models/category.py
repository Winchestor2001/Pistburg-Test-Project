from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, BaseMixin

if TYPE_CHECKING:
    from src.db import Product

class Category(Base, BaseMixin):
    name: Mapped[str] = mapped_column()

    products: Mapped["Product"] = relationship(back_populates="category")

    def __str__(self):
        return self.name
