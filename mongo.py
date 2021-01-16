import pymongo
from PASS import password

def updateMongoDB(offers):	
	client = pymongo.MongoClient(f'mongodb+srv://admin:{password}@cluster0.jtv83.mongodb.net/job_scraper?retryWrites=true&w=majority')

	db = client["job_scraper"]

	col = db["offers"]

	col.delete_many({})

	col.insert_many(offers)