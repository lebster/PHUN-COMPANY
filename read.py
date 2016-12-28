#!/usr/bin/env /Users/philliptsan/Projects/phun-company/bin/python

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

old = open("old.txt", "r")
new = open("new.txt", "r")

new_1 = new.read().split("\n")
old_1 = old.read().split("\n")

temp3 = list(tuple(x for x in new_1[-1] if x not in set(old_1[-1])))
#print (temp3)
#print (old_1)
#print (new_1)
if temp3 > []:
    for pro in temp3:
        item2 = requests.get(pro + ".xml")
        soup3 = BeautifulSoup(item2.content,"lxml")
        title = soup3.find("title")
        for img_detail in soup3.find_all("image")[1:]:
            img_url = img_detail.find("src")
        for var_ele in soup3.find_all("variant"):     
            variant = var_ele.find("id", {"type": "integer"})
            option = var_ele.find("option1")   
            count = var_ele.find("inventory-quantity", {"type": "integer"})
            filename = variant.text + "-temp.jpg"
            request = requests.get(img_url.text)
            if request.status_code == 200:
                with open(filename, 'wb') as image:
                    for chunk in request:
                        image.write(chunk)
            api.update_with_media(filename, title.text + ", " + option.text + "\n" + "Inventory: " + count.text + "\n" + "http://www.funko-shop.com/cart/" + variant.text + ":1")
            #print (title.text + ", " + option.text + "\n" + "Inventory: " + count.text + "\n" + "http://www.funko-shop.com/cart/" + variant.text + ":1")
            os.remove(filename)

copyfile("/Users/philliptsan/Projects/phun-company/new.txt", "/Users/philliptsan/Projects/phun-company/old.txt")