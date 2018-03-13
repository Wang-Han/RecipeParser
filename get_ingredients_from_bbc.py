# coding=utf-8
import string
from bs4 import BeautifulSoup
import requests
# import nltk
import re
# nltk.download('wordnet')
# from nltk.corpus import wordnet as wn
# food = wn.synset('food.n.02')
# t = list(set([w for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))
# print t
# filename = "food_list.txt"
# f = open(filename, "w")
# f.write(str(t))


# usda = 'FOOD_DES.txt'
# usda_file = open(usda, "rb")
# i = 0
# print usda_file.read()
# # for line in usda:
# #
# #
# #     print i
# #     i += 1
# usda_file.close()


f = "file_food.txt"
f_txt = open(f, "w")

alpha_list = list(string.ascii_lowercase)
base_url = str("https://www.bbc.co.uk/food/ingredients/by/letter/")

for letter in alpha_list:
    url = base_url + letter
    r  = requests.get(str(url))
    data = r.text
    soup = BeautifulSoup(data, "html5lib")
    links = soup.findAll("li")
    for link in links:
        if link.get("class") == [u'resource', u'food']:
            food = link.get("id").replace('_',' ')
            f_txt.write(str(food + ))
            print food
