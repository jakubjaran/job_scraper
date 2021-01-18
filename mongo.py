import pymongo
from SECRET import url

def updateMongoDB(offers):	
	client = pymongo.MongoClient(url)

	db = client["job_scraper"]

	col = db["offers"]

	col.delete_many({})

	col.insert_many(offers)