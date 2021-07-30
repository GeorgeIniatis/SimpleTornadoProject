import pymongo
import json
from bson.json_util import loads, dumps

# We assume our database is empty with no collections
# w3schools provides excellent resources/tutorials

connection = pymongo.MongoClient("localhost", 27017)
print("Connection successful")
print("Available databases:", end=" ")
print(connection.list_database_names())

testDB = connection["testDB"]
print("testDB accessed successfully")

print("Available collections:", end=" ")
collectionList = testDB.list_collection_names()
print(collectionList)

# Check if collection already exists
if "widgets" in collectionList:
    print("The collection exists.")
else:
    print("The collection doesn't exist.")

# Lets create the collection
widgets = testDB["widgets"]

widgets.insert_one(
    {"Name": "George", "Address": "Glasgow"}
)
widgets.insert_many(
    [
        {"Name": "Test", "Address": "Unknown"},
        {"Name": "Subject", "Address": "Known"},
    ]
)

print("Collection created")
print("Available collections:", end=" ")
collectionList = testDB.list_collection_names()
print(collectionList)

# Retrieve a document and print its info
document = widgets.find_one(
    {"Name": "George"}
)
print(document)
print(document["Name"])
print(document["_id"])

# Update document
query = {"Name": "George"}
update = {"$set": {"Name": "Alex"}}

widgets.update_one(query, update)

# Retrieve all documents
for document in widgets.find():
    print(document)

# Retrieve specific documents
print()
for document in widgets.find({"Address": "Glasgow"}):
    print(document)

# Remove document
widgets.delete_one({"Address": "Unknown"})

# Convert document to json by removing _id
del document["_id"]
document_json = json.dumps(document)
print(document_json)

# Convert document to json without removing _id
document = widgets.find_one(
    {"Name":"Alex"}
)
document_json = dumps(document)
print(document_json)

