from flask import current_app as app
from flask import jsonify
from werkzeug.exceptions import NotFound
from sqlalchemy import func

from src.models import *


@app.route('/<int:session_id>/shopping')
def shopping_list(session_id):
    """
    :param session_id: The ID of the desired session. TODO potentially read this from a cookie or other storage
    :return: Json describing a shopping list for the given session.
        That is, all the ingredients needed to make this session's recipes.
    """
    ingredient_quantities = db.session.query(Ingredient, func.sum(RecipeIngredient.amount))\
        .join(RecipeIngredient).join(Recipe).join(RecipientSessionRecipe)\
        .filter(RecipientSessionRecipe.session_id == session_id).group_by(Ingredient.id).order_by(Ingredient.aisle_id)

    return jsonify([
        {
            'name': ingredient.name,
            'unit': ingredient.store_unit,
            'aisle': ingredient.aisle.name,
            'qty': quantity / ingredient.unit_conversion,
        } for ingredient, quantity in ingredient_quantities
    ])
