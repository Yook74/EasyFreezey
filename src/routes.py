from flask import current_app as app
from flask import jsonify
from werkzeug.exceptions import NotFound
from sqlalchemy import func

from src.models import *


@app.route('/<int:session_id>/shopping')
def shopping_list(session_id):
    ingredient_quantities = db.session.query(Ingredient, func.sum(RecipeIngredient.amount))\
        .join(RecipeIngredient).join(Recipe).join(RecipientSessionRecipe)\
        .filter(RecipientSessionRecipe.session_id == session_id).group_by(Ingredient.id)

    return jsonify([
        {
            'name': ingredient.name,
            'unit': ingredient.store_unit,
            'qty': quantity / ingredient.unit_conversion
        } for ingredient, quantity in ingredient_quantities
    ])
