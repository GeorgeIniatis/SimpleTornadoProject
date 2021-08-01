import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options

"""
Any option in a define statement will become available as an attribute of the global options object
python3 helloUser.py --help will print out all the options you have defined along with the help text
"""

define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')  # Get greeting else use default greeting 'Hello'
        self.write(greeting + " friendly user!")

    def write_error(self, status_code, **kwargs):
        self.write(f"Gosh darnit, user! You have caused a {status_code} error ")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
        ]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print("Listening")
    tornado.ioloop.IOLoop.instance().start()
