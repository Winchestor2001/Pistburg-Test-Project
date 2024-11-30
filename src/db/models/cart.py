from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base, BaseMixin

if TYPE_CHECKING:
    from src.db import User, Product


class Cart(Base, BaseMixin):
    quantity: Mapped[int] = mapped_column()

    product_id: Mapped[str] = mapped_column(ForeignKey('products.uuid'))
    user_id: Mapped[str] = mapped_column(ForeignKey('users.uuid'))

    product: Mapped['Product'] = relationship(back_populates='cart')
    user: Mapped['User'] = relationship(back_populates='cart')

    def __str__(self):
        return self.uuid
