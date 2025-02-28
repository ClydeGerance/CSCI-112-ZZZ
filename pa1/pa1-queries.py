import pymongo
from pymongo import MongoClient

MONGO_HOST = "172.31.91.223"
MONGO_PORT = 27017
MONGO_DB = "movies_db"

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]

movies = db["movies"]

# 1. Find all movies with imdb_rating higher than 7.5 or roten_tomatoes rating higher than 6.0
query1 = {"$or": [{"imdb_rating": {"$gt": 7.5}}, {"roten_tomatoes": {"$gt": 6.0}}]}
result1 = list(movies.find(query1))
print("Movies with IMDb rating > 7.5 or Rotten Tomatoes rating > 6.0:")
for movie in result1:
    print(movie["title"])

# 2. Find all movies where category includes drama or action
query2 = {"category": {"$in": ["drama", "action"]}}
result2 = list(movies.find(query2))
print("\nMovies in the Drama or Action category:")
for movie in result2:
    print(movie["title"])

# 3. Find the top movie based on revenue
query3 = movies.find_one(sort=[("revenue", -1)])
print("\nTop movie based on revenue:")
print(query3["title"])