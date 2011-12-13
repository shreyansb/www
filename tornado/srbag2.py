import tornado.httpserver
import tornado.ioloop
import tornado.web
import urllib
import random
from BeautifulSoup import BeautifulSoup
import logging
import datetime
import re
import string
import sqlite3

#Picture of day handler without storing class variables, next step: method w class variables, only update
#pics_of_day if it is currently empty or next set of pics are closer to target date - pass boolean in get_pics meth
class PicofDayHandler(tornado.web.RequestHandler):
	def get(self):
		closest_pics =[]
		closest_pics = self.get_stored_pics()
		img_selected_url = random.choice(closest_pics)+"lightbox"
		self.redirect(img_selected_url)

	#Creates an instance array from the database
	def get_stored_pics(self):
		closest_pics = []
		conn = sqlite3.connect("/home/ubuntu/www/db/pod")
		connexec = conn.execute("select url from pics")
		for row in connexec:
		    pic_url = row[0]
		    closest_pics.append(pic_url)
		return closest_pics



application = tornado.web.Application([
 	(r"/pod", PicofDayHandler)
])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8887)
    tornado.ioloop.IOLoop.instance().start()
