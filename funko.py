#!/usr/bin/env /Users/philliptsan/Projects/phun-company/bin/python

import requests
import os
from bs4 import BeautifulSoup

url = "http://www.funko-shop.com/sitemap_products_1.xml"

products = requests.get(url)

soup = BeautifulSoup(products.content,"lxml")

new = soup.find_all("loc")

open("new.txt", 'w').close()
file = open("new.txt", "w")
for item in new:
    #print (item.text + ",")
    file.write(item.text+"\n")
file.close()

exec(open("./read.py").read())