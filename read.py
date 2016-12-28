#!/usr/bin/env python

import requests
import tweepy, time, sys
import os
from shutil import copyfile
from bs4 import BeautifulSoup

CONSUMER_KEY = 'YGvIINLApvre82RB8yyU9kQjV'
CONSUMER_SECRET = 'u6MVHxDpXfcwylmfM2cHrPm206HfJpbbeNhRSyyrXATfnlhqQ8'
ACCESS_KEY = '813834541013925889-vcr6K4d42CpsAKYk2Y9VJnNawK4iEGQ'
ACCESS_SECRET = 'Yn0VSUZZXjL1owHzE7EcYgTfCUcBNVWoZMw96Vs6Lndr9'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)

new = open("new.txt", "r").read().split("\n")
old = open("old.txt", "r").read().split("\n")

temp = list(tuple(x for x in new if x not in set(old)))
#print (temp)
#print (old)
#print (new)
if temp > []:
    for pro in temp:
        item_soup = BeautifulSoup(requests.get(pro + ".xml").content,"lxml")
        title = item_soup.find("title")
        for img_detail in item_soup.find_all("image")[1:]:
            img_url = img_detail.find("src")
        for var_ele in item_soup.find_all("variant"):
            variant = var_ele.find("id", {"type": "integer"})
            #option = var_ele.find("option1")
            count = var_ele.find("inventory-quantity", {"type": "integer"})
            filename = variant.text + "-temp.jpg"
            request = requests.get(img_url.text)
            if request.status_code == 200:
                with open(filename, 'wb') as image:
                    for chunk in request:
                        image.write(chunk)
            api.update_with_media(filename, title.text + "\n" + "Inventory: " + count.text + "\n" + "http://www.funko-shop.com/cart/" + variant.text + ":1")
            #print (title.text + "\n" + "Inventory: " + count.text + "\n" + "http://www.funko-shop.com/cart/" + variant.text + ":1")
            os.remove(filename)

copyfile("new.txt", "old.txt")
