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

#Picture of day handler without storing class variables, next step: method w class variables, only update
#pics_of_day if it is currently empty or next set of pics are closer to target date - pass boolean in get_pics meth
class PicofDayHandler(tornado.web.RequestHandler):
	def get(self):
		SB_FLICKR_ARCHIVE_URL = "http://www.flickr.com/photos/thebigdurian/archives/date-taken/20"
		today = datetime.date.today()
		month_date = "/"+str(today.month)+"/"+str(today.day)+"/"
		pics_of_day = {}
		
		for i in range (4, int(str(today.year)[2:])+1):
			if i < 10:
				i = '0'+str(i)
			curr_date_taken_url = SB_FLICKR_ARCHIVE_URL+str(i)+month_date 
			curr_pics = {}
			curr_pics = self.get_pics(curr_date_taken_url, today)
		
			if len(curr_pics)>0:
				key = curr_pics.keys()[0]
				imgs = curr_pics.get(key)
				if key in pics_of_day:
					for i in imgs:
						pics_of_day[key].append(i)			
				else:
					pics_of_day[key] = imgs
		
		closest = min(pics_of_day.keys())			
		img_selected_url = random.choice((pics_of_day[closest]))+"lightbox"
		self.redirect(img_selected_url)
		
	#Returns dict of pics for closest day to target date in url, if none available, returns proxy dict
	def get_pics(self, url=string, target_date=datetime.date):
		FLICKR_PATH = "http://www.flickr.com"
		split_url = string.rsplit(url, '/')
		url_month = int(split_url[8])
		url_day = int(split_url[9])
		url_date = datetime.date(target_date.year, url_month, url_day) #only concerned with proximity of month and day

		pics = {}
		img_links = []
		rss = urllib.urlopen(url)
		soup = BeautifulSoup(rss.read())
		for item in soup.findAll('a', href=re.compile('datetaken')):
			img_links.append(FLICKR_PATH+item['href'])
			
		if len(img_links)<1:
			item = soup.find("table", {"class" : "ArchiveFoot" }).find('a', href=True)
			proxy_date_url = FLICKR_PATH+item['href']
			return self.get_pics(proxy_date_url, target_date)
		else:
			pics[(target_date-url_date).days] = img_links	
			return pics
		
application = tornado.web.Application([
 	(r"/pod", PicofDayHandler)
])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8887)
    tornado.ioloop.IOLoop.instance().start()
