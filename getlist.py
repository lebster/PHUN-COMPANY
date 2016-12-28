#!/usr/bin/env python

import requests
import os
from bs4 import BeautifulSoup

url = "http://www.funko-shop.com/sitemap_products_1.xml"

soup = BeautifulSoup(requests.get(url).content,"lxml")

products = soup.find_all("loc")
file = open("old.txt", "w")
for item in products:
    file.write(item.text + "\n")
file.close()
