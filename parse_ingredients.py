from scraper import scrapeRecipe
import re
from pattern.en import pluralize

# using for testing because allrecipes got mad
ings = [u'6 egg yolks', u'3/4 cup white sugar', u'2/3 cup milk',
 u'1 1/4 cups heavy cream', u'1/2 teaspoon vanilla extract', u'1 pound mascarpone cheese',
  u'1/4 cup strong brewed coffee, room temperature', u'2 tablespoons rum',
  u'2 (3 ounce) packages ladyfinger cookies', u'1 tablespoon unsweetened cocoa powder',
  u'2 cups rose water chilled', u'1 cup shiitake chopped']

ingredient_book = {}

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

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

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
    # all_i = open("new_ing.txt", "r")
    # all_i = all_i.read()

    all_ingredients = ingredient_book.keys()

    # lst = all_i.split(',')
    # all_ingredients = []
    # for i in lst:
    #     i = i.replace('u\'', '').replace('\'', '').strip()
    #     all_ingredients.append(i)

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
def print_ingredients(ings, ingredient_book):
    # recipe = scrapeRecipe(url)
    # ings = recipe[0]
    all_results = get_all_names_plus_fixed_rejects(ings, ingredient_book)
    names = all_results[0]
    desc_and_preps = all_results[1]
    for x in range(len(names)):
        name = names[x]
        print "Name:", name
        qty = get_ing_quantity(desc_and_preps[x][0])
        print "Quantity:", qty
        msrmnt = get_ing_measurement(desc_and_preps[x][0])
        print "Measurement:", msrmnt
        desc = get_ing_descriptor(desc_and_preps[x][0])
        print "Descriptor:", desc
        if len(desc_and_preps[x]) > 1:
            prep = get_ing_preparation(desc_and_preps[x][1])
            print "Preparation:", prep
        print '\n'

'''
input: ings (recipe ings), ingredient_book(full ing dict)
output:
{'olive oil': {'preparation': u'', 'descriptor': u'', 'measurement': u'tablespoon', 'name': 'olive oil', 'quantity': 1.0}, 'parmesan cheese': {'preparation': u'', 'descriptor'
: u'grated', 'measurement': u'cup', 'name': 'parmesan cheese', 'quantity': 0.25}, etc.}
use: ex. quantity of parmesan in : p["parmesan cheese"]["quantity"] --> 0.25
'''

def parse_ingredients(ings, ingredient_book):
    # recipe = scrapeRecipe(url)
    # ings = recipe[0]
    all_results = get_all_names(ings, ingredient_book)
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
    # print all_parsed_ings
    return all_parsed_ings


def fix_rejects(rejects, ingredient_book):
    fixed = []
    for r in rejects:
        r_split = r.split()
        # r_split = [w for w in r_split if not re.search(fraction_match, w)] # take out nums
        # print r_split
        # get bbc ingredients
        # all_i = open("new_ing.txt", "r")
        # all_i = all_i.read()

        all_ingredients = ingredient_book.keys()

        # lst = all_i.split(',')
        # all_ingredients = []
        # for i in lst:
        #     i = i.replace('u\'', '').replace('\'', '').strip()
        #     all_ingredients.append(i)

        t = []
        for true_ing in all_ingredients: # real ings from bbc
            ing_regex_single = r'\b{0}\b'.format(true_ing)
            ing_regex_plural = r'\b{0}\b'.format(pluralize(true_ing))
            match_single = re.search(ing_regex_single, true_ing.lower())
            match_plural = re.search(ing_regex_plural, true_ing.lower())
            if match_single:
                t.append(true_ing.lower())
            elif match_plural:
                t.append(pluralize(true_ing.lower()))

        full_name = []
        for s in r_split: # word in rejected ingredient
            match_flag = False
            for i in t: # i in ing_book_keys
                s_regex_single = r'\b{0}\b'.format(s)
                s_regex_plural = r'\b{0}\b'.format(pluralize(s))
                match_single = re.search(s_regex_single, i.lower())
                match_plural = re.search(s_regex_plural, i.lower())
                if match_single:
                    match_flag = True
                    full_name.append(i)
                    # fixed.append(i)
                elif match_plural:
                    match_flag = True
                    full_name.append(i)
                    # fixed.append(i)
                else:
                    if s not in full_name:
                        full_name.append(s)

            if match_flag:
                break
        f = ' '.join(full_name)
        full_name_result = ' '.join(unique_list(f.split()))
        fixed.append(full_name_result)
    return fixed


'''
pretty much exactly like get_all_names, except this allows us
to include ingredients that we don't have in our db
returns:
index 0 --> list of ingredient names
1 --> desc_and_prep
2 --> rejected stuff
3 --> merged list of ingredients including rejects
'''
def get_all_names_plus_fixed_rejects(ings, ingredient_book):
    a = get_all_names(ings, ingredient_book)

    b = fix_rejects(a[2], ingredient_book)

    merge_list = ings + b

    c = get_all_names(merge_list, ingredient_book)
    c.append(merge_list)
    return c

# d = get_all_names_plus_fixed_rejects(ings, "")
#
# # print d[0], '\n'
# # print d[1], '\n'
# # print d[3]
#
# e = parse_ingredients(d[3], ingredient_book)
# print e["rose wine"]

def print_parsed_ingredients(ings, ingredient_book):
    parsed = []
    ing_dict = parse_ingredients(get_all_names_plus_fixed_rejects(ings, ingredient_book)[3], ingredient_book)
    for k in ing_dict.keys():
        b = "{0} {1} {2} {3} {4}\n".format(ing_dict[k]["quantity"], ing_dict[k]["measurement"], ing_dict[k]["descriptor"], ing_dict[k]["name"], ing_dict[k]["preparation"])
        c = ' '.join(b.split())
        parsed.append(c)
    # for i in parsed:
    #     print i
    return parsed

# print_parsed_ingredients(d[3], ingredient_book)
