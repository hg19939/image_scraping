# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 16:58:55 2022

Some of the code is adapted from the first challenge: https://github.com/hg19939/ebook_scraping.git
Scraped website: https://www.vox.com/

@author: hg19939
"""

# Imports:
import os
import io
import cv2
import csv
import random
import requests
import numpy as np
import pandas as pd
from PIL import Image
from bs4 import BeautifulSoup


# Script:
def web_crawler():
    """
    Upon calling, this function will loop through the contents of
    the current web page, extract the links of all articles presented,
    save them in a dictionary, and finally return it.
    
    Returns
    -------
    links : list
        A list of web links to scrape data from.
        
    @author: hg19939
    """
    
    links = []
    
    for article in soup.find_all("a", {"class": "c-entry-box--compact__image-wrapper"}): 
        links.append(article["href"])
        
    return links


def web_scraper(articles: list):
    """
    Uppon calling, this function will loop through a list of scraped articles,
    extract the images' link and description, before returning them.
    Parameters
    ----------
    books : list
        A list of book webpage links to scrape.

    Returns
    -------
    img_links: list
        A list of images' links.
    img_descs : list
        A list of images' descriptions.
        
    @author: hg19939
    """
    
    img_links = []
    img_descs = []
        
    for article in articles:
        source = requests.get(article).text
        soup = BeautifulSoup(source, "lxml")
        figures = soup.find_all("figure", {"class": "e-image"})
        
        for figure in figures:
            image = figure.find("img", "")
            caption = figure.find("figcaption", "")
            if (image is not None) and (caption is not None):
                img_links.append(image["src"])
                img_descs.append(caption.text)
            else: 
                continue

    return img_links, img_descs


def save_as_csv(csv_file, links: list, descriptions: list):
    """
    Upon calling, this function will save the scraped images' links
    and descriptions as a CSV file for convinient use.

    Parameters
    ----------
    csv_file : TYPE
        DESCRIPTION.
    links : list
        Images' links.
    descriptions : list
        Images' descriptions.

    Returns
    -------
    None.

    @author: hg19939
    """
    
    if (len(links) == len(descriptions)):
        for i in range(len(links)): csv_writer.writerow([links[i], descriptions[i]])
    else:
        print("Number of titles do not match the number of links.")
        

def download_images(path, url, file_name):
    """
    Uppon calling, this function will request the contents of the
    provided link, extract the image, turn it into a NumPy array,
    before preprocessing and saving it.

    Parameters
    ----------
    path : 
        Path to store the images at.
    url : 
        Link to download the images from.
    file_name : 
        Name of the file.

    Returns
    -------
    None.

    """
    image_content = requests.get(url).content
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file)
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (300, 200))
    cv2.imwrite(os.path.join(path, file_name), image)
        
        
csv_file = open("scraped_images.csv", "a", encoding="utf-8")
csv_writer = csv.writer(csv_file)

# Loop through all pages:
for page_num in range(1, 16):
    source = requests.get("https://www.vox.com/energy-and-environment/archives/{}".format(page_num)).text    
    soup = BeautifulSoup(source, "lxml")
    
    links = web_crawler()
    links, descriptions = web_scraper(links)
    save_as_csv(csv_file, links, descriptions)

# Close the CSV file:
csv_file.close()

# Load the CSV file:
df = pd.read_csv("scraped_images.csv")

# Loop through the links and download the images:
for i in range(len(df[df.columns[0]])):
    download_images("images/", df[df.columns[0]][i], "img-{}.jpg".format(random.random()))
