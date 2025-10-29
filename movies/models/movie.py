from typing import List, Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.db_init import Base

class Movie(Base):
    __tablename__ = "movies"

    movieId: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    genres: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    #links: Mapped[List["Link"]] = relationship(back_populates="movie", cascade="all, delete-orphan")
    #ratings: Mapped[List["Rating"]] = relationship(back_populates="movie", cascade="all, delete-orphan")
    #tags: Mapped[List["Tag"]] = relationship(back_populates="movie", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "movieId": self.movieId,
            "title": self.title,
            "genres": self.genres
            #"links": [l.to_dict() for l in self.links],
            #"ratings": [r.to_dict() for r in self.ratings],
            #"tags": [t.to_dict() for t in self.tags],
        }
