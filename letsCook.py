from testAll import *
from steps_parser import print_steps
from methods_tools_parser import *
from scraper import scrapeRecipe
from write_book import *
from parse_ingredients import *

def transformIt(url):
	which = ['healthy', 'vegetarian', 'vegan', 'mexican', 'greek']
	choice = raw_input('\nWhich transform would you like to see?\nType in healthy, vegetarian, vegan, mexican, or greek!\n')
	while(choice not in which):
		choice = raw_input('\nSorry, it looks like that we haven\'t implemented that one yet.\n Try typing in healthy, vegetarian, vegan, mexican, or greek!\n')
	print('Your ' + choice + ' transformation is coming right up!\n')
	if choice == 'healthy':
		make_healthy(url)
	elif choice == 'vegetarian':
		make_vegetarian(url)
	elif choice == 'vegan':
		make_vegan(url)
	elif choice == 'mexican':
		make_mexican(url)
	elif choice == 'greek':
		make_greek(url)	
	repeater = raw_input('\n\nWould you like to do another one? (y/n)\n')
	if(repeater == 'y' or 'yes'):
		transformIt(url)


url = raw_input('Hello and welcome to SomeRecipes.com!\nTo start out, please input a recipe url from AllRecipes:\n')
while(not re.search('allrecipes.com/recipe/', url)):
	url = raw_input('Uh-oh, it looks like that\s isn\'t a valid url\nTry again with a url from AllRecipes!\n')
answer = raw_input('\nThanks! Now do you want some info about that recipe?\n Otherwise we\'ll jump straight to transformations. (y/n)\n')
if(answer == 'y' or 'yes'):
	print("Cool! Here's some more info on it:\n")
	print_original_ingredients(url)
	scraped = scrapeRecipe(url)
	cookBook = writeBook()
	scrapedIng = scraped[0]
	scrapedSteps = scraped[1]
	basicIngredients = get_all_names_plus_fixed_rejects(scrapedIng, cookBook) 
	print_steps(scrapedSteps, basicIngredients)
	print_tools(scrapedSteps)
	print_methods(scrapedSteps)
print('\n\nLet\'s move on to some transformations!\n')
transformIt(url)
print('Okay then. Thanks for using SomeRecipes, come back soon!')
