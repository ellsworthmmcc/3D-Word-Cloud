from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.database import Base


class Article(Base):
    __tablename__ = 'article'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        nullable=False,
    )

    url: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    date_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )
