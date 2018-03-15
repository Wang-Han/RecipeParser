# coding=utf-8
import string
from bs4 import BeautifulSoup
import requests

f = "file_food.txt"
f_txt = open(f, "w")

def get_ingredients():
    lst = []
    alpha_list = list(string.ascii_lowercase)
    base_url = str("https://www.bbc.co.uk/food/ingredients/by/letter/")
    for letter in alpha_list:
        url = base_url + letter
        r  = requests.get(str(url))
        data = r.text
        soup = BeautifulSoup(data, "html5lib")
        links = soup.findAll("li")
        for l in links:
            if l.get("class") == [u'resource', u'food']:
                food = l.get("id").replace('_',' ')
                lst.append(food)
    return lst

print get_ingredients()
