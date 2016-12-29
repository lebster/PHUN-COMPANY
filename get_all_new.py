#!/usr/bin/env python

import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlsplit

site_list = open("sites.txt", "r").read().split("\n")

for site in site_list:
    soup = BeautifulSoup(requests.get(site).content,"lxml")
    products = soup.find_all("loc")
    domain = "{0.netloc}".format(urlsplit(site))[:-4]
    #print(domain)
    file = open(domain + "-new.txt", "w")
    for item in products:
        file.write(item.text + "\n")
    file.close()

exec(open("./read_all.py").read())
