from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.database import Base


class Article(Base):
    __tablename__ = 'articles'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        nullable=False,
    )

    url: Mapped[str] = mapped_column(
        String(2000),
        unique=True,
        nullable=False,
    )

    article_analysis: Mapped[dict[str, float]] = mapped_column(
        type_=JSON,
        nullable=False
    )

    date_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    date_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
