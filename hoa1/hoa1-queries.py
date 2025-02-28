import pymongo
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('172.31.91.223',27017)
db = client['sample']
grades = db['grades']
inspections = db['inspections']
stories = db['stories']


query1 = {"scores": {"$elemMatch": {"type": "exam", "score": {"$gt": 75}}}}
result1 = list(grades.find(query1))

print("Students that have an exam grade higher than 75")
for student in result1:
    student_id = grades["student_id"]

    exam_scores = [
        s["score"]
        for s in student["score"] 
        if s["type"] == "exam" and s["score"] > 75
    ]

    print(f"Student ID: {student_id}, Exam Score: {exam_scores}")


query2 = {"$or": [{"topic.name": "Television"}, {"media": "videos"}]}
result2 = list(stories.find(query2).sort("diggs", -1))

print("Digg stories where the topic name is 'Television' or the media type is 'videos', and sorted by diggs in descending order")
for story in result2:
   print(story["title"])


query3 = {"shorturl": {"$elemMatch": {"view_count": {"$gt": 1000}}}}
result3 = list(stories.find(query3))

print("All stories where the view count is greater than 1000")
for story in result3:
   print(story["title"])


query4 = {"result": "Fail"}
inspections.update_many(query1, {"$set": {"fine": 100}})


query5 = {"result": "Fail", "address.city": "ROSEDALE"}
inspections.update_many(query2, {"$inc": {"fine": 150}})