#!/usr/bin/env python

import requests
import os, sys
from bs4 import BeautifulSoup
from urllib.parse import urlsplit

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
site_list = open("sites.txt", "r").read().split("\n")

for site in site_list:
    if site is not "":
        #print(site)
        soup = BeautifulSoup(requests.get(site).content,"lxml")
        #print(soup)
        products = soup.find_all("loc")
        if "{0.netloc}".format(urlsplit(site))[:-4].startswith('www.'):
            domain = "{0.netloc}".format(urlsplit(site))[4:-4]
        else:
            domain = "{0.netloc}".format(urlsplit(site))[:-4]
        file = open(os.getcwd() + "/files/" + domain + "-new.txt", "w")
        for item in products:
            file.write(item.text + "\n")
        file.close()

exec(open("./read_all.py").read())

