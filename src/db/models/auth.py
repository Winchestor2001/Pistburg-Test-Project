from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, BaseMixin

if TYPE_CHECKING:
    from src.db import Order


class User(Base, BaseMixin):
    full_name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(unique=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    password: Mapped[bytes] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(default="user")
    verification_code: Mapped[str] = mapped_column(nullable=True)

    orders: Mapped["Order"] = relationship(back_populates="user")

    def __str__(self):
        return self.username

    def generate_verification_code(self):
        # self.verification_code = str(random.randint(1000, 9999))
        self.verification_code = "1111"
