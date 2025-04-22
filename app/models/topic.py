from fastapi import Request
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String
from typing import List

from app.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    games: Mapped[List["Game"]] = relationship(back_populates="topic")
    question: Mapped[List["Question"]] = relationship(back_populates="topic")

    async def __admin_repr__(self, request: Request):
        return self.name