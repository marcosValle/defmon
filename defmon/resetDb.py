import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
client.drop_database('defmon')
