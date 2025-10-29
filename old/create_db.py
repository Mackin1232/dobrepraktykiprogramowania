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

class Movie(Base):
    __tablename__ = "movies"
    movieId: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    genres: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Movie(movieId={self.movieId!r}, title={self.title!r}, genres={self.genres!r})"


class Link(Base):
    __tablename__ = "links"
    linkId: Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    movieId: Mapped[int] = mapped_column(ForeignKey("movies.movieId"))
    imdbId: Mapped[Optional[str]]
    tmdbId: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Link(linkId={self.linkId}, movieId={self.movieId!r}, imdbId={self.imdbId!r}, tmdbId={self.tmdbId!r})"
'''
class Rating(Base):
    __tablename__ = "ratings"
    userId: Mapped[int]
    movieId: Mapped[str] = mapped_column(ForeignKey("movies.movieId"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"



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
            new_movie = Movie(movieId=line[0],title=line[1],genres=line[2])
            movie_list.append(new_movie)
    file.close()
    session.add_all(movie_list)
    session.commit()

with Session(engine) as session:
    test = select(Movie).where(Movie.movieId.in_([1, 2, 3, 4, 5]))
    for movie in session.scalars(test):
        print(movie)

with Session(engine) as session:
    links_list = list()
    with open("links.csv", "r", encoding="utf8") as file:
        next(file)
        for line in csv.reader(file, skipinitialspace=True):
            new_link = Link(movieId=line[0],imdbId=line[1],tmdbId=line[2])
            links_list.append(new_link)
    file.close()
    session.add_all(links_list)
    session.commit()

with Session(engine) as session:
    test = select(Link).where(Link.movieId.in_([1, 2, 3, 4, 5]))
    for link in session.scalars(test):
        print(link)
