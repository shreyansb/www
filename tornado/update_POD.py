import urllib
import random
from BeautifulSoup import BeautifulSoup
import logging
import datetime
import re
import string
import sqlite3
import math

#Methods required to clear and update the database of PODs once per day.
#These methods are scheduled using a crontab

#Deletes previous pod entries from the database
def clear_database():
    conn = sqlite3.connect("/home/ubuntu/www/db/pod")
    conn.execute("delete from pics")
    conn.commit()

#Returns dict of pics for closest day to target date in url, if none available, returns proxy dict
def get_pics(url=string, target_date=datetime.date):
    FLICKR_PATH = "http://www.flickr.com"
    split_url = string.rsplit(url, '/')
    url_month = int(split_url[8])
    url_day = int(split_url[9])
    url_date = datetime.date(target_date.year, url_month, url_day)

    pics = {}
    img_links = []
    rss = urllib.urlopen(url)
    soup = BeautifulSoup(rss.read())
    for item in soup.findAll('a', href=re.compile('datetaken')):
    	img_links.append(FLICKR_PATH+item['href'])

    if len(img_links)<1:
    	item = soup.find("table", {"class" : "thumb" }).find('a', href=True)
    	proxy_date_url = FLICKR_PATH+item['href']
    	return get_pics(proxy_date_url, target_date)
    else:
    	date_diff = (target_date-url_date).days
    	if date_diff<0:
    	    date_diff = 365 + date_diff
    	pics[date_diff] = img_links
    	return pics

#Stores the urls for today in a database: /home/ubuntu/www/db/pod
def store_pics(closest_pics=[]):
    conn = sqlite3.connect("/home/ubuntu/www/db/pod")
    for image in closest_pics:
        conn.execute("insert into pics(url) values(?)", (image,))	    
        conn.commit()

#Find pics and stores them
def update_database():
    clear_database()
    SB_FLICKR_ARCHIVE_URL = "http://www.flickr.com/photos/thebigdurian/archives/date-taken/20"
    today = datetime.date.today()
    month_date = "/"+str(today.month)+"/"+str(today.day)+"/"
    pics_of_day = {}
    closest_pics = []

    for i in range (4, int(str(today.year)[2:])+1):
    	if i < 10:
    		i = '0'+str(i)
    	curr_date_taken_url = SB_FLICKR_ARCHIVE_URL+str(i)+month_date 
    	curr_pics = {}
    	curr_pics = get_pics(curr_date_taken_url, today)

    	if len(curr_pics)>0:
    		key = curr_pics.keys()[0]
    		imgs = curr_pics.get(key)
    		if key in pics_of_day:
    			for i in imgs:
    				pics_of_day[key].append(i)
    		else:
    			pics_of_day[key] = imgs

    closest = min(pics_of_day.keys())
    closest_pics = pics_of_day[closest]
    store_pics(closest_pics)


if __name__ == "__main__":
    update_database()
