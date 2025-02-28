import pymongo
from pymongo import MongoClient

MONGO_HOST = "172.31.91.223"
MONGO_PORT = 27017
MONGO_DB = "movies_db"

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]

movies = db["movies"]

movies.insert_many([
  {
    "title": "Batman",
    "category": [
      "action",
      "adventure"
    ],
    "imdb_rating": 7.6,
    "budget": 35,
    "revenue": 70,
    "roten_tomatoes": 7.1
  },
  {
    "title": "Godzilla",
    "category": [
      "action",
      "adventure",
      "sci-fi"
    ],
    "imdb_rating": 6.6,
    "budget": 70,
    "revenue": 20,
    "roten_tomatoes": 8
  },
  {
    "title": "Home Alone",
    "category": [
      "family",
      "comedy"
    ],
    "imdb_rating": 7.4,
    "budget": 10,
    "revenue": 15,
    "roten_tomatoes": 6.3
  },
  {
    "title": "Avengers",
    "category": [
      "action",
      "adventure",
      "sci-fi"
    ],
    "imdb_rating": 8.0,
    "budget": 20,
    "revenue": 30,
    "roten_tomatoes": 8.2
  },
  {
    "title": "James Bond",
    "category": [
      "action",
      "drama"
    ],
    "imdb_rating": 7.4,
    "budget": 13,
    "revenue": 15,
    "roten_tomatoes": 7.2
  }
])