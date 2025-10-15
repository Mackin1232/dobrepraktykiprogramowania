from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
import csv

class Base(DeclarativeBase):
    pass

class Movie_db(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    genres: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Movie_db(id={self.id!r}, title={self.title!r}, genres={self.genres!r})"

'''
class Link_db(Base):
    __tablename__ = "links"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
'''

engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)


with Session(engine) as session:
    movie_list = list()
    with open("movies.csv", "r", encoding="utf8") as file:
        next(file)
        for line in csv.reader(file, skipinitialspace=True):
            new_movie = Movie(id=line[0],title=line[1],genres=line[2])
            movie_list.append(new_movie)
    file.close()
    session.add_all(movie_list)
    session.commit()

with Session(engine) as session:
    test = select(Movie).where(Movie.id.in_([1, 2, 3, 4, 5]))
    for movie in session.scalars(test):
        print(movie)