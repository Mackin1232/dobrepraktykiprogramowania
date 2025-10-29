from typing import List, Optional
from sqlalchemy import String, ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.db_init import Base

class Tag(Base):
    __tablename__ = "tags"

    tagId: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    userId: Mapped[int] = mapped_column(Integer)
    movieId: Mapped[int] = mapped_column(ForeignKey("movies.movieId"))
    tag: Mapped[str] = mapped_column(String)
    timestamp: Mapped[int] = mapped_column(Integer)

    #movie: Mapped[Movie] = relationship(back_populates="tags")

    def to_dict(self):
        return {
            "tagId": self.tagId,
            "userId": self.userId,
            "movieId": self.movieId,
            "tag": self.tag,
            "timestamp": self.timestamp,
        }