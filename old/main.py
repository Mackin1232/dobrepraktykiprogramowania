# main.py
from typing import List, Optional
import csv
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, String, ForeignKey, Float, Integer, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, Session


SQLALCHEMY_DATABASE_URL = "sqlite:///./movies.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class Movie(Base):
    __tablename__ = "movies"

    movieId: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    genres: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    links: Mapped[List["Link"]] = relationship(back_populates="movie", cascade="all, delete-orphan")
    ratings: Mapped[List["Rating"]] = relationship(back_populates="movie", cascade="all, delete-orphan")
    tags: Mapped[List["Tag"]] = relationship(back_populates="movie", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "movieId": self.movieId,
            "title": self.title,
            "genres": self.genres,
            "links": [l.to_dict() for l in self.links],
            "ratings": [r.to_dict() for r in self.ratings],
            "tags": [t.to_dict() for t in self.tags],
        }


class Link(Base):
    __tablename__ = "links"

    linkId: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    movieId: Mapped[int] = mapped_column(ForeignKey("movies.movieId"))
    imdbId: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    tmdbId: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    movie: Mapped[Movie] = relationship(back_populates="links")

    def to_dict(self):
        return {
            "linkId": self.linkId,
            "movieId": self.movieId,
            "imdbId": self.imdbId,
            "tmdbId": self.tmdbId,
        }


class Rating(Base):
    __tablename__ = "ratings"

    ratingId: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    userId: Mapped[int] = mapped_column(Integer)
    movieId: Mapped[int] = mapped_column(ForeignKey("movies.movieId"))
    rating: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[int] = mapped_column(Integer)

    movie: Mapped[Movie] = relationship(back_populates="ratings")

    def to_dict(self):
        return {
            "ratingId": self.ratingId,
            "userId": self.userId,
            "movieId": self.movieId,
            "rating": self.rating,
            "timestamp": self.timestamp,
        }


class Tag(Base):
    __tablename__ = "tags"

    tagId: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    userId: Mapped[int] = mapped_column(Integer)
    movieId: Mapped[int] = mapped_column(ForeignKey("movies.movieId"))
    tag: Mapped[str] = mapped_column(String)
    timestamp: Mapped[int] = mapped_column(Integer)

    movie: Mapped[Movie] = relationship(back_populates="tags")

    def to_dict(self):
        return {
            "tagId": self.tagId,
            "userId": self.userId,
            "movieId": self.movieId,
            "tag": self.tag,
            "timestamp": self.timestamp,
        }


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def init_data():
    with Session(engine) as session:
        if session.query(Movie).count() == 0:
            try:
                with open("movies.csv", "r", encoding="utf8") as file:
                    next(file)
                    reader = csv.reader(file)
                    movies = [Movie(movieId=int(r[0]), title=r[1], genres=r[2]) for r in reader]
                session.add_all(movies)
                session.commit()
                print("Loaded movies.csv")
            except FileNotFoundError:
                print("movies.csv not found.")

        if session.query(Link).count() == 0:
            try:
                with open("links.csv", "r", encoding="utf8") as file:
                    next(file)
                    reader = csv.reader(file)
                    links = [
                        Link(movieId=int(r[0]), imdbId=r[1] or None, tmdbId=r[2] or None)
                        for r in reader
                    ]
                session.add_all(links)
                session.commit()
                print("Loaded links.csv")
            except FileNotFoundError:
                print("links.csv not found.")

        if session.query(Rating).count() == 0:
            try:
                with open("ratings.csv", "r", encoding="utf8") as file:
                    next(file)
                    reader = csv.reader(file)
                    ratings = [
                        Rating(userId=int(r[0]), movieId=int(r[1]), rating=float(r[2]), timestamp=int(r[3]))
                        for r in reader
                    ]
                session.add_all(ratings)
                session.commit()
                print("Loaded ratings.csv")
            except FileNotFoundError:
                print("ratings.csv not found.")

        if session.query(Tag).count() == 0:
            try:
                with open("tags.csv", "r", encoding="utf8") as file:
                    next(file)
                    reader = csv.reader(file)
                    tags = [
                        Tag(userId=int(r[0]), movieId=int(r[1]), tag=r[2], timestamp=int(r[3]))
                        for r in reader
                    ]
                session.add_all(tags)
                session.commit()
                print("Loaded tags.csv")
            except FileNotFoundError:
                print("tags.csv not found.")

init_data()


app = FastAPI()

@app.get("/movies/")
def get_movies(db: Session = Depends(get_db)):
    movies = db.scalars(select(Movie).where(Movie.movieId.in_([1,2,3,4,5]))).unique().all()
    return [m.to_dict() for m in movies]

@app.get("/links/")
def get_links(db: Session = Depends(get_db)):
    links = db.scalars(select(Link)).unique().all()
    return [l.to_dict() for l in links]


@app.get("/ratings/")
def get_ratings(db: Session = Depends(get_db)):
    ratings = db.scalars(select(Rating)).all()
    return [r.to_dict() for r in ratings]


@app.get("/tags/")
def get_tags(db: Session = Depends(get_db)):
    tags = db.scalars(select(Tag)).all()
    return [t.to_dict() for t in tags]


