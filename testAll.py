from write_book import *
from parse_ingredients import *
from scraper import scrapeRecipe
from methods_tools_parser import *

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
	#print(scrapedIng)
	#print(cookBook)
	basicIngredients = get_all_names(scrapedIng, cookBook)[0]
	
	tools = get_tools_names(scrapedSteps)
	methods = get_methods_names(scrapedSteps)	
		
	for i in basicIngredients:
		healthy.append('substituted ' + str(i) ' for ' + str(cookBook[i].healthy))
		vegetarian.append('substituted ' + str(i) ' for ' + str(cookBook[i].vegetarian))
		vegan.append('substituted ' + str(i) ' for ' + str(cookBook[i].vegan))
		greek.append('substituted ' + str(i) ' for ' + str(cookBook[i].greek))
		mexican.append('substituted ' + str(i) ' for ' + str(cookBook[i].mexican)	

	transforms = [healthy, vegetarian, vegan, greek, mexican]
	
	for l in transforms:
		print("Now showing ingredients for  transformation:\n")
		if l:
			for ing in l:
				print(ing + "\n")
	
