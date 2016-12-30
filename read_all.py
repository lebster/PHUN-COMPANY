#!/usr/bin/env python

import requests
import tweepy, time, sys
import os
import configparser
from shutil import copyfile
from bs4 import BeautifulSoup
from urllib.parse import urlsplit

CONSUMER_KEY = 'V05KauqiVMAXUYUqSA9hZSDUH'
CONSUMER_SECRET = 'v4VSC4GbM6sqWmVECAh1NlXTr3A2JmM7uikajmzly8FBGtHtWj'
ACCESS_KEY = '812212841822310401-yuQIXEVFlGdTsEWKRqQCoBLpRLCY2kr'
ACCESS_SECRET = 'yzvdvKAVrkHv35vGmviJu7UaU1GDu6CQZfUMzBmfN3NIk'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)

site_list = open("sites.txt", "r").read().split("\n")

for site in site_list:
    if "{0.netloc}".format(urlsplit(site))[:-4].startswith('www.'):
        domain = "{0.netloc}".format(urlsplit(site))[4:-4]
    else:
        domain = "{0.netloc}".format(urlsplit(site))[:-4]
    new = open("files/" + domain + "-new.txt", "r").read().split("\n")
    old = open("files/" + domain + "-old.txt", "r").read().split("\n")
    temp = list(tuple(x for x in new if x not in set(old)))

    if temp > []:
        for product in temp:
            item_soup = BeautifulSoup(requests.get(product + ".xml").content,"lxml")
            title = item_soup.find("title").text
            #print (title)
            for img_detail in item_soup.find_all("image")[1:]:
                img_url = img_detail.find("src").text
            for var_ele in item_soup.find_all("variant"):
                variant = var_ele.find("id", {"type": "integer"}).text
                option = var_ele.find("option1").text
                count = var_ele.find("inventory-quantity", {"type": "integer"}).text
                filename = variant + "-temp.jpg"
                request = requests.get(img_url)
                if request.status_code == 200:
                    with open(filename, 'wb') as image:
                        for chunk in request:
                            image.write(chunk)
                api.update_with_media(filename, title + ", " + option + "\n" + "Inventory: " + count + "\n" + "http://" + domain + ".com/cart/" + variant + ":1")
                #print (title + ", " + option + "\n" + "Inventory: " + count + "\n" + "http://www." + domain + ".com/cart/" + variant + ":1")
                os.remove(filename)
    copyfile(os.getcwd() + "/files/" + domain + "-new.txt", os.getcwd() + "/files/" + domain + "-old.txt")
