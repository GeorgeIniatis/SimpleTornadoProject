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


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/recommended", RecommendedHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            ui_modules={"Book": BookModule, },
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class BookModule(tornado.web.UIModule):
    def render(self, book):
        return self.render_string('modules/book.html', book=book)

    def embedded_javascript(self):
        return "document.write(\"<b>Hi from embedded JS inside module</b>\")"
        # Could also return a file - return "https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.14/jquery-ui.min.js"

    def embedded_css(self):
        return ".book {background-color:#F5F5F5}"
        # Could also return a file - return "/static/css/newreleases.css"

    def html_body(self):
        return "<script>document.write(\"Hello!\")</script>"


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html",
                    page_title="Burt's Books - Home",
                    header_text="Welcome to Burt's Books!",
                    )


class RecommendedHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("recommended.html",
                    page_title="Burt's Books - Recommended Reading",
                    header_text="Recommended Reading!",
                    books=[
                        {
                            "title": "Programming Collective Intelligence",
                            "subtitle": "Building Smart Web 2.0 Applications",
                            "author": "Toby Segaran",
                            "date_added": 1310248056,
                            "date_released": "August 2007",
                            "isbn": "978-0-596-52932-1",
                            "description": "Book description"
                        },
                        {
                            "title": "Another book",
                            "subtitle": "Building Smart Web 2.0 Applications",
                            "author": "Toby Segaran",
                            "date_added": 1310248056,
                            "date_released": "August 2007",
                            "isbn": "978-0-596-52932-1",
                            "description": "Another Book description"
                        }
                    ]
                    )


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print("Listening")
    tornado.ioloop.IOLoop.instance().start()
