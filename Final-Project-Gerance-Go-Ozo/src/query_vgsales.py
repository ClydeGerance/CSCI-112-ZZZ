import pymongo
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('172.31.91.223', 27017)
db = client['video_game_db']
collection = db['games']

# 1. Top 10 Best Selling Platforms Globally
cursor1 = collection.aggregate([
    {
        "$group": {
            "_id": "$platform",
            "global_sales": {"$sum": "$sales.global"}
        }
    },
    {"$sort": {"global_sales": -1}},
    {"$limit": 10}
])
print("\nTop 10 Best Selling Platforms Globally")
for doc in cursor1:
    pprint(doc)

# 2. Top 10 Best Selling Publishers Globally
cursor2 = collection.aggregate([
    {
        "$group": {
            "_id": "$publisher",
            "global_sales": {"$sum": "$sales.global"}
        }
    },
    {"$sort": {"global_sales": -1}},
    {"$limit": 10}
])
print("\nTop 10 Best Selling Publishers Globally")
for doc in cursor2:
    pprint(doc)

# 3. Best-Selling Game per ESRB Rating
cursor3 = collection.aggregate([
    {
        "$match": {
            "ratings.esrb_rating": {"$ne": None},
            "sales.global": {"$ne": None}
        }
    },
    {
        "$sort": {
            "ratings.esrb_rating": 1,
            "sales.global": -1
        }
    },
    {
        "$group": {
            "_id": "$ratings.esrb_rating",
            "topGame": {"$first": "$name"},
            "platform": {"$first": "$platform"},
            "globalSales": {"$first": "$sales.global"},
            "criticScore": {"$first": "$ratings.critic_score"},
            "userScore": {"$first": "$ratings.user_score"}
        }
    },
    {"$sort": {"globalSales": -1}}
])
print("\nBest-Selling Game per ESRB Rating")
for doc in cursor3:
    pprint(doc)

# 4. Average Critic Score vs User Score by Genre (minimum 5 games)
cursor4 = collection.aggregate([
    {
        "$match": {
            "ratings.critic_score": {"$ne": None},
            "ratings.user_score": {"$ne": None},
            "genre": {"$ne": None}
        }
    },
    {
        "$group": {
            "_id": "$genre",
            "avgCriticScore": {"$avg": "$ratings.critic_score"},
            "avgUserScore": {"$avg": "$ratings.user_score"},
            "gameCount": {"$sum": 1}
        }
    },
    {
        "$match": {"gameCount": {"$gte": 5}}
    },
    {"$sort": {"avgCriticScore": -1}}
])
print("\nAverage Critic Score vs User Score by Genre (min 5 games)")
for doc in cursor4:
    pprint(doc)

# 5. Best-Selling Video Game Each Year in Terms of Global Sales
cursor5 = collection.aggregate([
    {
        "$match": {"year_of_release": {"$ne": "null"}}
    },
    {
        "$sort": {"year_of_release": 1, "sales.global": -1}
    },
    {
        "$group": {
            "_id": "$year_of_release",
            "game": {"$first": "$name"},
            "overall_sales": {"$first": "$sales.global"}
        }
    },
    {
        "$project": {
            "_id": 0,
            "year": "$_id",
            "game": 1,
            "overall_sales": 1
        }
    },
    {"$sort": {"year": -1}}
])
print("\nBest-Selling Video Game Each Year in Terms of Global Sales")
for doc in cursor5:
    pprint(doc)

# 6. Most Successful Genre per ESRB Rating Based on Average User Score (very complex query)
cursor6 = collection.aggregate([
    {
        "$match": {
            "ratings.esrb_rating": {"$ne": None},
            "ratings.user_score": {"$ne": None},
            "genre": {"$ne": None}
        }
    },
    {
        "$group": {
            "_id": {
                "esrb_rating": "$ratings.esrb_rating",
                "genre": "$genre"
            },
            "avgUserScore": {"$avg": "$ratings.user_score"},
            "countGames": {"$sum": 1},
            "topGame": {"$first": "$name"},
            "topPlatform": {"$first": "$platform"},
            "topUserScore": {"$first": "$ratings.user_score"}
        }
    },
    {
        "$match": {"countGames": {"$gte": 5}}
    },
    {
        "$sort": {
            "_id.esrb_rating": 1,
            "avgUserScore": -1
        }
    },
    {
        "$group": {
            "_id": "$_id.esrb_rating",
            "bestGenre": {"$first": "$_id.genre"},
            "avgUserScore": {"$first": "$avgUserScore"},
            "topGame": {"$first": "$topGame"},
            "topPlatform": {"$first": "$topPlatform"},
            "topUserScore": {"$first": "$topUserScore"}
        }
    },
    {
        "$sort": {"_id": 1}
    }
])
print("\nMost Successful Genre per ESRB Rating Based on Average User Score (min 5 games)")
for doc in cursor6:
    pprint(doc)