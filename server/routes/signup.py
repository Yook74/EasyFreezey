from flask import request, Blueprint
from werkzeug.exceptions import NotFound, BadRequest

from server.models import db, RecipientSessionRecipe, Recipient, Session, Recipe

blueprint = Blueprint('signup', __name__, url_prefix='/signup')


@blueprint.post('')
def post_signup():
    """
    A signup is a combination of a recipe, a recipient, a session, and a number of meals.
    It basically says "this recipient wants this many of this recipe for this session".
    Expects a JSON object with the keys recipeId, recipientId, sessionId, and mealCount.
    mealCount is the number of made recipes that the recipient wants as a float.
    """
    signup = RecipientSessionRecipe(
        recipient=Recipient.query.filter_by(id=request.json['recipientId']).first(),
        session=Session.query.filter_by(id=request.json['sessionId']).first(),
        recipe=Recipe.query.filter_by(id=request.json['recipeId']).first(),
        meal_count=request.json['mealCount']
    )
    db.session.add(signup)

    for entity, name in [[signup.recipient, 'recipient'], [signup.session, 'session'], [signup.recipe, 'recipe']]:
        if entity is None:
            raise NotFound(f'No {name} was found with the given ID')

    if float(signup.meal_count) <= 0:
        raise BadRequest('mealCount must be greater than or equal to 0')

    db.session.commit()
    return 'created signup'
