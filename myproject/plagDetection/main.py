from pymongo import cursor
import pysimilar
from pprint import pprint
from pysimilar import compare
import pymongo

#DB connection with djongo
client = pymongo.MongoClient("mongodb://localhost:27017/")

#DB name
db = client["fypdjangoplag"]

#Collection name
col = db["myapp_document"]



x = col.find_one()
print(x)
