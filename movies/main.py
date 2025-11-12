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
from auth.dependencies import verify_token
from fastapi.testclient import TestClient
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
        raise HTTPException(status_code=401, detail="Empty username")
    if data.password is None:
        raise HTTPException(status_code=401, detail="Empty password")
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








'''
client = TestClient(app)
def test_post():
    # test utworzenia bd users
    data = {
        "username": "admin",
        "password": "admin123",
    }
    response = client.post("/login", json=data)
    print(response.json())
    
    # test dodania użytkownika - poprawnie
    data = {
        "username": "Mackin",
        "password": "123",
    }
    response = client.post("/users", json=data,headers={"Authorization": f"Bearer {response.json()['access_token']}"})
    print(response.json())
    

    # test dodania użytkownika - niepoprawnie
    data = {
        "username": "Mackin",
        "password": "123",
    }
    response_token = client.post("/login", json=data)
    data = {
        "username": "test",
        "password": "1234"
    }
    response = client.post("/users", json=data,headers={"Authorization": f"Bearer {response_token.json()['access_token']}"})
    print(response.json())


    # test autoryzacji loginu
    data = {
        "username": "admin",
        "password": "admin123",
    }
    response_token = client.post("/login", json=data)
    if "access_token" in response_token.json().keys():
        response = client.get("/", headers={"Authorization": f"Bearer {response_token.json()['access_token']}"})
        print(response.json()) # zwraca hello world
    else:
        print(response_token.json())

    ## dla złego hasła
    data = {
        "username": "Mackin",
        "password": "1234"
    }
    response_token = client.post("/login", json=data)
    if "access_token" in response_token.json().keys():
        response = client.get("/", headers={"Authorization": f"Bearer {response_token.json()['access_token']}"})
        print(response.json())
    else:
        print(response_token.json()) # invalid credentials
    
    # user details
    data = {
        "username": "admin",
        "password": "admin123",
    }
    response_token = client.post("/login", json=data)
    response = client.get("/user_details", headers={"Authorization": f"Bearer {response_token.json()['access_token'] }"})
    print(response.json())



test_post()
'''