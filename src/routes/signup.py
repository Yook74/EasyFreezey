from flask import request, Blueprint

from src.models import RecipientSessionRecipe, db

blueprint = Blueprint('signup', __name__, url_prefix='/signup')


@blueprint.route('', methods=['POST'])
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
