import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import os.path
import tornado.options
from tornado.options import define, options
from uuid import uuid4

"""
Any option in a define statement will become available as an attribute of the global options object
python3 helloUser.py --help will print out all the options you have defined along with the help text
"""

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        self.ShoppingCart = ShoppingCart()
        handlers = [
            (r'/', DetailHandler),
            (r'/cart', CartHandler),
            (r'/cart/status', StatusHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class ShoppingCart(object):
    totalInventory = 10
    callbacks = []
    carts = {}

    def register(self, callback):
        self.callbacks.append(callback)

    def unregister(self, callback):
        self.callbacks.remove(callback)

    def moveItemToCart(self, session):
        if session in self.carts:
            return

        self.carts[session] = True
        self.notifyCallbacks()

    def removeItemFromCart(self, session):
        if session not in self.carts:
            return

        del (self.carts[session])
        self.notifyCallbacks()

    def notifyCallbacks(self):
        for callback in self.callbacks:
            callback(self.getInventoryCount())

    def getInventoryCount(self):
        return self.totalInventory - len(self.carts)


class DetailHandler(tornado.web.RequestHandler):
    def get(self):
        session = uuid4()
        count = self.application.ShoppingCart.getInventoryCount()
        self.render("index.html", session=session, count=count)


class CartHandler(tornado.web.RequestHandler):
    def post(self):
        action = self.get_argument('action')
        session = self.get_argument('session')

        if not session:
            self.set_status(400)
            return

        if action == 'add':
            self.application.ShoppingCart.moveItemToCart(session)
        elif action == 'remove':
            self.application.ShoppingCart.removeItemFromCart(session)
        else:
            self.set_status(400)


class StatusHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.application.ShoppingCart.register(self.callback)

    def on_close(self):
        self.application.ShoppingCart.unregister(self.callback)

    def on_message(self, message):
        pass

    def callback(self, count):
        self.write_message('{"inventoryCount":"%d"}' % count)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print("Listening")
    tornado.ioloop.IOLoop.instance().start()
