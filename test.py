import requests

BASE = "http://127.0.0.1:5000/"

new_recipe = {
	"name": "butteredBagel", 
		"ingredients": [
			"1 bagel", 
			"butter"
		], 
	"instructions": [
		"cut the bagel", 
		"spread butter on bagel"
	] 
} 

mod_recipe = {
	"name": "butteredBagel", 
		"ingredients": [
			"1 bagel", 
			"2 tbsp butter"
		], 
	"instructions": [
		"cut the bagel", 
		"spread butter on bagel"
	] 
}

# response = requests.post(BASE + "recipes", new_recipe)
# response = requests.get(BASE + "recipes/details/butteredBagel")
response = requests.put(BASE + "recipes", mod_recipe)
print(response.json())