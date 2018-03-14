from get_ingredients_from_bbc import get_ingredients
from scraper import scrapeRecipe
# from ingredients_parser import *
import re
from pattern.en import pluralize

# print pluralize("tomato")

# "allingredients"

all_ingredients = open("allingredients.txt", "r")
all_ingredients = all_ingredients.read()

lst = all_ingredients.split(',')
all_ing_list = []
for i in lst:
    i = i.replace('u\'', '').replace('\'', '').strip()
    all_ing_list.append(i)
# print all_ing_list

# import ast
# x = ast.literal_eval(all_ingredients)
#
# for g in x:
#     print g

fraction_match = r"(\d+[\/\d. ]*|\d)" # /g means global match
measurements = [r'([a-z]+)spoons?', r'cloves?', r'cups?', r'pounds?', r'ounces?', r'large',
r'medium', r'small', r'packs?', r'pints?', r'quarts?', r'gallons?', r'bushel', r'grams?', r'dessertspoons?']

def frac_to_float(frac_str):
    try:
        return float(frac_str)
    except ValueError:
        num, denom = frac_str.split('/')
        try:
            leading, num = num.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac

def get_ing_name(ing):
    t = []
    for true_ing in all_ing_list: # real ings from bbc
        ing_regex_single = r'\b{0}\b'.format(true_ing)
        ing_regex_plural = r'\b{0}\b'.format(pluralize(true_ing))
        match_single = re.search(ing_regex_single, i.lower())
        match_plural = re.search(ing_regex_plural, i.lower())
        if match_single:
            t.append(true_ing)
        elif match_plural:
            t.append(pluralize(true_ing))

    seen = set()
    seen_add = seen.add
    t = [x for x in t if not (x in seen or seen_add(x))]

    t.sort(key=lambda x: len(x.split()), reverse=True)

    lst_of_lst = []
    name = ""
    # for i in ings:
    for db_ingredient in t:
        if db_ingredient in ing.lower():
            print "HERE:", db_ingredient
            name = db_ingredient
            # db_ingredient is now the name of the Ingredient
            lst_of_lst.append(i.split(db_ingredient))
            break

    # print '\n', lst_of_lst
    return [name, lst_of_lst]

def get_ing_quantity(ing_front):
    ingredient_split_list = ing_front.split()
    amount = 0
    for num in ingredient_split_list:
        frac_match = re.search(fraction_match, num)
        if frac_match:
            amount += frac_to_float(frac_match.group(0))
    return amount

def get_ing_measurement(ing_front):
    ingredient_split_list = ing_front.split()
    measurement = ""
    no_nums_ingredient = [w for w in ingredient_split_list if not re.search(fraction_match, w)]
    if(len(no_nums_ingredient) > 0):
        i = no_nums_ingredient[0]
        measurement = i if re.search(r"(?=("+'|'.join(measurements)+r"))", i) else ""
        regex = re.compile(r'[^a-zA-Z]')
        regex.sub('', measurement)
    return measurement

def get_ing_descriptor(ing_front):
    ingredient_split_list = ing_front.split()
    descriptor = ""
    no_nums_ingredient = [w for w in ingredient_split_list if not re.search(fraction_match, w)]
    m = get_ing_measurement(ing_front)
    descriptor = ' '.join(no_nums_ingredient).replace(m, '').strip()
    return descriptor

def get_ing_preparation(ing_back):
    return ing_back.strip()


# all_ing = get_ingredients()
# print len(all_ing)
print "done"
recipe = scrapeRecipe("https://www.allrecipes.com/recipe/21412/tiramisu-ii/?clickId=right%20rail0&internalSource=rr_feed_recipe_sb&referringId=247082%20referringContentType%3Drecipe")
ings = recipe[0]
steps = recipe[1]
print ings, '\n' #, steps, '\n'

# TODO:
# ADD: tomato sauce, cooking spray, tortillas, yellow squash, zucchini, tortillas, bell pepper,
# REMOVE: fat,
# make subs for healthy, veg, chinese,
# make better ingredient parser


lstlst = []
for i in ings: # from scraper
    name_ret = get_ing_name(i)
    lstlst.append(name_ret)

for lst in lstlst:
    print lst
    qty = get_ing_quantity(lst[1][0][0])
    print qty
    msrmnt = get_ing_measurement(lst[1][0][0])
    print msrmnt
    d = get_ing_descriptor(lst[1][0][0])
    print d
    print lst[0]
    # if len(lst) > 1:
    #     p = get_ing_preparation(lst[1])
    #     print p


# stuff in front == qty, DESCRIPTOR
# stuff after == prep
