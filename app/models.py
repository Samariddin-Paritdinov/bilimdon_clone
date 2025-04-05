from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, DateTime, Date, ForeignKey, Integer, Text

from typing import Optional
from datetime import datetime, date, timezone, time

from app.database import Base

class User(Base):
    __tablename__="users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(String(128))
    username: Mapped[str] = mapped_column(String(32), unique=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    birth_date: Mapped[date] = mapped_column(Date)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)


class Participation(Base):
    __tablename__ = 'participations'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        type_=Integer,
        nullable=True
    )
    owner: Mapped[Optional["User"]] = relationship("User")
    topic_id: Mapped[int] = mapped_column()
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    game_id: Mapped[int] = mapped_column()
    start_time: Mapped[time]
    eng_time: Mapped[Optional[time]] = mapped_column(nullable=False)
    gained_score: Mapped[int] = mapped_column(default=0)