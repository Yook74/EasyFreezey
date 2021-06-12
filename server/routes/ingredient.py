from flask import request, jsonify, Blueprint
from werkzeug.exceptions import NotFound

from server.models import Ingredient, db

blueprint = Blueprint('ingredient', __name__, url_prefix='/ingredient')


@blueprint.post('')
def post_ingredient():
    """
    Expects JSON describing an ingredient. The JSON object should have the following keys:
    name: a descriptive name for the ingredient
    aisleId: ID of the aisle for this ingredient
    recipeUnit: the unit you would use to measure this ingredient in a recipe, eg "tsp"
    storeUnit: the unit that a store would sell this ingredient in, eg "oz"
    unitConversion: the ratio of storeUnit to recipeUnit. Usually >= 1
    storeUnitPrice: the price of one storeUnit at a store like Costco
    """
    ingredient = Ingredient(
        name=request.json['name'],
        aisle_id=request.json['aisleId'],
        recipe_unit=request.json['recipeUnit'],
        store_unit=request.json['storeUnit'],
        unit_conversion=request.json['unitConversion'],
        store_unit_price=request.json['storeUnitPrice']
    )
    db.session.add(ingredient)
    db.session.commit()
    return str(ingredient.id)


@blueprint.get('')
def all_ingredients():
    return jsonify([
        {'name': ingredient.name, 'id': ingredient.id}
        for ingredient in Ingredient.query
    ])


@blueprint.get('<int:ingredient_id>')
def get_ingredient(ingredient_id: int):
    ingredient = Ingredient.query.filter_by(id=ingredient_id).first()

    if ingredient is None:
        raise NotFound('No ingredient exists with that ID')
    else:
        return jsonify({
            'name': ingredient.name,
            'aisle': ingredient.aisle.name,
            'recipeUnit': ingredient.recipe_unit,
            'storeUnit': ingredient.store_unit,
            'unitConversion': ingredient.unit_conversion,
            'storeUnitPrice': ingredient.store_unit_price
        })
