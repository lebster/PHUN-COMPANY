#!/usr/bin/env /Users/philliptsan/Projects/phun-company/bin/python

import requests
import os
from bs4 import BeautifulSoup

url = "http://www.funko-shop.com/sitemap_products_1.xml"

products = requests.get(url)

soup = BeautifulSoup(products.content,"lxml")

new = soup.find_all("loc")
file = open("old.txt", "w")
for product in soup.find_all("loc"):   
    file.write(product.text + "\n")
    
file.close()