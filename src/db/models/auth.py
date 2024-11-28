import random

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger

from src.db.base import Base, BaseMixin


class User(Base, BaseMixin):
    full_name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(unique=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    password: Mapped[bytes] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(default="user")
    verification_code: Mapped[str] = mapped_column(nullable=True)

    def __str__(self):
        return self.username

    def generate_verification_code(self):
        # self.verification_code = str(random.randint(1000, 9999))
        self.verification_code = "1111"
