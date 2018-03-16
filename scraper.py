import requests
from bs4 import BeautifulSoup as bs
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import os
import sys

def scrapeRecipe(url):
    page = requests.get(url)
    soup = bs(page.content, 'html.parser')
    ingredients = []
    ingredientSoup = soup.find_all("span", itemprop="ingredients")
    ingredients = [i.text for i in ingredientSoup]
    stepSoup = soup.find_all(class_="step")
    steps = [s.text for s in stepSoup]

    return([ingredients, steps])
