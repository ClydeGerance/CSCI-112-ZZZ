import pymongo
import pymongo import MongoClient
from pprint import pprint

client = MongoClient('172.31.91.223',27017)
db = client['sample']
grades = db['grades']
inspections = db['inspections']
stories = db['stories']

