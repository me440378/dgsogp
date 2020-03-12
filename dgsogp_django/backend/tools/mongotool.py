from pymongo import MongoClient

def getMongoDB():
	client = MongoClient(
			host = '192.168.191.10',
			port = 27017,
			username = 'dgsogp_data',
			password = '123456',
			authSource = 'dgsogp_data_db',
		)
	return client.get_database('dgsogp_data_db')

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
		json_data.append(document)
	return json_data
