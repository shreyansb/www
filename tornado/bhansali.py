import tornado.httpserver
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
		self.render("templates/bhansali.html", 
			title="bhansa.li")

application = tornado.web.Application([
    (r"/", MainHandler),
])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8886)
    tornado.ioloop.IOLoop.instance().start()
