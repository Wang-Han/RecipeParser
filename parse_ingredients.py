from scraper import scrapeRecipe
import re
from pattern.en import pluralize

# using for testing because allrecipes got mad
ings = [u'6 egg yolks', u'3/4 cup white sugar', u'2/3 cup milk',
 u'1 1/4 cups heavy cream', u'1/2 teaspoon vanilla extract', u'1 pound mascarpone cheese',
  u'1/4 cup strong brewed coffee, room temperature', u'2 tablespoons rum',
  u'2 (3 ounce) packages ladyfinger cookies', u'1 tablespoon unsweetened cocoa powder', u'2 cups rose water chilled']

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

'''
ex. get_all_names(recipe_ingredient_list_from_scraper, ingredient_book) -->
['egg yolk', 'white sugar', 'milk', 'cream', 'vanilla extract', 'mascarpone cheese', 'coffee', 'rum', 'ladyfinger cookies', 'cocoa']
'''
def get_all_names(ings, ingredient_book):
    #scrape
    # recipe = scrapeRecipe(url)
    # ings = recipe[0]
    ings = map(lambda x:x.lower(), ings)

    # get bbc ingredients
    # all_ingredients = open("new_ing.txt", "r")
    # all_ingredients = all_ingredients.read()

    all_ingredients = ingredient_book.keys()

    # lst = all_ingredients.split(',')
    # all_ing_list = []
    # for i in lst:
    #     i = i.replace('u\'', '').replace('\'', '').strip()
    #     all_ing_list.append(i)

    #get names
    t = []
    rejected = []
    for true_ing in all_ingredients: # real ings from bbc
        ing_regex_single = r'\b{0}\b'.format(true_ing)
        ing_regex_plural = r'\b{0}\b'.format(pluralize(true_ing))
        match_single = re.search(ing_regex_single, true_ing.lower())
        match_plural = re.search(ing_regex_plural, true_ing.lower())
        if match_single:
            t.append(true_ing.lower())
        elif match_plural:
            t.append(pluralize(true_ing.lower()))
        # else:
        #     rejected.append(true_ing.lower())

    seen = set()
    seen_add = seen.add
    t = [x for x in t if not (x in seen or seen_add(x))]

    t.sort(key=lambda x: len(x.split()), reverse=True)

    names = []
    desc_and_prep = []

    for i in ings:
        for db_ingredient in t:
            if db_ingredient in i.lower():
                names.append(db_ingredient)
                # db_ingredient is now the name of the Ingredient
                desc_and_prep.append(i.split(db_ingredient))
                break
        else:
            rejected.append(i)


    return [names, desc_and_prep, rejected] #[ ['white sugar'], [[u'1 cup', u'']]]

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
    return measurement.lower()

def get_ing_descriptor(ing_front):
    ingredient_split_list = ing_front.split()
    descriptor = ""
    no_nums_ingredient = [w for w in ingredient_split_list if not re.search(fraction_match, w)]
    no_nums_ingredient = map(lambda x:x.lower(), no_nums_ingredient)
    m = get_ing_measurement(ing_front).lower()
    descriptor = ' '.join(no_nums_ingredient).replace(m, '').strip()
    return descriptor.strip()

def get_ing_preparation(ing_back):
    return ing_back.strip()


'''
input: allrecipes url
output: prints -->
N: parmesan cheese
Q: 0.25
M: cup
D: grated
P:
"
'''
def print_ingredients(ings):
    # recipe = scrapeRecipe(url)
    # ings = recipe[0]
    all_results = get_all_names(ings, "")
    names = all_results[0]
    desc_and_preps = all_results[1]
    for x in range(len(names)):
        name = names[x]
        print "N:", name
        qty = get_ing_quantity(desc_and_preps[x][0])
        print "Q:", qty
        msrmnt = get_ing_measurement(desc_and_preps[x][0])
        print "M:", msrmnt
        desc = get_ing_descriptor(desc_and_preps[x][0])
        print "D:", desc
        if len(desc_and_preps[x]) > 1:
            prep = get_ing_preparation(desc_and_preps[x][1])
            print "P:", prep
        print '\n'

'''
input: allrecipes url
output:
{'olive oil': {'preparation': u'', 'descriptor': u'', 'measurement': u'tablespoon', 'name': 'olive oil', 'quantity': 1.0}, 'parmesan cheese': {'preparation': u'', 'descriptor'
: u'grated', 'measurement': u'cup', 'name': 'parmesan cheese', 'quantity': 0.25}, etc.}
use: ex. quantity of parmesan in : p["parmesan cheese"]["quantity"] --> 0.25
'''

def parse_ingredients(ings, ingredient_book):
    # recipe = scrapeRecipe(url)
    # ings = recipe[0]
    all_results = get_all_names(ings, "")
    names = all_results[0]
    desc_and_preps = all_results[1]

    all_parsed_ings = {}

    for x in range(len(names)):
        parsed = {"name":"", "quantity":"", "measurement":"", "descriptor":"", "preparation":""}
        name = names[x]
        parsed["name"] = name
        qty = get_ing_quantity(desc_and_preps[x][0])
        parsed["quantity"] = qty
        msrmnt = get_ing_measurement(desc_and_preps[x][0])
        parsed["measurement"] = msrmnt
        desc = get_ing_descriptor(desc_and_preps[x][0])
        parsed["descriptor"] = desc
        if len(desc_and_preps[x]) > 1:
            prep = get_ing_preparation(desc_and_preps[x][1])
            parsed["preparation"] = prep
        all_parsed_ings[name] = parsed
    print all_parsed_ings
    return all_parsed_ings


def fix_rejects(rejects, ingredient_book):
    for r in rejects:
        r_split = r.split()
        r_split = [w for w in r_split if not re.search(fraction_match, w)] # take out nums
        print r_split

a = get_all_names(ings, "")
# all_names = a[0]
# print all_names
# print_ingredients(ings, ingredient_book)
# p = parse_ingredients(ings, ingredient_book)
# print p["coffee"]
print "REJECTED:", a[2]

fix_rejects(a[2], "")
