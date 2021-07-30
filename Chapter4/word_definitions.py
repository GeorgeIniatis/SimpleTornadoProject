import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options
import os.path
import pymongo

"""
Any option in a define statement will become available as an attribute of the global options object
python3 helloUser.py --help will print out all the options you have defined along with the help text
"""

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/(\w+)", WordHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
        connection = pymongo.MongoClient("localhost", 27017)
        self.db = connection["testDB"]
        tornado.web.Application.__init__(self, handlers, **settings)


class WordHandler(tornado.web.RequestHandler):
    def get(self, word):
        collection = self.application.db.dictionary
        word_document = collection.find_one(
            {"Word": word}
        )
        if word_document:
            self.write(word_document["Definition"])
        else:
            self.set_status(404)
            self.write("Definition not found")

    def post(self, word):
        definition = self.get_argument("definition")
        collection = self.application.db.dictionary
        word_document = collection.find_one(
            {"Word": word}
        )
        if word_document:
            query = {"Word": word}
            update = {"$set": {"Definition": definition}}
            collection.update_one(query, update)
        else:
            collection.insert_one(
                {"Word": word, "Definition": definition}
            )
        self.write(f"{word}:{definition}")


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print("Listening")
    tornado.ioloop.IOLoop.instance().start()
