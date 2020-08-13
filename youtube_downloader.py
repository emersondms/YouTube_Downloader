#!/usr/bin/env python
# coding:utf-8

import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import re   
import youtube_dl

if len(sys.argv) < 2:
    sys.exit("Usage: python youtube_downloader.py <playlist_url> [username] [password]")

playlist_url = sys.argv[1]
must_login = False

if len(sys.argv) > 2:
    username = sys.argv[2]
    password = sys.argv[3]
    must_login = True

driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.get(playlist_url)

if must_login == True:
    driver.find_element_by_partial_link_text("LOGIN").click()

    edit_user = driver.find_element_by_id("identifierId")
    edit_user.send_keys(username)
    edit_user.send_keys(Keys.ENTER)

    driver.find_element_by_name("hiddenPassword")
    time.sleep(3)
    actions = ActionChains(driver)
    actions.send_keys(password)
    actions.send_keys(Keys.ENTER)
    actions.perform()

    # validate login
    driver.find_element_by_id("search-icon-legacy") 
    time.sleep(3)

is_page_bottom = "var bottom = (document.documentElement.scrollTop + window.innerHeight) >= document.documentElement.scrollHeight;return bottom"
y_scroll = 100000

# scroll until reach the page bottom
while not (driver.execute_script(is_page_bottom)):
    driver.execute_script("window.scrollTo(0, %d)" %y_scroll)
    y_scroll += 100000
    time.sleep(3)

page_source = driver.page_source
driver.close()

videos_list = []
video_index = 1

# fetch all video url's
for tag in page_source.split():
   video = re.search("watch..=..........." , tag)
   if video:
        if not "__video_enc" in video.group():
            url = "https://www.youtube.com/"+video.group()
            if not url in videos_list:
                videos_list.append(url)
                print (str(video_index)+" - "+url)
                video_index += 1
                   
ydl_opts = {
    'format': 'worst', # best
    'nocheckcertificate': True,
} 
  
def download_video(): 
    with youtube_dl.YoutubeDL(ydl_opts) as ydl: 
        ydl.download([url]) 

# download the videos
for video in videos_list: 
    url = video.strip()
    try: 
        download_video()
    except:
        pass
