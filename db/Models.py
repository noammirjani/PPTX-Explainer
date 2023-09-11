import os

from typing import List
from sqlalchemy import ForeignKey, String, create_engine, Integer, DateTime
from sqlalchemy.orm import Mapped, relationship, declarative_base, mapped_column, validates
from uuid import UUID
from constants import DB_PATH

Base = declarative_base()


class User(Base):
    __tablename__ = "user_data"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    uploads: Mapped[List["Upload"]] = relationship(
        "Upload", back_populates="user", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"


class Upload(Base):
    __tablename__ = "uploads"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uid: Mapped[UUID] = mapped_column(unique=True, as_uuid=True, nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    upload_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    finish_time: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_data.id"), nullable=True)
    user: Mapped[User] = relationship(back_populates="uploads")

    def __str__(self) -> str:
        return f"Upload(id={self.id!r}, uid={self.uid!r}, filename={self.filename!r}, upload_time={self.upload_time!r}, finish_time={self.finish_time!r}, status={self.status!r}, user_id={self.user_id!r})"


def create_app():
    engine = get_engine()
    Base.metadata.create_all(engine)


def get_engine():
    return create_engine(f"sqlite:///{DB_PATH}", echo=True, future=True)


if __name__ == '__main__':
    create_app()
