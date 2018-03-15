from write_book import *
from parse_ingredients import *
from scraper import scrapeRecipe
from methods_tools_parser import *
from steps_parser import print_steps
def testAll(url):
	cookBook = writeBook()
	healthy = []
	vegetarian = []
	vegan = []
	greek = []
	mexican = []
	
	healthySteps = []
	vegetarianSteps = []
	veganSteps = []
	greekSteps = []
	mexicanSteps = []

	scraped = scrapeRecipe(url)

	scrapedIng = scraped[0]
	scrapedSteps = scraped[1]
	#index into the basic names
	#print(scrapedIng)
	#print(cookBook)
	basicIngredients = get_all_names_plus_fixed_rejects(scrapedIng, cookBook)[0]
	
	tools = get_tools_names(scrapedSteps)
	methods = get_methods_names(scrapedSteps)	
	stepParsed = print_steps(scrapedSteps, basicIngredients)

	for i in basicIngredients:
		healthy.append('substituted ' + str(i) + ' for ' + str(cookBook[i].healthy))
		vegetarian.append('substituted ' + str(i) + ' for ' + str(cookBook[i].vegetarian))
		vegan.append('substituted ' + str(i) + ' for ' + str(cookBook[i].vegan))
		greek.append('substituted ' + str(i) + ' for ' + str(cookBook[i].greek))
		mexican.append('substituted ' + str(i) + ' for ' + str(cookBook[i].mexican))	
	
	for i in basicIngredients:
		for s in scrapedSteps:
			healthySteps.append(re.sub(i, cookBook[i].healthy, s))
			vegetarianSteps.append(re.sub(i, cookBook[i].vegetarian, s))
			veganSteps.append(re.sub(i, cookBook[i].vegan, s))
			greekSteps.append(re.sub(i, cookBook[i].greek, s))
			mexicanSteps.append(re.sub(i, cookBook[i].mexican, s))

	transforms = [list(set(healthy)), list(set(vegetarian)), list(set(vegan)), list(set(greek)), list(set(mexican))]
	transformNames = ['healthy', 'vegetarian', 'vegan', 'greek', 'mexican']
	for counter, l in enumerate(transforms):
		print("Now showing ingredients for " + transformNames[counter] + " transformation:\n")
		if l:
			for ing in l:
				print(ing + "\n")


	stepLists = [healthySteps, vegetarianSteps, veganSteps, greekSteps, mexicanSteps]

	for l in range(0, 5):
		res = "";
		for st in stepLists[l]:
			res += (st + '\n')
		print('Here are the steps to follow for a ' + transformNames[l] + ' version of this dish: \n' + res)
