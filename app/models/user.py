from fastapi import Request
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, DateTime, Date, Integer, Boolean, ForeignKey

from datetime import datetime, date, timezone
from typing import Optional, List

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(String(128))
    username: Mapped[str] = mapped_column(String(32), unique=True)
    first_name: Mapped[str] = mapped_column(String(32), nullable=True)
    last_name: Mapped[str] = mapped_column(String(32), nullable=True)
    birthdate: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    owned_games: Mapped[List["Game"]] = relationship(back_populates="owner")
    submissions: Mapped[List["Submission"]] = relationship(back_populates="owner")
    participations: Mapped[List["Participation"]] = relationship(back_populates="user")

    async def __admin_repr__(self, request: Request):
        return f"{self.last_name} {self.first_name}"

    async def __admin_select2_repr__(self, request: Request) -> str:
        return f'<span><b>{self.first_name} {self.last_name}</b></span>'