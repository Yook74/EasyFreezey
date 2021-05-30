from flask import request, jsonify, Blueprint
from werkzeug.exceptions import BadRequest, NotFound

from server.models import Recipe, db, Ingredient, RecipeIngredient

blueprint = Blueprint('recipe', __name__, url_prefix='/recipe')


@blueprint.post('')
def post_recipe():
    """
    Expects JSON describing a recipe in the following format:
    {
        name: <recipe name/title>
        text: <full text of the recipe as HTML>
        source: <a URL or other type of attribution for the recipe>
        servings: <a float specifying the number of servings>
        ingredients: [
            {
                id: <ingredient ID>
                amount: <amount of that ingredient in this recipe in recipe units>
            }
            ...
        ]
    }
    """
    new_recipe = Recipe(
        name=request.json['name'],
        text=request.json['text'],
        source=request.json['source'],
        servings=request.json['servings']
    )
    db.session.add(new_recipe)

    if len(request.json['ingredients']) == 0:
        raise BadRequest('Recipes must have at least one ingredient')

    if any(ingredient['amount'] <= 0 for ingredient in request.json['ingredients']):
        raise BadRequest('Recipe amounts must be greater than 0')

    for ingredient in request.json['ingredients']:
        if Ingredient.query.filter_by(id=ingredient['id']).first() is None:
            raise NotFound(f'No ingredient with id {ingredient["id"]} was found')

        db.session.add(RecipeIngredient(
            recipe_id=new_recipe.id,
            ingredient_id=ingredient['id'],
            amount=ingredient['amount']
        ))

    db.session.commit()
    return str(new_recipe.id)


@blueprint.get('')
def all_recipes():
    return jsonify([
        {'name': recipe.name, 'id': recipe.id, 'cost': recipe.cost}
        for recipe in Recipe.query
    ])


@blueprint.get('<int:recipe_id>')
def get_recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()

    if recipe is None:
        raise NotFound('No recipe was found with that ID')
    else:
        return jsonify({
            'name': recipe.name,
            'text': recipe.text,
            'source': recipe.source,
            'servings': recipe.servings,
            'ingredients': [
                {
                    'id': recipe_ingredient.ingredient.id,
                    'name': recipe_ingredient.ingredient.name,
                    'amount': recipe_ingredient.amount,
                    'unit': recipe_ingredient.ingredient.recipe_unit,
                }
                for recipe_ingredient in RecipeIngredient.query.filter_by(recipe_id=recipe.id)
            ]
        })
