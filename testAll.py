from write_book import *
from parse_ingredients.py import *
from scraper import scrapeRecipe

def testAll(url):
	cookBook = writeBook()
	healthy = []
	vegetarian = []
	vegan = []
	greek = []
	mexican = []
	
	scraped = scrapeRecipe(url)

	scrapedIng = scraped[0]
	scrapedSteps = scraped[1]
	#index into the basic names
	basicIngredients = get_all_names(scrapedIng)[0]
	
	for i in basicIngredients:
		healthy.append(cookBook[i].healthy)
		vegetarian.append(cookBook[i].vegetarian)
		vegan.append(cookBook[i].vegan)
		greek.append(cookBook[i].greek)
		mexican.append(cookBook[i].mexican)	

	transforms = list(healthy, vegetarian, vegan, greek, mexican)
	
	for l in transforms:
		print("Now showing ingredients for " + str(l) + " transformation:\n"
		for ing in l:
			print(ing + "\n")
