#!/usr/bin/env python

import requests
import os
from bs4 import BeautifulSoup

url = "http://www.funko-shop.com/sitemap_products_1.xml"

soup = BeautifulSoup(requests.get(url).content,"lxml")
products = soup.find_all("loc")

open("new.txt", 'w').close()
file = open("new.txt", "w")
for item in products:
    #print (item.text + ",")
    file.write(item.text+"\n")
file.close()

exec(open("./read.py").read())
