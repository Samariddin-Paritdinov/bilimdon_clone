from fastapi import Request
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, DateTime, Date, Integer, Boolean, ForeignKey

from datetime import datetime, date, timezone
from typing import Optional, List

from app.database import Base



class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey("games.id"))
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id"))
    option_id: Mapped[int] = mapped_column(Integer, ForeignKey("options.id"))
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    owner = relationship("User", back_populates="submissions")
    question = relationship("Question", back_populates="submissions")
    option = relationship("Option", back_populates="submissions")
    game = relationship("Game", back_populates="submissions")

    async def __admin_repr__(self, request: Request ):
        return f"Submission of user with id={self.id}"