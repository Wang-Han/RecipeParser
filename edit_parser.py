from get_ingredients_from_bbc import get_ingredients
from scraper import scrapeRecipe
# from ingredients_parser import *
import re
from pattern.en import pluralize

# print pluralize("tomato")

# "allingredients"

# print all_ing_list

# import ast
# x = ast.literal_eval(all_ingredients)
#
# for g in x:
#     print g




# all_ing = get_ingredients()
# print len(all_ing)
#print "done"
recipe = scrapeRecipe("https://www.allrecipes.com/recipe/21412/tiramisu-ii/?clickId=right%20rail0&internalSource=rr_feed_recipe_sb&referringId=247082%20referringContentType%3Drecipe")
ings = recipe[0]
steps = recipe[1]
#print ings, '\n' #, steps, '\n'

# TODO:
# ADD: tomato sauce, cooking spray, tortillas, yellow squash, zucchini, tortillas, bell pepper,
# REMOVE: fat,
# make subs for healthy, veg, chinese,
# make better ingredient parser


# lstlst = []
# for i in ings: # from scraper
#     name_ret = get_ing_name(i)
#     lstlst.append(name_ret)



# stuff in front == qty, DESCRIPTOR
# stuff after == prep

fraction_match = r"(\d+[\/\d. ]*|\d)" # /g means global match
measurements = [r'([a-z]+)spoons?', r'cloves?', r'cups?', r'pounds?', r'ounces?', r'large',
r'medium', r'small', r'packs?', r'pints?', r'quarts?', r'gallons?', r'bushel', r'grams?']

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

def bbc_ingredients_from_txt():
        t = []
        for true_ing in all_ing_list: # real ings from bbc
            ing_regex_single = r'\b{0}\b'.format(true_ing)
            ing_regex_plural = r'\b{0}\b'.format(pluralize(true_ing))
            match_single = re.search(ing_regex_single, true_ing.lower())
            match_plural = re.search(ing_regex_plural, true_ing.lower())
            if match_single:
                t.append(true_ing.lower())
            elif match_plural:
                t.append(pluralize(true_ing.lower()))
        #print "HEREHEREHEREHEREHEREHERE:", t


'''
ex. get_all_names(url)[0] --> ['egg yolk', 'white sugar', 'milk', 'cream', 'vanilla extract', 'mascarpone cheese', 'coffee', 'rum', 'ladyfinger cookies', 'cocoa']
'''
def get_all_names(url):
    #scrape
    recipe = scrapeRecipe(url)
    ings = recipe[0]

    # get bbc ingredients
    all_ingredients = open("allingredients.txt", "r")
    all_ingredients = all_ingredients.read()

    lst = all_ingredients.split(',')
    all_ing_list = []
    for i in lst:
        i = i.replace('u\'', '').replace('\'', '').strip()
        all_ing_list.append(i)

    #get names
    t = []
    for true_ing in all_ing_list: # real ings from bbc
        ing_regex_single = r'\b{0}\b'.format(true_ing)
        ing_regex_plural = r'\b{0}\b'.format(pluralize(true_ing))
        match_single = re.search(re.escape(ing_regex_single), true_ing.lower())
        match_plural = re.search(re.escape(ing_regex_plural), true_ing.lower())
        if match_single:
            t.append(true_ing.lower())
        elif match_plural:
            t.append(pluralize(true_ing.lower()))
    #print "HEREHEREHEREHEREHEREHERE:", t

    seen = set()
    seen_add = seen.add
    t = [x for x in t if not (x in seen or seen_add(x))]

    t.sort(key=lambda x: len(x.split()), reverse=True)

    #print t

    names = []
    desc_and_prep = []

    name = ""
    for i in ings:
        for db_ingredient in t:
            if db_ingredient in i.lower():
                #print "HERE:", db_ingredient
                names.append(db_ingredient)
                # db_ingredient is now the name of the Ingredient
                desc_and_prep.append(i.split(db_ingredient))
                break

    return [names, desc_and_prep] #[ ['white sugar'], [[u'1 cup', u'']]]



# class Ingredient:
#     def __init__(self, ing_string):
#         self.str = ing_string
#         self.name = ""
#         self.quantity = 0
#         self.measurement = ""
#         self.descriptor = ""
#         self.preparation = ""
#         # self.name_with_descriptor = ""
#
#         # def make_ingredients():
#         #     return lst_of_ingredients

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


def print_ingredients(all_names_results): # substitution -> "vegan", "greek", etc. --> name = name[x].greek: figure out how to incorporate IngredientBook
    all_results = get_all_names(ings)
    names = all_results[0]
    other = all_results[1]
    for x in range(len(names)):
        # b = Ingredient(i)
        name = names[x]
        #print name
        qty = get_ing_quantity(other[x][0])
        #print qty
        msrmnt = get_ing_measurement(other[x][0])
        #print msrmnt
        desc = get_ing_descriptor(other[x][0])
        #print desc
        if len(other) > 1:
            prep = get_ing_preparation(other[x][1])
            #print prep
