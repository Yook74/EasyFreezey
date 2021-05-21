from datetime import date
from difflib import SequenceMatcher

from flask import current_app as app
from flask import jsonify, request
from werkzeug.exceptions import NotFound, BadRequest
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from src.models import *


def validate_session_id(session_id: int):
    if Session.query.filter_by(id=session_id).count() == 0:
        raise NotFound(f'No session was found with ID {session_id}.')


@app.route('/<int:session_id>/shopping', methods=['GET'])
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


@app.route('/<int:session_id>/recipe', methods=['GET'])
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


@app.route('/<int:session_id>/recipient', methods=['GET'])
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


@app.route('/recipe', methods=['POST'])
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


@app.route('/recipe', methods=['GET'])
def all_recipes():
    return jsonify([
        {'name': recipe.name, 'id': recipe.id, 'cost': recipe.cost}
        for recipe in Recipe.query
    ])


@app.route('/recipe/<int:recipe_id>', methods=['GET'])
def get_recipes(recipe_id):
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


@app.route('/ingredient', methods=['POST'])
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


@app.route('/ingredient', methods=['GET'])
def all_ingredients():
    return jsonify([
        {'name': ingredient.name, 'id': ingredient.id}
        for ingredient in Ingredient.query
    ])


@app.route('/ingredient/<int:ingredient_id>', methods=['GET'])
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


@app.route('/aisle', methods=['POST'])
def post_aisle():
    """
    Expects JSON describing an aisle. An aisle is a generic area of a store.
    For example, "canned goods" would be an aisle even if a store actually has multiple canned goods aisles.
    The JSON object should have just one key: name.
    """
    new_aisle = Aisle(name=request.json['name'])
    for existing_aisle in Aisle.query:
        if SequenceMatcher(a=existing_aisle.name, b=new_aisle.name).ratio() > .7:
            raise BadRequest(f'The given name is too similar to an existing aisle name: {existing_aisle.name}')

    db.session.add(new_aisle)
    db.session.commit()
    return str(new_aisle.id)


@app.route('/aisle', methods=['GET'])
def all_aisles():
    return jsonify([
        {'name': aisle.name, 'id': aisle.id}
        for aisle in Aisle.query
    ])


@app.route('/signup', methods=['POST'])
def post_signup():
    """
    A signup is a combination of a recipe, a recipient, a session, and a number of meals.
    It basically says "this recipient wants this many of this recipe for this session".
    Expects a JSON object with the keys recipeId, recipientId, sessionId, and mealCount.
    mealCount is the number of made recipes that the recipient wants as a float.
    """
    signup = RecipientSessionRecipe(
        recipient_id=request.json['recipientId'],
        session_id=request.json['sessionId'],
        recipe_id=request.json['recipeId'],
        meal_count=request.json['mealCount']
    )
    db.session.add(signup)
    db.session.commit()
    return 'created signup'


@app.route('/session', methods=['POST'])
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


@app.route('/session', methods=['GET'])
def all_sessions():
    return jsonify([
        {'id': session.id, 'date': session.date}
        for session in Session.query
    ])
