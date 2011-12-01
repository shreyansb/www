import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.autoreload
import urllib
import random
from BeautifulSoup import BeautifulStoneSoup
import datetime
import re
import time

class MainHandler(tornado.web.RequestHandler):
    def get_latest_url(self, user):
        SB_FLICKR_LATEST_RSS_URL = "http://api.flickr.com/services/feeds/photos_public.gne?id=94416001@N00&lang=en-us&format=rss_200"
        AG_FLICKR_LATEST_RSS_URL = "http://api.flickr.com/services/feeds/photos_public.gne?id=51883129@N06&lang=en-us&format=rss_200"		
        if user == 'sb': RSS_URL = SB_FLICKR_LATEST_RSS_URL
        if user == 'ag': RSS_URL = AG_FLICKR_LATEST_RSS_URL
        rss = urllib.urlopen(RSS_URL)
        soup = BeautifulStoneSoup(rss.read())
        latest_lightbox_url = soup.find('item').link.string+"lightbox"
        return latest_lightbox_url
        
    def get(self):
        if self.request.uri == '/sb': return self.redirect(self.get_latest_url('sb'))
        if self.request.uri == '/ag': return self.redirect(self.get_latest_url('ag'))
        
        STATIC_DIR_PATH = "/static/images/"
        HOMEPAGE_IMAGES = [
            ("srb-ag_looking_up.jpg","ag-redwood.jpg"),
            ("sb-varanasi_tree.jpg","ag-gingko.jpg"),
            ("sb-china-food.jpg","ag-china-slippers.jpg")
        ] 
        # pick a random image from the ones pairs defined above
        choice = random.choice(HOMEPAGE_IMAGES)
        sb_image = STATIC_DIR_PATH+choice[0]
        ag_image = STATIC_DIR_PATH+choice[1]
        
        wikipedia_random = 'http://en.wikipedia.org/wiki/Special:Random';
        utc = datetime.datetime.now()
        est = (utc - datetime.timedelta(hours=5)).strftime("%H:%M")
        pst = (utc - datetime.timedelta(hours=8)).strftime("%H:%M")

        # get the rss feeds for both flickr streams and create the url for the latest lightbox
        sb_latest_lightbox_url = self.get_latest_url('sb')
        ag_latest_lightbox_url = self.get_latest_url('ag')
        template_vars = {
            "sb_latest_lightbox_url":sb_latest_lightbox_url,
            "ag_latest_lightbox_url":ag_latest_lightbox_url,
            "sb_image":sb_image,
            "ag_image":ag_image,
            "sb_time_link":wikipedia_random,
            "ag_time_link":wikipedia_random,
            "est":est,
            "pst":pst
        }
        self.render("templates/first_homepage.html", title="srb.ag", **template_vars)

class RedirectHandler(tornado.web.RequestHandler):
    def get(self):
        uri = self.request.uri
        if re.match('^/dotfiles$', uri):
	        self.redirect('http://github.com/shreyansb/dotfiles')
        elif re.match('^/github$', uri):
            self.redirect('http://github.com/shreyansb')
        elif re.match('^/new$', uri):
            self.redirect('http://github.com/')
        elif re.match('^/fks$', uri):
            self.redirect('http://srb.ag/static/files/flickr_keyboard_shortcuts_v0_2_9.crx')
        elif re.match('^/venmolive$', uri):
            self.redirect('http://107.20.240.170/')
        else:
            self.redirect('http://srb.ag')

class FlappyHandler(tornado.web.RequestHandler):
    def get(self):
        very_early_morning = ["18621108"]
        early_morning = ["18621251"]
        morning = ["18621197"]
        late_morning = ["18609243"]
        noon = ["18609330"]
        evening = ["18609390"]
        late_evening = ["18609432"]
        night = ["18609455", "18609482"]
        late_night = ["18620985"]
        
        now = datetime.datetime.now()
        now = now - datetime.timedelta(hours=5)
        hour = now.hour
        v = None
        state = ""
        
        if hour >= 6 and hour < 7: 
            v = very_early_morning
            state = "waking up"
        elif hour >= 7 and hour < 8:
            v = early_morning
            state = "stretching"
        elif hour >= 8 and hour < 9:
            v = morning
            state = "flapping"
        elif hour >= 9 and hour < 11:
            v = late_morning
            state = "flapping"
        elif hour >= 11 and hour < 16: 
            v = noon
            state = "flapping"
        elif hour >= 16 and hour < 18: 
            v = evening
            state = "slowing down"
        elif hour >= 18 and hour < 24: 
            v = late_evening
            state = "resting"
        elif hour >= 0 and hour < 2: 
            v = night
            state = "sleeping"
        else:
            v = late_night
            state = "dreaming"
        
        v = random.choice(v)
        self.render("templates/flappy.html", video_id=v, state=state)

class SlideShowHandler(tornado.web.RequestHandler):
    def get(self):
        if self.request.uri == '/insta': return self.render("templates/slideshow.html", ss_type="insta")
        if self.request.uri == '/doodles': return self.render("templates/slideshow.html", ss_type="doodles")

class YogaHandler(tornado.web.RequestHandler):
    def get(self):
        m = re.match("/yoga/([\d]+)", self.request.uri)
        if m:
            video_number = m.group(1)
            if len(video_number) == 1:
                video_number_l = "0%s" % video_number
            elif len(video_number) == 2:
                video_number_l = video_number

            # possibly differing sizes due to orientation
            if video_number in ['1', '3', '4']:
                height = "640"
                width = "480"
            else:
                height = "480"
                width = "640"

            flash_player_path = "/static/files/flowplayer-3.2.7.swf"
            video_url = "http://dl.dropbox.com/u/1654579/Videos/%s.flv" % video_number_l
            return self.render("templates/yoga_video.html", 
                               video_number = video_number,
                               video_url = video_url,
                               flash_player_path = flash_player_path,
                               height=height,
                               width=width)
        return self.render("templates/yoga_menu.html")

application = tornado.web.Application([
    (r"/", MainHandler),
	(r"/sb", MainHandler),
	(r"/ag", MainHandler),
	(r"/flappy", FlappyHandler),
	(r"/insta", SlideShowHandler),
	(r"/doodles", SlideShowHandler),
	(r"/yoga", YogaHandler),
	(r"/yoga/.*", YogaHandler),
	(r"/dotfiles", RedirectHandler),
	(r"/fks", RedirectHandler),
	(r"/.*", RedirectHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
