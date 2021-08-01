from datetime import date

from flask import jsonify, request, Blueprint
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, NotFound

from server.models import *
from server.routes.helpers import validate_session_id

blueprint = Blueprint('session', __name__, url_prefix='/session')


@blueprint.get('/<int:session_id>/shopping')
def shopping_list(session_id):
    """
    :param session_id: The ID of the desired session. TODO potentially read this from a cookie or other storage
    :return: Json describing a shopping list for the given session.
        That is, all the ingredients needed to make this session's recipes.
    """
    validate_session_id(session_id)

    # Total amount of ingredient needed = Σ number of meals in a particular signup * amount of ingredient in that recipe
    ingredient_amounts = \
        db.session.query(Ingredient, func.sum(RecipientSessionRecipe.meal_count * RecipeIngredient.amount))\
        .join(RecipeIngredient).join(Recipe).join(RecipientSessionRecipe)\
        .filter(RecipientSessionRecipe.session_id == session_id)\
        .group_by(Ingredient.id)\
        .order_by(Ingredient.aisle_id)

    return jsonify([
        {
            'name': ingredient.name,
            'unit': ingredient.store_unit,
            'aisle': ingredient.aisle.name,
            'qty': total_ingredient_amount / ingredient.unit_conversion
        } for ingredient, total_ingredient_amount in ingredient_amounts
    ])


@blueprint.get('/<int:session_id>/recipe')
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


@blueprint.get('/<int:session_id>/recipient')
def session_recipients(session_id):
    """
    :param session_id: The ID of the desired session. TODO potentially read this from a cookie or other storage
    :return: JSON describing all the recipients of meals in this session and what meals they will be receiving
    """
    validate_session_id(session_id)

    out = []
    for recipient in Recipient.query:
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


@blueprint.post('')
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

    except (ValueError, TypeError) as exc:
        raise BadRequest(exc.args[0])

    else:
        return str(session.id)


@blueprint.get('')
def all_sessions():
    return jsonify([
        {'id': session.id, 'date': session.date.isoformat()}
        for session in Session.query
    ])


@blueprint.get('<int:session_id>')
def get_session(session_id):
    session = Session.query.filter_by(id=session_id).first()

    if session is None:
        raise NotFound('No session was found with that ID')
    else:
        recipients = Recipient.query.join(RecipientSessionRecipe).filter(RecipientSessionRecipe.session_id == session_id)
        return jsonify({
            'date': session.date.isoformat(),
            'recipientNames': [recipient.name for recipient in recipients]
        })
