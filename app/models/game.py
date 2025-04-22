from fastapi import Request
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, DateTime, Date, Integer, Boolean, ForeignKey

from datetime import datetime
from typing import List

from app.database import Base


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000))
    topic_id: Mapped[int] = mapped_column(Integer, ForeignKey("topics.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="owned_games")
    questions: Mapped[List["GameQuestion"]] = relationship(back_populates="game")
    topic: Mapped["Topic"] = relationship("Topic", back_populates="games")
    submissions: Mapped[List["Submission"]] = relationship("Submission", back_populates="game")
    participations: Mapped[List["Participation"]] = relationship(back_populates="game")

    async def __admin_repr__(self, request: Request):
        return self.title


class GameQuestion(Base):
    __tablename__ = "game_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey("games.id"))
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id"))
    score: Mapped[int] = mapped_column(Integer, default=0)

    question: Mapped["Question"] = relationship(back_populates="games")
    game: Mapped["Game"] = relationship(back_populates="questions")