from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.db_init import engine, SessionLocal, Base
from models.movie import Movie
from models.link import Link
from models.rating import Rating
from models.tag import Tag
from models.user import User
from load_data import init_data
from auth.login_auth import LoginData, login
from fastapi.testclient import TestClient

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


with SessionLocal() as session:
    init_data(session)


app = FastAPI()

@app.get("/movies/")
def get_movies(db: Session = Depends(get_db)):
    #movies = db.scalars(select(Movie).where(Movie.movieId.in_([1,2,3,4,5]))).unique().all()
    movies = db.scalars(select(Movie)).unique().all()
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

@app.post("/login")
def post_login(data: LoginData, db: Session = Depends(get_db)):
    user = db.scalars(select(User).where(User.username.like(data.username))).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        return login(user, data.password)


client = TestClient(app)
def test_post():
    data = {
        "username": "admin",
        "password": "admin123"
    }
    response = client.post("/login", json=data)
    print(response.json())


test_post()
#Base.metadata.drop_all(bind=engine)

