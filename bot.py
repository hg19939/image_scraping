# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 15:54:46 2022

@author: hg19939
"""

# Imports:
import os
import io
import cv2
import random
import requests
import numpy as np
from PIL import Image
from bs4 import BeautifulSoup

# Script:
def web_crawling(soup):
    """Crawl and extract image links from the website."""
    links = []
    images = soup.find_all("img")

    for image in soup.find_all("a", {"class": "ez-resource-thumb__link"}):
        link = image.img["src"]
        links.append(link)
    
    return links


def web_scraping(path, url, file_name):
    """Download and preprocess the image."""
    image_content = requests.get(url).content
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file)
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (300, 200))
    cv2.imwrite(os.path.join(path, file_name), image)
        


cat_source = requests.get("https://www.vecteezy.com/free-photos/cat?license-free=true&orientation-horizontal=true").text    
cat_soup = BeautifulSoup(cat_source, "html.parser")
cat_links = web_crawling(cat_soup)

for i in range(1, 101, 2):
    web_scraping("images/", cat_links[i], "img-{}.jpg".format(random.random()))
    
parrot_source = requests.get("https://www.vecteezy.com/free-photos/parrot?license-free=true&orientation-horizontal=true").text    
parrot_soup = BeautifulSoup(parrot_source, "html.parser")
parrot_links = web_crawling(parrot_soup)

for i in range(1, 101, 2):
    web_scraping("images/", parrot_links[i], "img-{}.jpg".format(random.random()))
    
frog_source = requests.get("https://www.vecteezy.com/free-photos/frog?license-free=true&orientation-horizontal=true").text    
frog_soup = BeautifulSoup(frog_source, "html.parser")
frog_links = web_crawling(frog_soup)

for i in range(1, 101, 2):
    web_scraping("images/", frog_links[i], "img-{}.jpg".format(random.random()))
