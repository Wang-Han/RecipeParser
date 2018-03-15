import re
from collections import Counter
from nltk.tokenize import RegexpTokenizer


''' the format of  step list returned by scraper.py'''
# steps_list = [u'Preheat oven to 350 degrees F (175 degrees C).', u'Slice the baguette into 1/2 inch thick diagonal slices. Arrange the slices in a single layer on a baking sheet. Brush both sides of each slice with the olive oil. Place tomato slices and a sprinkling of basil and oregano on the bread slices. Sprinkle the tomatoes, basil and oregano with the garlic powder and white pepper. Cover the tomato slices with slices of  the mozzarella and provolone. Place more basil, oregano and tomato slices on top of the cheese.', u'Bake in the preheated oven for 7 to 10 minutes, or until the cheese is bubbly.', u'\n\n']

verbs_to_tools_mapping = { 'cut' : 'knife', 'chop':'knife', 'dice':'knife', 'julienne':'knife', 'mince':'knife', 'minced' : 'knife', 'slice':'knife', 'fold': 'wooden spoon', 'stir':'wooden spoon', 'glaze':'spoon', 'drizzle':'spoon', 'marinate': 'bowl', 'beat':'fork', 'shred': 'food processor', 'baste': 'baster', 'basting' : 'baster', 'sift':'colander', 'cream':'hand mixer', 'grate':'grater', 'whisk':'whisk', 'peel':'peeler', 'puree':'blender', 'crush':'pestle mortar',}
tools_to_methods_mapping = { 'baking powder':'bake', 'baking soda': 'bake', 'preheat' : 'preheat', 'mixing bowl': 'mix' }
indeed_tools = ['casserole', 'knife', 'cooker', 'microwave safe bowl', 'baster', 'pan', 'peeler', 'cube tray', 'strainer', 'measuring cups', 'fruit muddler', 'freezer tray', 'plate', 'yogurt maker', 'fry pan', 'cuisinart', 'grinder', 'spatula', 'mincer', 'fork', 'hullster', 'shaker', 'grate and slice set', 'scale', 'spoon', 'press', 'whisk', 'skimmer', 'cake pan', 'foil', 'tongs', 'potato masher', 'soup ladle', 'brush', 'an opener', 'juicer press', 'floor sifter', 'pizza wheel', 'salt shaker', 'grater', 'corkscrew', 'lid', 'pepper grinder', 'bowl', 'measuring cup', 'utensil', 'egg topper', 'cheese slicer', 'scoop', 'skimmer', 'strainer', 'serve ladle', 'saute spoon', 'cutting board', 'spill stopper', 'splatter screen', 'burner', 'egg beater', 'potato ricer', 'food mill', 'grater', 'peeler', 'slicer', 'stripper', 'corn zipper', 'shear', 'snips', 'chopper', 'mandoline', 'mortar', 'pestle', 'can', 'mister', 'seal', 'stopper', 'pourer', 'scale', 'tea ball', 'timer', 'thermometer', 'board', 'baking cups', 'cloth', 'parchment roll', 'aluminium foil', 'cupcake liners', 'decorating pen', 'muffin papers', 'lifter', 'gloves', 'rack', 'rolling pin', 'skewer', 'wrangler', 'oven', 'baking pan', 'bags', 'smoother', 'sieve', 'wheel', 'shield', 'probe', 'rack', 'blender', 'scraper', 'microwave', 'lighter', 'saucepan', 'baking dish', 'plastic bag', 'paper warp', 'pan', 'dish', 'skillet', 'mixing bowl', 'frying pan', 'baking sheet', 'loaf pan', 'pot']
verbs = ['sear', 'rotisserie', 'broil', 'fry', 'grill', 'barbeque', 'poach', 'sautee', 'saute', 'pressure cook', 'steam', 'stew', 'stir-fry', 'stir fry', 'roast', 'freeze', 'mince', 'grate', 'coddle', 'blanch', 'marinate', 'skillet', 'smoke', 'microwave', 'bake', 'baste', 'boil', 'stew', 'pound', 'crush', 'squeeze', 'stir', 'mix', 'grease', 'preheat', 'melt', 'coat', 'turn', 'sprinkle', 'season', 'place', 'form', 'combine', 'add', 'blend', 'pour', 'slice', 'cook', 'reduce', 'adjust', 'spoon', 'cut', ]

# get the name of cooking tools
def get_tools_names(steps):
    res = []
    visited = []
    mp = Counter()
    tokenizer = RegexpTokenizer(r'\w+')
    for step in steps:
        step_txt = str(step)
        step_string = tokenizer.tokenize(step_txt)
        for i in range(len(step_string)):
            tool1 = step_string[i]
            if len(step_string) - 2 > i:
                tool2 = step_string[i] + ' ' + step_string[i + 1]
                tool3 = step_string[i] + ' ' + step_string[i + 1] + ' ' + step_string[i + 2]
            for tool in indeed_tools:
                if tool == tool2:
                    visited.append(step_string[i + 1])
                    mp[tool] += 1
                elif tool == tool3:
                    visited.append(step_string[i + 1])
                    visited.append(step_string[i + 2])
                    mp[tool] += 1
                elif tool not in visited and tool == tool1:
                    mp[tool] += 1
            for verb in verbs_to_tools_mapping:
                tool = verbs_to_tools_mapping[verb]
                if tool not in visited and step_string == verb:
                    mp[tool] += 1
    for tool_name in mp.most_common():
        res.append(tool_name[0])
    return res

# get the name of cooking methods
# return a list with the first list inside is the primary method, and the second one is other cooking methods
def get_methods_names(steps):
    primary_method_res = []
    other_methods_res = []
    tokenizer = RegexpTokenizer(r'\w+')
    same_meaning = ['oven', 'preheat']
    verb_suffix = ["ing", "s", "er", "ed"]
    mp = Counter()
    for step in steps:
        step_txt = str(step)
        step_string = tokenizer.tokenize(step_txt)
        for word in step_string:
            word_formal = word.lower()
            for verb in verbs:
                if word_formal == verb:
                    if verb == same_meaning[0] :
                        mp['bake'] += 2
                    elif verb == same_meaning[1]:
                        mp['bake'] += 1
                        mp[same_meaning[1]] += 1
                    else :
                        mp[verb] += 1
                elif verb[:-1] + verb_suffix[0] == word_formal:
                    # mp[verb[:-1] + verb_suffix[0]] += 1
                    mp[verb] += 1
                else :
                    for suffix in verb_suffix:
                        if word_formal == verb + suffix :
                            mp[verb] += 1
                            # mp[verb + suffix] += 1
        for i in range(0, len(step_string) - 1):
            for method in tools_to_methods_mapping:
                if step_string[i] == method or step_string[i] + ' ' + step_string[i + 1] == method:
                    mp[method] += 1

    max_number = 0
    if len(mp) > 0:
        max_number = mp.most_common(1)[0][1]
    primary_list = []
    for method, number in mp.most_common():
        if number == max_number:
            primary_list.append(method)
    primary_list.sort()
    if len(primary_list) > 0:
        primary_method_res.append(primary_list[0])
        for method in mp.most_common():
            if method[0] not in primary_method_res:
                other_methods_res.append(method[0])
    return [primary_method_res, other_methods_res]

# print get_methods_names(steps_list)