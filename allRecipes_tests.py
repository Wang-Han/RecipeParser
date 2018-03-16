from write_book import * 
from parse_ingredients import *
import requests
from time import sleep
def testIngredients(startNum, recipeCount):
	failedIngredients = []
	cookBook = writeBook()
	ingredientBook = cookBook.keys()
	
	for i in range(startNum, recipeCount + startNum):
		url = 'https://www.allrecipes.com/recipe/' + str(i)
		page = requests.get(url)
		if page.status_code == 200:
			ingredients = get_all_names(url, cookBook)[0]
			if ingredients:
				for n in ingredients:
					print('Now Testing: ' + n)
					if n not in ingredientBook:
						failedIngredients.append(n)
		sleep(2)
	print(failedIngredients)

testIngredients(213717, 50)			
