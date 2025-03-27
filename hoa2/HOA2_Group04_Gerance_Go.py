# Clyde Lester Gerance, 185503
# Paul Jason C Go, 212786
# 
# March 14, 2025

# We certify that this submission complies with the DISCS Academic Integrity
# Policy.

# We have discussed our Python language code with anyone other than
# our instructor, our groupmate, the teaching assistant,
# the extent of each discussion has been clearly noted along with a proper
# citation in the comments of our program.

# If any Python language code or documentation used in my/our program
# was obtained from another source, either modified or unmodified, such as a
# textbook, website, or another individual, the extent of its use has been
# clearly noted along with a proper citation in the comments of my/our program.

################################################################################

#https://www.mongodb.com/developer/languages/python/python-quickstart-aggregation/

################################################################################

import pymongo
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('172.31.89.104',27017)
db = client['sample']
posts = db['posts']
inspections = db['inspections']
stories = db['stories']
tweets = db['tweets']
movies = db['movies']


pipeline1 =[
    {"$unwind": "$tags"},  
    {"$group": {
        "_id": "$tags",  
        "count": {"$sum": 1}  
    }},
    {"$sort": {"count": -1}},  
    {"$limit": 1}  
]
result1 = posts.aggregate(pipeline1)

print("Most common tag")
for doc in result1:
    print(f"Tag: {doc['_id']}")


pipeline2 = [
    {"$match": {"address.city": "JAMAICA", "result": "Violation Issued"}},  
    {"$group": {
        "_id": "$address.zip",  
        "failure_count": {"$sum": 1}  
    }},
    {"$sort": {"failure_count": -1}}  
]
result2 = inspections.aggregate(pipeline2)

print("Number of Failures per ZIP Code in Jamaica")
for doc in result2:
    print(f"ZIP Code: {doc['_id']}, Failed Inspections: {doc['failure_count']}")


pipeline3 = [
    {"$match": {"status": "popular"}},  
    {"$unwind": "$shorturl"},  
    {"$group": {
        "_id": "$media",  
        "avg_view_count": {"$avg": "$shorturl.view_count"}  # Calculate average view count
    }}
]
result3 = stories.aggregate(pipeline3)

print("Average view count of each media type")
for doc in result3:
    print(f"Media Type: {doc['_id']}, Average View Count: {doc['avg_view_count']}")
    
    
pipeline4 = [
    {"$unwind": "$entities.user_mentions"},  
    {"$group": {
        "_id": "$entities.user_mentions.screen_name",  
        "user_mentioned_count": {"$sum": 1}  
    }},
    {"$sort": {"user_mentioned_count": -1}},  
    {"$limit": 10}  
]
result4 = tweets.aggregate(pipeline4)

print("Top 10 Most Mentioned Users")
for doc in result4:
    print(f"User: @{doc['_id']}, Mentions: {doc['user_mentioned_count']}")


pipeline5 = [
    {"$unwind": "$cast"},  
    {"$group": {
        "_id": "$cast",  # Group by actor/actress
        "AvgRating": {"$avg": "$tomatoes.viewer.rating"}  
    }},
    {"$sort": {"AvgRating": -1}},  
    {"$limit": 1}
]
result5 = movies.aggregate(pipeline5)

print("Highest Average Tomatoes Rating per Actor/Actress")
for doc in result5:
    print(f"Top Actor/Actress: {doc['_id']}, Average Viewer Rating: {doc['AvgRating']}")

