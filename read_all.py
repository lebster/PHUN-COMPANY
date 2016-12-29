#!/usr/bin/env python

import requests
import tweepy, time, sys
import os
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
    domain = "{0.netloc}".format(urlsplit(site))[:-4]
    new = open(domain + "-new.txt", "r").read().split("\n")
    old = open(domain + "-old.txt", "r").read().split("\n")
    temp = list(tuple(x for x in new if x not in set(old)))

    if temp > []:
        for product in temp:
            item_soup = BeautifulSoup(requests.get(product + ".xml").content,"lxml")
            title = item_soup.find("title")
            for img_detail in item_soup.find_all("image")[1:]:
                img_url = img_detail.find("src")
            for var_ele in item_soup.find_all("variant"):
                variant = var_ele.find("id", {"type": "integer"})
                option = var_ele.find("option1")
                count = var_ele.find("inventory-quantity", {"type": "integer"})
                filename = variant.text + "-temp.jpg"
                request = requests.get(img_url.text)
                if request.status_code == 200:
                    with open(filename, 'wb') as image:
                        for chunk in request:
                            image.write(chunk)
                #api.update_with_media(filename, title.text + "\n" + "Inventory: " + count.text + "\n" + "http://" + domain + ".com/cart/" + variant.text + ":1")
                #print (title.text + "\n" + "Inventory: " + count.text + "\n" + "http://www.funko-shop.com/cart/" + variant.text + ":1")
                os.remove(filename)
    copyfile(domain + "-new.txt", domain + "-old.txt")
