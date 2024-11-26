from __future__ import annotations

from sqlalchemy import (
    String
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from app.models.base import Base


class Pizza(Base):
    __tablename__ = "pizza"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(240), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(String(240), nullable=True)

    def __str__(self):
        return self.name.capitalize()