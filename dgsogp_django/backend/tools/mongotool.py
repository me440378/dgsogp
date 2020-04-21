from pymongo import MongoClient

from dgsogp_django.settings import MONGO_DATA_DB

def getMongoDB():
	client = MongoClient(**MONGO_DATA_DB)
	return client.get_database(MONGO_DATA_DB["authSource"])

def checkCollection(db, collectionname):
	collection = db.get_collection(collectionname)
	if collection.count():
		return True
	else:
		return False

def countCollection(db, collectionname):
	collection = db.get_collection(collectionname)
	return collection.count()

def insertCollection(db, collectionname, line):
	collection = db.get_collection(collectionname)
	document = {
		"data": line,
	}
	collection.insert_one(document)

def readCollection(db, collectionname):
	collection = db.get_collection(collectionname)
	json_data = []
	for document in collection.find():
		document['_id'] = str(document['_id'])
		json_data.append(document)
	return json_data
