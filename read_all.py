#!/usr/bin/env python

import requests
import tweepy, time, sys
import os
import inspect
from shutil import copyfile
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from configparser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.ini')
os.chdir(os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)))

site_list = open('sites.txt', 'r').read().split('\n')

for site in site_list:
    if "{0.netloc}".format(urlsplit(site))[:-4].startswith('www.'):
        domain = "{0.netloc}".format(urlsplit(site))[4:-4]
    else:
        domain = "{0.netloc}".format(urlsplit(site))[:-4]
    print(domain)
    new = open(os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)) + "/files/" + domain + "-new.txt", "r").read().split("\n")
    old = open(os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)) + "/files/" + domain + "-old.txt", "r").read().split("\n")
    temp = list(tuple(x for x in new if x not in set(old)))

    auth = tweepy.OAuthHandler(parser.get(domain, 'CONSUMER_KEY'), parser.get(domain, 'CONSUMER_SECRET'))
    auth.set_access_token(parser.get(domain, 'ACCESS_KEY'), parser.get(domain, 'ACCESS_SECRET'))
    api = tweepy.API(auth)

    if temp > []:
        for product in temp:
            item_soup = BeautifulSoup(requests.get(product + ".xml").content,"lxml")
            title = item_soup.find("title").text
            for img_detail in item_soup.find_all("image")[1:]:
                img_url = img_detail.find("src").text
            for var_ele in item_soup.find_all("variant"):
                variant = var_ele.find("id", {"type": "integer"}).text
                if var_ele.find("option1").text == "Default Title":
                    option = ""
                else:
                    option = ", " + var_ele.find("option1").text
                if var_ele.find("option2", {"nil": "true"}) is None:
                    option2 = ", " + var_ele.find("option2").text
                    option = option + option2
                if var_ele.find("inventory-quantity", {"type": "integer"}) is not None:
                    count = var_ele.find("inventory-quantity", {"type": "integer"}).text
                    filename = variant + "-temp.jpg"
                    if int(count) > 1:
                        request = requests.get(img_url)
                        if request.status_code == 200:
                            with open(filename, 'wb') as image:
                                for chunk in request:
                                    image.write(chunk)
                        api.update_with_media(filename, title + option + "\n" + "Inventory: " + count + "\n" + "http://www." + domain + ".com/cart/" + variant + ":1")
                        #print(title + option + "\n" + "Inventory: " + count + "\n" + "http://www." + domain + ".com/cart/" + variant + ":1")
                        os.remove(filename)
    copyfile(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)) + "/files/" + domain + "-new.txt", os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)) + "/files/" + domain + "-old.txt")ß