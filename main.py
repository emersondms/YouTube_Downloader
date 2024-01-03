#!/usr/bin/env python
# coding:utf-8

import sys
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import re   
import youtube_dl

if len(sys.argv) < 2:
    sys.exit("Usage: python main.py <playlist_url>")

#============================================================================
print ("Initiating the webdriver...")

playlist_url = sys.argv[1]
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)
driver.implicitly_wait(30)
driver.get(playlist_url)

#============================================================================
print ("Scraping the HTML page source...")

is_page_bottom = "var bottom = (document.documentElement.scrollTop + window.innerHeight) >= " \
                 "document.documentElement.scrollHeight;return bottom"
y_scroll = 100000

while not (driver.execute_script(is_page_bottom)):
    driver.execute_script("window.scrollTo(0, %d)" %y_scroll)
    y_scroll += 100000
    time.sleep(3)

page_source = driver.page_source
driver.close()

#============================================================================
print ("Fetching all video url's...")

videos_list = []
video_index = 1

for tag in page_source.split():
   video = re.search("watch..=..........." , tag)
   if video:
        if not "__video_enc" in video.group():
            url = "https://www.youtube.com/"+video.group()
            if not url in videos_list:
                videos_list.append(url)
                print (str(video_index)+" - "+url)
                video_index += 1
                   
#============================================================================
print ("Downloadings videos...")

ydl_opts = {
    'format': 'worst', # best
    'nocheckcertificate': True,
} 

def download_video(): 
    with youtube_dl.YoutubeDL(ydl_opts) as ydl: 
        ydl.download([url]) 

for video in videos_list: 
    url = video.strip()
    try: 
        download_video()
    except:
        pass
