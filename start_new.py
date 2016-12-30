#!/usr/bin/env python

import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlsplit

site_list = open("sites.txt", "r").read().split("\n")

os.makedirs(os.getcwd() + "/files", exist_ok=True)

for site in site_list:
    soup = BeautifulSoup(requests.get(site).content,"lxml")
    products = soup.find_all("loc")
    for site in site_list:
        soup = BeautifulSoup(requests.get(site).content,"lxml")
        products = soup.find_all("loc")
        if "{0.netloc}".format(urlsplit(site))[:-4].startswith('www.'):
            domain = "{0.netloc}".format(urlsplit(site))[4:-4]
        else:
            domain = "{0.netloc}".format(urlsplit(site))[:-4]
        file = open(os.getcwd() + "/files/" + domain + "-old.txt", "w")
        for item in products:
            file.write(item.text + "\n")
        file.close()
        open(os.getcwd() + "/files/" + domain + "-new.txt", 'a').close()