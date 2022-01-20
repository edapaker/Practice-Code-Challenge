from importlib.metadata import requires
from flask import Flask
from flask_restful import Api, Resource, reqparse
import json

app = Flask(__name__)
api = Api(app)

recipes_post_args = reqparse.RequestParser()
recipes_post_args.add_argument("name", type = str, help = "Name of recipe.", required = True)
recipes_post_args.add_argument("ingredients", type = str, action = "append", help = "List of ingredients.", required = True)
recipes_post_args.add_argument("instructions", type = str, action = "append", help = "List of instructions.", required = True)

class Recipes (Resource) : 
    def get (self) :
        with open("data.json", "r") as fptr : 
            data = json.load(fptr)

        recipe_names = [recipe["name"] for recipe in data["recipes"]]

        fptr.close()

        return {"recipeNames": recipe_names}, 200

    def post (self) :
        args = recipes_post_args.parse_args()

        with open("data.json", "r") as fptr :
            data = json.load(fptr)
        
        fptr.close()

        if args["name"] in [recipe["name"] for recipe in data["recipes"]] :
            return {"error": "Recipe already exists"}, 400

        data["recipes"].append(args)
        
        with open("data.json", "w") as fptr :
            fptr.write(json.dumps(data))

        fptr.close()

        return None, 201

    def put (self) : 
        args = recipes_post_args.parse_args()

        with open("data.json", "r") as fptr :
            data = json.load(fptr)

        fptr.close()

        if args["name"] in [recipe["name"] for recipe in data["recipes"]] :
            [data["recipes"].remove(recipe) for recipe in data["recipes"] if recipe["name"] == "butteredBagel"]
            data["recipes"].append(args)

            with open("data.json", "w") as fptr :
                fptr.write(json.dumps(data))

            fptr.close()

            return None, 204
        else :
            return {"error": "Recipe does not exist"}, 404

class Details (Resource) :
    def get (self, recipe) :
        with open("data.json", "r") as fptr :
            data = json.load(fptr)

        recipe_details = [recip for recip in data["recipes"] if recip["name"] == recipe]

        if len(recipe_details) :
            recipe_details = recipe_details[0]
            recipe_ingredients = recipe_details["ingredients"]
            recipe_steps = len(recipe_details["instructions"])

            fptr.close()

            return {"details": {"ingredients": recipe_ingredients, "numSteps": recipe_steps}}, 200
        else :
            fptr.close()

            return {}, 200

api.add_resource(Recipes, "/recipes")
api.add_resource(Details, "/recipes/details/<string:recipe>")
 
if __name__ == "__main__" :
    app.run(debug = True)