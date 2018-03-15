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

	transforms = [list(set(healthy)), list(set(vegetarian)), list(set(vegan)), list(set(greek)), list(set(mexican))]
	transformNames = ['healthy', 'vegetarian', 'vegan', 'greek', 'mexican']
	for counter, l in enumerate(transforms):
		print("Now showing ingredients for " + transformNames[counter] + " transformation:\n")
		if l:
			for ing in l:
				print(ing + "\n")
	print(tools)
	print(methods)


def vegan_ingredients(url):
	after = []
	cookBook = writeBook()
	scraped = scrapeRecipe(url)
	scrapedIng = scraped[0]
	scrapedSteps = scraped[1]
	basicIngredients = get_all_names_plus_fixed_rejects(scrapedIng, cookBook)[0]
	for i in scrapedIng: # allrecipes ings
		merge = []
		qty = str(get_ing_quantity(i))
		merge.append(qty)
		msrmnt = str(get_ing_measurement(i))
		merge.append(msrmnt)
		for b in basicIngredients: # the stripped ingredients from webpage
			if b in i: # if i is the full of the basic ingredient
				merge.append(str(cookBook[b].vegan))
				transformed_ingredient = ' '.join(merge)
				print transformed_ingredient
				after.append(transformed_ingredient)
				break
	return transformed_ingredient

def healthy_ingredients(url):
	after = []
	cookBook = writeBook()
	scraped = scrapeRecipe(url)
	scrapedIng = scraped[0]
	scrapedSteps = scraped[1]
	basicIngredients = get_all_names_plus_fixed_rejects(scrapedIng, cookBook)[0]
	for i in scrapedIng: # allrecipes ings
		merge = []
		qty = str(get_ing_quantity(i))
		merge.append(qty)
		msrmnt = str(get_ing_measurement(i))
		merge.append(msrmnt)
		for b in basicIngredients: # the stripped ingredients from webpage
			if b in i: # if i is the full of the basic ingredient
				merge.append(str(cookBook[b].healthy))
				transformed_ingredient = ' '.join(merge)
				print transformed_ingredient
				after.append(transformed_ingredient)
				break
	return transformed_ingredient

def greek_ingredients(url):
	after = []
	cookBook = writeBook()
	scraped = scrapeRecipe(url)
	scrapedIng = scraped[0]
	scrapedSteps = scraped[1]
	basicIngredients = get_all_names_plus_fixed_rejects(scrapedIng, cookBook)[0]
	for i in scrapedIng: # allrecipes ings
		merge = []
		qty = str(get_ing_quantity(i))
		merge.append(qty)
		msrmnt = str(get_ing_measurement(i))
		merge.append(msrmnt)
		for b in basicIngredients: # the stripped ingredients from webpage
			if b in i: # if i is the full of the basic ingredient
				merge.append(str(cookBook[b].greek))
				transformed_ingredient = ' '.join(merge)
				print transformed_ingredient
				after.append(transformed_ingredient)
				break
	return after

def mexican_ingredients(url):
	after = []
	cookBook = writeBook()
	scraped = scrapeRecipe(url)
	scrapedIng = scraped[0]
	scrapedSteps = scraped[1]
	basicIngredients = get_all_names_plus_fixed_rejects(scrapedIng, cookBook)[0]
	for i in scrapedIng: # allrecipes ings
		merge = []
		qty = str(get_ing_quantity(i))
		merge.append(qty)
		msrmnt = str(get_ing_measurement(i))
		merge.append(msrmnt)
		for b in basicIngredients: # the stripped ingredients from webpage
			if b in i: # if i is the full of the basic ingredient
				merge.append(str(cookBook[b].mexican))
				transformed_ingredient = ' '.join(merge)
				print transformed_ingredient
				after.append(transformed_ingredient)
				break
	return after

def vegetarian_ingredients(url):
	after = []
	cookBook = writeBook()
	scraped = scrapeRecipe(url)
	scrapedIng = scraped[0]
	scrapedSteps = scraped[1]
	basicIngredients = get_all_names_plus_fixed_rejects(scrapedIng, cookBook)[0]
	for i in scrapedIng: # allrecipes ings
		merge = []
		qty = str(get_ing_quantity(i))
		merge.append(qty)
		msrmnt = str(get_ing_measurement(i))
		if qty > 1.0:
			msrmnt = pluralize(msrmnt)
		merge.append(msrmnt)
		for b in basicIngredients: # the stripped ingredients from webpage
			if b in i: # if i is the full of the basic ingredient
				sub = str(cookBook[b].vegetarian)
				merge.append(sub)
				transformed_ingredient = ' '.join(merge)
				print transformed_ingredient
				after.append(transformed_ingredient)
				break


	# for x in basicIngredients:
	# 	for i in print_parsed_ingredients(scrapedIng, cookBook):
	# 		print i
	# # 		if x in i: # if basic ingredient in full ingredient name
	# 			print re.sub(x, cookBook[x].healthy, i, 1)

# testAll("https://www.allrecipes.com/recipe/236915/lemon-buttermilk-pound-cake-with-aunt-evelyns-lemon-glaze/?internalSource=streams&referringId=276&referringContentType=recipe%20hub&clickId=st_trending_b")
# vegan_ingredients("https://www.allrecipes.com/recipe/236915/lemon-buttermilk-pound-cake-with-aunt-evelyns-lemon-glaze/?internalSource=streams&referringId=276&referringContentType=recipe%20hub&clickId=st_trending_b")

def print_original_ingredients(url):
	cookBook = writeBook()
	scraped = scrapeRecipe(url)
	scrapedIng = scraped[0]
	print "Original Ingredients:", '\n'
	print_ingredients(scrapedIng, cookBook)

def make_vegan(url):
	print '\n', "Vegan Transformation:", '\n'
	vg = vegan_ingredients(url)

def make_vegetarian(url):
	print '\n', "Vegitarian Transformation:", '\n'
	v = vegetarian_ingredients(url)

def make_mexican(url):
	print '\n', "Mexican Transformation:", '\n'
	mx = mexican_ingredients(url)

def make_greek(url):
	print '\n', "Vegan Transformation:", '\n'
	grk = greek_ingredients(url)

def make_healthy(url):
	print '\n', "Healthy Transformation:", '\n'
	h = healthy_ingredients(url)

def transform_all(url):
	make_greek(url)
	make_vegan(url)
	make_healthy(url)
	make_vegetarian(url)
	make_mexican(url)

print_original_ingredients("https://www.allrecipes.com/recipe/236915/lemon-buttermilk-pound-cake-with-aunt-evelyns-lemon-glaze/?internalSource=streams&referringId=276&referringContentType=recipe%20hub&clickId=st_trending_b")

transform_all("https://www.allrecipes.com/recipe/236915/lemon-buttermilk-pound-cake-with-aunt-evelyns-lemon-glaze/?internalSource=streams&referringId=276&referringContentType=recipe%20hub&clickId=st_trending_b")
