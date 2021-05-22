from difflib import SequenceMatcher

from flask import request, jsonify, Blueprint
from werkzeug.exceptions import BadRequest

from src.models import Aisle, db

blueprint = Blueprint('aisle', __name__, url_prefix='/aisle')


@blueprint.post('')
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


@blueprint.get('')
def all_aisles():
    return jsonify([
        {'name': aisle.name, 'id': aisle.id}
        for aisle in Aisle.query
    ])
