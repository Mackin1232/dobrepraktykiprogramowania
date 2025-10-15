from fastapi import FastAPI
import csv

app = FastAPI()


class Movie:
    def __init__(self, movieid: str, title: str, genres: str):
        self.movieid = movieid
        self.title = title
        self.genres = genres


class Link:
    def __init__(self, movieId: str, imdbId: str, tmdbId: str):
        self.movieId = movieId
        self.imdbId = imdbId
        self.tmbdbId = tmdbId


class Rating:
    def __init__(self, userId, movieId, rating, timestamp):
        self.userId = userId
        self.movieId = movieId
        self.rating = rating
        self.timestamp = timestamp


class Tag:
    def __init__(self,userId, movieId, tag, timestamp):
        self.userId = userId
        self.movieId = movieId
        self.tag = tag
        self.timestamp = timestamp


@app.get("/")
def hello_world():
    return {'hello': 'world'}


@app.get("/movies")
def return_movies():
    movie_list = list()
    with open("movies.csv", "r", encoding="utf8") as file:
        next(file)
        for line in csv.reader(file, skipinitialspace=True):
            movie_dict = Movie(line[0], line[1], line[2]).__dict__
            movie_list.append(movie_dict)
    file.close()
    return movie_list


@app.get("/links")
def return_links():
    links_list = list()
    with open("links.csv", "r", encoding="utf8") as file:
        next(file)
        for line in csv.reader(file, skipinitialspace=True):
            link_dict = Link(line[0], line[1], line[2]).__dict__
            links_list.append(link_dict)
    file.close()
    return links_list


@app.get("/ratings")
def return_ratings():
    ratings_list = list()
    with open("ratings.csv", "r", encoding="utf8") as file:
        next(file)
        for line in csv.reader(file, skipinitialspace=True):
            rating_dict = Rating(line[0], line[1], line[2], line[3]).__dict__
            ratings_list.append(rating_dict)
    file.close()
    return ratings_list


@app.get("/tags")
def return_tags():
    tags_list = list()
    with open("tags.csv", "r", encoding="utf8") as file:
        next(file)
        for line in csv.reader(file, skipinitialspace=True):
            tag_dict = Tag(line[0], line[1], line[2], line[3]).__dict__
            tags_list.append(tag_dict)
    file.close()
    return tags_list

