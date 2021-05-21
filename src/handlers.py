from flask import Response, Blueprint
from sqlalchemy.exc import IntegrityError

blueprint = Blueprint('error_handlers', __name__)


@blueprint.errorhandler(IntegrityError)
def handle_integrity_error(exception):
    return Response(exception.args[0], status=400)


@blueprint.errorhandler(KeyError)
def handle_key_error(exception):
    return Response(f'JSON was missing key "{exception.args[0]}"', status=400)
