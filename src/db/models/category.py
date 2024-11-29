from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, BaseMixin


class Category(Base, BaseMixin):
    name: Mapped[str] = mapped_column()

    def __str__(self):
        return self.name
