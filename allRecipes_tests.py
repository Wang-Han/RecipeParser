from write_book import * 
from edit_parser import *
import requests
from time import sleep
def testIngredients(startNum, recipeCount):
	failedIngredients = []
	ingredientBook = writeBook().keys()
	
	for i in range(startNum, recipeCount + startNum):
		url = 'https://www.allrecipes.com/recipe/' + str(i)
		page = requests.get(url)
		if page.status_code == 200:
			ingredients = get_all_names(url)[0]
			if ingredients:
				for n in ingredients:
					if n not in ingredientBook:
						failedIngredients.append(n)
		sleep(4)
	print(failedIngredients)

testIngredients(8740, 10)			
