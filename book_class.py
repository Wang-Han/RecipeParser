class IngredientBook():
	#define the substitution for each transformation we're doing
	name = ""
	healthy = ""
	vegetarian = ""
	vegan = ""
	mexican = ""
	greek = ""

	def __init__(self, name, healthy, vegetarian, vegan, mexican, greek):
        	if not healthy:
			healthy = name
		if not vegetarian:
			vegetarian = name
		if not vegan:
			vegan = name
		if not mexican:
			mexican = name
		if not greek:
			greek = name
		
		self.name = name
        	self.healthy = healthy
        	self.vegetarian = vegetarian
        	self.vegan = vegan
        	self.mexican = mexican
        	self.greek = greek
