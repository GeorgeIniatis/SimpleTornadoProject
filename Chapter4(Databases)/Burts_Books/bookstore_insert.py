import pymongo

connection = pymongo.MongoClient("localhost", 27017)
testDB = connection["testDB"]
bookstore = testDB["bookstore"]

bookstore.insert_many(
    [
        {
            "title": "Programming Collective Intelligence",
            "subtitle": "Building Smart Web 2.0 Applications",
            "author": "Toby Segaran",
            "date_added": 1310248056,
            "date_released": "August 2007",
            "isbn": "978-0-596-52932-1",
            "description": "Simple description of a book",
        },
        {
            "title": "RESTful Web Services",
            "subtitle": "Web services for the real world",
            "author": "Leonard Richardson, Sam Ruby",
            "date_added": 1311148056,
            "date_released": "May 2007",
            "isbn": "978-0-596-52926-0",
            "description": "Another simple desription",
        }
    ]
)
