class IngredientBook:
	#define the substitution for each transformation we're doing
	name = "";
	healthy = "";
	vegetarian = "";
	vegan = "";
	mexican = "";
	greek = "";

	def __init__(self, name, healthy, vegetarian, vegan, mexican, greek):
        	self.name = name
        	self.healthy = healthy
        	self.vegetarian = vegetarian
        	self.vegan = vegan
        	self.mexican = mexican
        	self.greek = greek
