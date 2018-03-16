import re
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from methods_tools_parser import *

# steps_list = [u'Preheat oven to 350 degrees F (175 degrees C).', u'Slice the baguette into 1/2 inch thick diagonal slices. Arrange the slices in a single layer on a baking sheet. Brush both sides of each slice with the olive oil. Place tomato slices and a sprinkling of basil and oregano on the bread slices. Sprinkle the tomatoes, basil and oregano with the garlic powder and white pepper. Cover the tomato slices with slices of  the mozzarella and provolone. Place more basil, oregano and tomato slices on top of the cheese.', u'Bake in the preheated oven for 7 to 10 minutes, or until the cheese is bubbly.', u'\n\n']


def get_steps_info(steps, basicIngredients) :
    all_steps_res = []
    cnt = 1
    for step in steps:
        step_list = []
        step_list.append(step)
        step_txt = str(step)
        if len(step_txt) > 2:
            each_step_info = {}
            step_num_list = []
            step_num_list.append(str(cnt))
            each_step_info['Step'] = step_num_list
            each_step_info['Ingredients'] = get_steps_ingredients(step, basicIngredients)
            each_step_info['Tools'] = get_tools_names(step_list)
            methods_res = get_methods_names(step_list)
            each_step_info['Primary Cooking Methods'] = methods_res[0]
            each_step_info['Other Cooking Methods'] = methods_res[1]
            each_step_info['Time'] = get_steps_time(step)
            cnt += 1
            all_steps_res.append(each_step_info)
    return all_steps_res


def get_steps_ingredients(step, basicIngredients) :
    
    step_ingredients = []
    tokenizer = RegexpTokenizer(r'\w+')
    step_txt = str(step)
    step_string = tokenizer.tokenize(step_txt)
    visited = []
    for i in range(len(step_string)):
        if i + 1 < len(step_string):
            word2 = step_string[i] + ' ' + step_string[i + 1]
            if word2 in basicIngredients and step_string[i] not in visited:
                step_ingredients.append(word2)
                visited.append(step_string[i])
                visited.append(step_string[i + 1])
        elif i + 1 < len(step_string):
            word3 = step_string[i] + ' ' + step_string[i + 1] + ' ' + step_string[i + 2]
            if word3 in basicIngredients and step_string[i] not in visited:
                step_ingredients.append(word3)
                visited.append(step_string[i])
                visited.append(step_string[i + 1])
                visited.append(step_string[i + 2])
        elif step_string[i] in basicIngredients:
            step_ingredients.append(step_string[i])
            visited.append(step_string[i])
    return step_ingredients
    '''
    stepIngredients = []
    for i in basicIngredients:
        print(i)
	print(step)
	res = re.search(i, step)
        if(res):
            stepIngredients.append(res.group(0))
    return stepIngredients
    '''

def get_steps_time(step):
    step_time = []
    tokenizer = RegexpTokenizer(r'\w+')
    step_txt = str(step)
    step_string = tokenizer.tokenize(step_txt)
    time_units = ['min', 'min.', 'minutes', 'minute', 'hour', 'hours', 'hr', 'hrs', 'hr.', 'hrs.']
    time_string = " "
    last_index = -1
    for i in range(0, len(step_string) - 2):
        if i > last_index and i + 3 < len(step_string) and step_string[i].isdigit() and step_string[i + 1] == 'to' and step_string[i + 2].isdigit() and step_string[i + 3] in time_units:
            time_string += step_string[i] + ' ' + step_string[i + 1] + ' ' + step_string[i + 2] + ' ' + step_string[i + 3] + ' '
            last_index = i + 3
        elif i > last_index and step_string[i].isdigit() and step_string[i + 1] in time_units:
            time_string += step_string[i] + ' ' + step_string[i + 1] + ' '
            last_index = i + 1
    step_time.append(time_string)
    return step_time

# basicIngredients = ["olive oil", "baguette", "ground white pepper", "provolone cheese", "garlic powder", "oregano", "mozzarella cheese", "basil", "roma tomatoes", "provolone cheese", "mozzarella cheese"]
# dics = get_steps_info(steps_list, basicIngredients)

def print_steps(steps, basicIngredients):
    dics = get_steps_info(steps, basicIngredients)
    output = ['Step', 'Ingredients', 'Tools', 'Primary Cooking Methods', 'Other Cooking Methods', 'Time']
    for dic in dics:
        for item in output:
        	priStr = ""
		for i in dic[item]:
			priStr += (i + ' ')
		print item + ": " + priStr    

# print_steps(steps_list, basicIngredients)

