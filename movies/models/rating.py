from typing import List, Optional
from sqlalchemy import String, ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.db_init import Base
from pydantic import BaseModel

class newRating(BaseModel):
    userId: int
    movieId: int
    rating: float

class Rating(Base):
    __tablename__ = "ratings"

    ratingId: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    userId: Mapped[int] = mapped_column(Integer)
    movieId: Mapped[int] = mapped_column(ForeignKey("movies.movieId"))
    rating: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[int] = mapped_column(Integer)

    #movie: Mapped[Movie] = relationship(back_populates="ratings")

    def to_dict(self):
        return {
            "ratingId": self.ratingId,
            "userId": self.userId,
            "movieId": self.movieId,
            "rating": self.rating,
            "timestamp": self.timestamp,
        }
