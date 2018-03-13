from ingredients_parser import *
# healthy transform
# find healthy substitutes
# have a reasoning for making the recipe healthier
# maybe fewer calorie in ingredients

ingredient_list = ["1 cup vegetable oil for frying", "1/2 cup all-purpose flour", "salt and pepper to taste",
"4 (3/4 inch) thick pork chops", "1/2 teaspoon seasoning salt, or to taste"]

# [
# "2 tablespoons butter", "4 dashes garlic powder", "8 slices Cheddar cheese",
# "12 slices bacon", "4 pork chops", "4 dashes onion powder"
# ]

# for i in ingredient_list:
#     print_ingredient(i)

recipe_directions = ["Heat oil in a large skillet over medium-high heat. Combine flour, seasoning salt, salt and pepper in a paper or plastic bag. Place pork chops into the bag, and shake to coat.",
"When the oil is nice and hot, shake off excess flour from pork chops, and fry in the hot oil. Cook on each side for about 4 to 5 minutes, or until golden on the outside, and juices run clear."]

# ["Heat oven to 350 degrees F.", "Mix graham crumbs, butter and 1/4 cup sugar; press onto bottom of 9-inch springform pan.",
# "Beat cream cheese and remaining sugar in large bowl with mixer until blended. Add sour cream and vanilla; mix well. Add eggs, 1 at a time, beating on low speed after each addition just until blended. Pour over crust.",
# "Bake 1 hour to 1 hour 10 min. or until center is almost set. Run knife around rim of pan to loosen cake; cool before removing rim. Refrigerate cheesecake 4 hours.",
# "Top with pie filling before serving."]

# [
# "Melt butter in a skillet over medium heat. Add pork chops; season with onion and garlic powder. Cook until pork chops are no longer pink in the center, about 5 minutes per side.",
# "Transfer pork chops to a plate; top each one with 2 slices of Cheddar cheese. Place a bowl over the plate to trap in heat.",
# "Place bacon into the skillet; cook until crisp and no longer pink, about 6 minutes. Wrap 3 slices of bacon around each pork chop."
# ]

healthy_subs_dict = {
    'butter':'coconut butter',
    'whole milk':'soy milk',
    'sausage':'turkey sausage',
    'bacon':'turkey bacon',
    'sugar':'stevia',
    'philidelphia cream cheese':'silken tofu and soy milk',
    'cream cheese':'silken tofu and soy milk',
    'heavy whipping cream':'silken tofu and soy milk',
    'heavy cream':'silken tofu and soy milk',
    'whipped cream':'coconut whipped cream',
    'couscous':'quinoa',
    'noodles':'spaghetti squash',
    'bread crumbs':'ground flaxseeds',
    'croutons':'slivered almonds',
    'chocolate chips':'cacao nibs',
    'ice cream':'banana ice cream',
    'maple syrup':'agave',
    'beef':'bison',
    '':'',
    'pulled pork':'jackfruit',
    'guanciale':'turkey bacon',
    'ground beef':'ground turkey',
    'ground pork':'ground turkey',
    'bacon':'turkey bacon',
    'thigh':'breast',
    'duck':'turkey',
    'goose':'turkey',
    'beef chuck':'bison chuck',
    'beef rib':'bison rib',
    'beef brisket':'bison loin',
    'pork spareribs':'lamb ribs',
    'pork chop':'chicken breast',
    'chorizo':'turkey sausage',
    'chorizo sausage':'turkey sausage',
    'margarine':'olive oil',
    'cheddar cheese': 'parmesean cheese',
    'mozzerella': 'feta',
    # 'cream cheese':'ricotta cheese',
    'american cheese': 'cheddar cheese',
    'vegetable oil':'olive oil',
    'shortening':'olive oil',
    'soy sauce':'coconut aminos',
    'alfredo sauce':'coconut flour and olive oil roux', # roux is technically a cooking method...
    'salted':'unsalted',
    'pasta':'brown rice pasta',
    'sour cream':'greek yogurt',
    'flour tortilla':'corn tortilla',
    'all-purpose flour':'coconut flour',
    'white flour':'coconut flour',
    'white bread':'wheat bread',
    'mayonnaise':'greek yogurt',
    'eggs':'egg whites',
    'white rice':'cauliflower
}


# unhealthy_subs_dict = {
#     'skim milk':'whole milk',
#     'low-fat milk':'whole milk',
#     'low fat milk':'whole milk',
#     'wheat bread':'white bread',
#     'bread' : 'white bread',
#     'olive oil':'butter',
#
# }

healthy_techniques_subs_dict = {
    'deep-fry': 'bake',
    'fry':'bake',
    'pan fry':'bake',
    'microwave':'bake',
    'frying':'baking'
}

def to_healthy(directions_or_ingredients):
    for item in directions_or_ingredients:
        for ing_key in healthy_subs_dict:
            item = item.lower().replace(ing_key, healthy_subs_dict[ing_key])
        for tech_key in healthy_techniques_subs_dict:
            item = item.lower().replace(tech_key, healthy_techniques_subs_dict[tech_key])
        print item #.capitalize() - need to capitalize each sentence


to_healthy(recipe_directions)

to_healthy(ingredient_list)

'''
If there is an ingredient in the text, find it in the keys ingredient dict and sub it w/ the ingredient in the value

'''
