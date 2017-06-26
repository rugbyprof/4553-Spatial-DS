from pymongo import MongoClient, GEO2D
import pprint

db = MongoClient().world_data

db.airports.create_index([("geometry.coordinats", GEO2D)])


for doc in db.airports.find({"geometry.coordinates": {"$near": [ -99.8861999512, 35.5766983032 ]}}).limit(30):
    pprint.pprint(doc)

