import pymongo
import datetime

mongodb_host = "mongodb://localhost:27017/"
mongodb_dbname = 'sql_i'
myclient = pymongo.MongoClient(mongodb_host)
mydb = myclient[mongodb_dbname]
migration = mydb.list_collection_names()
for table in migration:
    print(table)
    mycol = mydb[table]
    mycol.delete_many({})

