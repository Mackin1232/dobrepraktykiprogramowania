from typing import List, Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.db_init import Base
from pydantic import BaseModel

class newLink(BaseModel):
    linkId: Optional[int] = None
    movieId: Optional[int] = None
    imdbId: Optional[str] = None
    tmdbId: Optional[str] = None

class Link(Base):
    __tablename__ = "links"

    linkId: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    movieId: Mapped[int] = mapped_column(ForeignKey("movies.movieId"))
    imdbId: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    tmdbId: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    #movie: Mapped[Movie] = relationship(back_populates="links")

    def to_dict(self):
        return {
            "linkId": self.linkId,
            "movieId": self.movieId,
            "imdbId": self.imdbId,
            "tmdbId": self.tmdbId,
        }