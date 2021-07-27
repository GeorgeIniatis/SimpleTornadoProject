import tornado.web
import tornado.ioloop


class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world!")


class staticRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class queryStringRequestHandler(tornado.web.RequestHandler):
    def get(self):
        number = int(self.get_argument("argument"))
        result = "even" if number % 2 == 0 else "odd"
        self.write(f"The number is {result}!")


class resourceRequestHandler(tornado.web.RequestHandler):
    def get(self, id):
        self.write(f"You have requested the book with id: {id}")


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", basicRequestHandler),
        (r"/welcome", staticRequestHandler),
        (r"/isEven", queryStringRequestHandler),
        (r"/books/([0-9]+)", resourceRequestHandler),
    ])

    app.listen(8888)
    print("Listening")
    tornado.ioloop.IOLoop.current().start()
