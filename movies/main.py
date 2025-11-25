from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from models.db_init import engine, SessionLocal, Base
from models.movie import Movie, newMovie
from models.link import Link, newLink
from models.rating import Rating, newRating
from models.tag import Tag, newTag
from models.user import User
from load_data import init_data
from auth.create_token import LoginData, login
from auth.login_token import verify_token

import bcrypt

#Base.metadata.drop_all(bind=engine)
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

@app.get("/")
def hello(user: dict = Depends(verify_token)):
    return {"hello": "world"}

@app.get("/movies/")
def get_movies(db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    #movies = db.scalars(select(Movie).where(Movie.movieId.in_([1,2,3,4,5]))).unique().all()
    movies = db.scalars(select(Movie)).unique().all()
    return [m.to_dict() for m in movies]

@app.post("/movies")
def post_movie(newmovie: newMovie, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    if user["role"] != "ROLE_ADMIN":
        raise HTTPException(status_code=401, detail="Access denied")
    if newmovie.movieId is not None:
        movie = Movie(movieId=newmovie.movieId,title=newmovie.title ,genres=newmovie.genres)
    else:
        movie = Movie(title=newmovie.title ,genres=newmovie.genres)
    db.add(movie)
    db.commit()
    return {"detail": f"Added movie {newmovie.title}"}

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    movie = db.scalar(select(Movie).where(Movie.movieId == movie_id))
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie.to_dict()
     
@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie_details: newMovie, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    if user["role"] != "ROLE_ADMIN":
        raise HTTPException(status_code=401, detail="Access denied")
    movie = db.scalar(select(Movie).where(Movie.movieId == movie_id))
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie_details.movieId is not None:
        movie.movieId = movie_details.movieId
    if movie_details.title is not None:
        movie.title = movie_details.title
    if movie_details.genres is not None:
        movie.genres = movie_details.genres
    db.commit()
    db.refresh(movie)
    return {"detail": f"Updated movie {movie_id}"}

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    if user["role"] != "ROLE_ADMIN":
        raise HTTPException(status_code=401, detail="Access denied")
    movie = db.scalar(select(Movie).where(Movie.movieId == movie_id))
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return {"detail": f"Deleted movie {movie_id}"}



@app.get("/links/")
def get_links(db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    links = db.scalars(select(Link)).unique().all()
    return [l.to_dict() for l in links]


@app.get("/ratings/")
def get_ratings(db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    ratings = db.scalars(select(Rating)).all()
    return [r.to_dict() for r in ratings]


@app.get("/tags/")
def get_tags(db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    tags = db.scalars(select(Tag)).all()
    return [t.to_dict() for t in tags]

@app.get("/userlist")
def get_users(db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    users = db.scalars(select(User)).all()
    return [u.to_dict() for u in users]

@app.post("/login")
def post_login(data: LoginData, db: Session = Depends(get_db)):
    user = db.scalars(select(User).where(User.username.like(data.username))).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        return login(user, data.password)
    
@app.post("/users")
def add_user(data: LoginData, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    if user["role"] != "ROLE_ADMIN":
        raise HTTPException(status_code=401, detail="Access denied")
    if data.username is None:
        raise HTTPException(status_code=404, detail="Empty username")
    if data.password is None:
        raise HTTPException(status_code=404, detail="Empty password")
    if db.scalars(select(User).where(User.username.like(data.username))).first() is not None:
        raise HTTPException(status_code=401, detail="User already exists")
    user = User(username=data.username, password=bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()))
    session.add(user)
    session.commit()
    return {"detail": "Added user"}

@app.get("/user_details")
def get_user_details(db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    user_db = db.scalars(select(User).where(User.username.like(user["username"]))).first()
    return user_db.to_dict()


