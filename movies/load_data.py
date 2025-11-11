import csv
from sqlalchemy.orm import Session
from models.movie import Movie
from models.link import Link
from models.rating import Rating
from models.tag import Tag
from models.user import User
import bcrypt


def init_data(session: Session):
    if session.query(Movie).count() == 0:
        try:
            with open("models/data/movies.csv", "r", encoding="utf8") as file:
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
            with open("models/data/links.csv", "r", encoding="utf8") as file:
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
            with open("models/data/ratings.csv", "r", encoding="utf8") as file:
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
            with open("models/data/tags.csv", "r", encoding="utf8") as file:
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

    if session.query(User).count() == 0:
        admin = User(username="admin", password=bcrypt.hashpw(b"admin123", bcrypt.gensalt()), role="ROLE_ADMIN")
        session.add(admin)
        session.commit()
        print("Loaded users")
