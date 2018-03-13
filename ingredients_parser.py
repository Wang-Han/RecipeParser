import re

'''
 break down ingredients
 # repo: https://github.com/tlitre/RecipeParser.git
'''

ingredients_list = ["1/8 teaspoon hot pepper sauce", "4 bone-in chicken breast halves, with skin",
"12 pounds spaghetti", "1 clove crushed garlic", "1/2 teaspoon salt", "2 1/2 cups white sugar",
"2 tablespoons melted butter", "2 1/3 teaspoons milk", "4 3/5 ounces goat milk"]

measurements = [r'([a-z]+)spoons?', r'cloves?', r'cups?', r'pounds?', r'ounces?']

fraction_match = r"(\d+[\/\d. ]*|\d)" # /g means global match

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
Input: List of full ingredients (ex. ["1/8 teaspoon hot pepper sauce", "4 3/5 ounces goat milk"])
Return: list of stripped ingredient names (ex. ["pepper sauce", "milk"])

Use this to replace ingredients in the prep directions
'''
def get_ingredient_names(ingredients_list):
    names = []
    for i in ingredients_list:
        s = find_ingredient_name(i)
        names.append(s.replace(find_ingredient_descriptor(s), "").strip())
    return names

# for i in ingredients_list:
#     print i
#     print_ingredient(i)

# print get_ingredient_names(ingredients_list)

class Ingredient:
    def __init__(self, ing_string):
        self.str = ing_string
        self.name = ""
        self.quantity = 0
        self.measurement = ""
        self.descriptor = ""
        self.preparation = ""
        self.name_with_descriptor = ""

        def find_ingredient_quantity(self, ing):
            ingredient_split_list = ing.split()
            amount = 0
            for num in ingredient_split_list:
                frac_match = re.search(fraction_match, num)
                if frac_match:
                    amount += frac_to_float(frac_match.group(0))
            return amount

        def find_ingredient_measurement(self, ing):
            ingredient_split_list = ing.split()
            measurement = ""
            no_nums_ingredient = [w for w in ingredient_split_list if not re.search(fraction_match, w)]
            i = no_nums_ingredient[0]
            measurement = i if re.search(r"(?=("+'|'.join(measurements)+r"))", i) else ""
            return measurement


        def find_ingredient_preparation(self, ing):
            ingredient_split_list = ing.split(',')
            prep = ""
            if len(ingredient_split_list) > 1:
                prep = ingredient_split_list[1]
            return prep.strip()

        def find_ingredient_name(self, ing):
            # remove meas, qty, and prep
            ingredient_split_list = ing.split()
            no_nums_ingredient = [w for w in ingredient_split_list if not re.search(fraction_match, w)]
            if find_ingredient_measurement(self, ing) in no_nums_ingredient:
                no_nums_ingredient.remove(find_ingredient_measurement(self, ing))
            name = ' '.join(no_nums_ingredient)
            # remove descriptor
            prep = find_ingredient_preparation(self, ing)
            if prep is not "":
                name = name.replace(prep, "")
            return name


        def find_ingredient_descriptor(self, name):
            n = name.split()
            descriptor = ""
            if len(n) > 1:
                descriptor = n[0]
            return descriptor

        self.name_with_descriptor = find_ingredient_name(self, self.str)
        self.quantity = find_ingredient_quantity(self, self.str)
        self.measurement = find_ingredient_measurement(self, self.str)
        self.descriptor = find_ingredient_descriptor(self, self.name_with_descriptor)
        self.preparation = find_ingredient_preparation(self, self.str)
        self.name = self.name_with_descriptor.replace(find_ingredient_descriptor(self, self.name_with_descriptor), "").strip()


    '''
Input: the ingredient string ex. "4 3/5 ounces goat milk"
Prints:
    NAME: milk
    QTY: 4.6
    MEASUREMENT: ounces
    DESCRIPTOR: goat
    PREPARATION:
Prints out ingredient info
'''
def print_ingredient(ing):
    b = Ingredient(ing)
    # i_name = find_ingredient_name(i)
    print "NAME:", b.name, "\nQTY:", b.quantity, "\nMEASUREMENT:", b.measurement, "\nDESCRIPTOR:", b.descriptor, "\nPREPARATION:", b.preparation, '\n'

for  i in ingredients_list:
    print_ingredient(i)
