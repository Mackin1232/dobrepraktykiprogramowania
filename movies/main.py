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


@app.post("/links/")
def post_link(newlink: newLink, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    if user["role"] != "ROLE_ADMIN":
        raise HTTPException(status_code=401, detail="Access denied")
    if newlink.linkId is not None:
        link = Link(linkId=newlink.linkId, movieId=newlink.movieId, imdbId=newlink.imdbId, tmdbId=newlink.tmdbId)
    else:
        link = Link(movieId=newlink.movieId, imdbId=newlink.imdbId, tmdbId=newlink.tmdbId)
    db.add(link)
    db.commit()
    return {"detail": f"Added link for movie {newlink.movieId}"}


@app.get("/links/{link_id}")
def get_link(link_id: int, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    link = db.scalar(select(Link).where(Link.linkId == link_id))
    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return link.to_dict()


@app.put("/links/{link_id}")
def update_link(link_id: int, link_details: newLink, db: Session = Depends(get_db),
                 user: dict = Depends(verify_token)):
    if user["role"] != "ROLE_ADMIN":
        raise HTTPException(status_code=401, detail="Access denied")
    link = db.scalar(select(Link).where(Link.linkId == link_id))
    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")

    if link_details.linkId is not None:
        link.linkId = link_details.linkId
    if link_details.movieId is not None:
        link.movieId = link_details.movieId
    if link_details.imdbId is not None:
        link.imdbId = link_details.imdbId
    if link_details.tmdbId is not None:
        link.tmdbId = link_details.tmdbId
    db.commit()
    db.refresh(link)
    return {"detail": f"Updated link {link_id}"}


@app.delete("/links/{link_id}")
def delete_link(link_id: int, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    if user["role"] != "ROLE_ADMIN":
        raise HTTPException(status_code=401, detail="Access denied")
    link = db.scalar(select(Link).where(Link.linkId == link_id))
    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    db.delete(link)
    db.commit()
    return {"detail": f"Deleted link {link_id}"}


@app.get("/ratings/")
def get_ratings(db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    ratings = db.scalars(select(Rating)).all()
    return [r.to_dict() for r in ratings]

@app.post("/ratings/")
def post_rating(newrating: newRating, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    if user["role"] != "ROLE_ADMIN":
        raise HTTPException(status_code=401, detail="Access denied")
    if newrating.ratingId is not None:
        rating = Rating(ratingId=newrating.ratingId, userId=newrating.userId, movieId=newrating.movieId, rating=newrating.rating, timestamp=newrating.timestamp)
    else:
        rating = Rating(userId=newrating.userId, movieId=newrating.movieId, rating=newrating.rating, timestamp=newrating.timestamp)
    db.add(rating)
    db.commit()
    return {"detail": f"Added rating for movie {newrating.movieId}"}


@app.get("/ratings/{rating_id}")
def get_rating(rating_id: int, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    rating = db.scalar(select(Rating).where(Rating.ratingId == rating_id))
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating.to_dict()


@app.put("/ratings/{rating_id}")
def update_rating(rating_id: int, rating_details: newRating, db: Session = Depends(get_db),
                 user: dict = Depends(verify_token)):
    if user["role"] != "ROLE_ADMIN":
        raise HTTPException(status_code=401, detail="Access denied")
    rating = db.scalar(select(Rating).where(Rating.ratingId == rating_id))
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")

    if rating_details.ratingId is not None:
        rating.ratingId = rating_details.ratingId
    if rating_details.userId is not None:
        rating.userId = rating_details.userId
    if rating_details.movieId is not None:
        rating.movieId = rating_details.movieId
    if rating_details.rating is not None:
        rating.rating = rating_details.rating
    if rating_details.timestamp is not None:
        rating.timestamp = rating_details.timestamp
    db.commit()
    db.refresh(rating)
    return {"detail": f"Updated rating {rating_id}"}


@app.delete("/ratings/{rating_id}")
def delete_rating(rating_id: int, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    if user["role"] != "ROLE_ADMIN":
        raise HTTPException(status_code=401, detail="Access denied")
    rating = db.scalar(select(Rating).where(Rating.ratingId == rating_id))
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    db.delete(rating)
    db.commit()
    return {"detail": f"Deleted rating {rating_id}"}


@app.get("/tags/")
def get_tags(db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    tags = db.scalars(select(Tag)).all()
    return [t.to_dict() for t in tags]

@app.post("/tags/")
def post_tag(newtag: newTag, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    if user["role"] != "ROLE_ADMIN":
        raise HTTPException(status_code=401, detail="Access denied")
    if newtag.tagId is not None:
        tag = Tag(tagId=newtag.tagId, userId=newtag.userId, movieId=newtag.movieId, tag=newtag.tag, timestamp=newtag.timestamp)
    else:
        tag = Tag(userId=newtag.userId, movieId=newtag.movieId, tag=newtag.tag, timestamp=newtag.timestamp)
    db.add(tag)
    db.commit()
    return {"detail": f"Added tag for movie {newtag.movieId}"}


@app.get("/tags/{tag_id}")
def get_tag(tag_id: int, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    tag = db.scalar(select(Tag).where(Tag.tagId == tag_id))
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag.to_dict()


@app.put("/tag/{tag_id}")
def update_movie(tag_id: int, tag_details: newTag, db: Session = Depends(get_db),
                 user: dict = Depends(verify_token)):
    if user["role"] != "ROLE_ADMIN":
        raise HTTPException(status_code=401, detail="Access denied")
    tag = db.scalar(select(Tag).where(Tag.tagId == tag_id))
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    if tag_details.tagId is not None:
        tag.tagId = tag_details.tagId
    if tag_details.userId is not None:
        tag.userId = tag_details.userId
    if tag_details.movieId is not None:
        tag.movieId = tag_details.movieId
    if tag_details.tag is not None:
        tag.tag = tag_details.tag
    if tag_details.timestamp is not None:
        tag.timestamp = tag_details.timestamp
    db.commit()
    db.refresh(tag)
    return {"detail": f"Updated tag {tag_id}"}


@app.delete("/tag/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    if user["role"] != "ROLE_ADMIN":
        raise HTTPException(status_code=401, detail="Access denied")
    tag = db.scalar(select(Tag).where(Tag.tagId == tag_id))
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(tag)
    db.commit()
    return {"detail": f"Deleted tag {tag_id}"}

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


