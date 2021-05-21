from datetime import date

from flask import jsonify, request, Blueprint
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from src.models import *
from src.routes.helpers import validate_session_id

blueprint = Blueprint('session', __name__)


@blueprint.route('/<int:session_id>/shopping', methods=['GET'])
def shopping_list(session_id):
    """
    :param session_id: The ID of the desired session. TODO potentially read this from a cookie or other storage
    :return: Json describing a shopping list for the given session.
        That is, all the ingredients needed to make this session's recipes.
    """
    validate_session_id(session_id)

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


@blueprint.route('/<int:session_id>/recipe', methods=['GET'])
def session_recipes(session_id):
    """
    :param session_id: The ID of the desired session. TODO potentially read this from a cookie or other storage
    :return: JSON describing all of the recipes for this session, including how many instances of each recipe are needed
    """
    validate_session_id(session_id)

    recipes = db.session.query(Recipe, func.sum(RecipientSessionRecipe.meal_count))\
        .join(RecipientSessionRecipe)\
        .filter(RecipientSessionRecipe.session_id == session_id).group_by(Recipe.id)

    return jsonify([
        {
            'id': recipe.id,
            'name': recipe.name,
            'totalMeals': total_meals
        } for recipe, total_meals in recipes
    ])


@blueprint.route('/<int:session_id>/recipient', methods=['GET'])
def session_recipients(session_id):
    """
    :param session_id: The ID of the desired session. TODO potentially read this from a cookie or other storage
    :return: JSON describing all the recipients of meals in this session and what meals they will be receiving
    """
    validate_session_id(session_id)

    out = []
    for recipient in Recipient.query.all():
        meals = db.session.query(Recipe, RecipientSessionRecipe.meal_count)\
            .join(Recipe)\
            .filter(RecipientSessionRecipe.session_id == session_id)\
            .filter(RecipientSessionRecipe.recipient_id == recipient.id).all()

        if meals:
            out.append({
                'name': recipient.name,
                'phone': recipient.phone,
                'email': recipient.email,
                'meals': [{'name': recipe.name, 'count': meal_count} for recipe, meal_count in meals]
            })

    return jsonify(out)


@blueprint.route('/session', methods=['POST'])
def post_session():
    """
    Expects JSON data containing just one key: "date".
    The value for date should be an ISO format string giving the approximate date of this cooking/packing session.
    """
    try:
        session = Session(
            date=date.fromisoformat(request.json['date'])
        )
        db.session.add(session)
        db.session.commit()

    except IntegrityError as exc:
        raise BadRequest(f'There is already a session at the given date. (error: {exc.args[0]})')

    else:
        return str(session.id)


@blueprint.route('/session', methods=['GET'])
def all_sessions():
    return jsonify([
        {'id': session.id, 'date': session.date}
        for session in Session.query
    ])
