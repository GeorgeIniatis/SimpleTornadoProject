import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options
import os.path

"""
Any option in a define statement will become available as an attribute of the global options object
python3 helloUser.py --help will print out all the options you have defined along with the help text
"""

define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class PoemPageHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument("noun1")
        noun2 = self.get_argument("noun2")
        noun3 = self.get_argument("noun3")
        verb = self.get_argument("verb")

        self.render("poem.html", roads=noun1, wood=noun2, difference=noun3, made=verb)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/poem", PoemPageHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print("Listening")
    tornado.ioloop.IOLoop.instance().start()
