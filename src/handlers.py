from flask import current_app as app
from flask import Response
from sqlalchemy.exc import IntegrityError


@app.errorhandler(IntegrityError)
def handle_integrity_error(exception):
    return Response(exception.args[0], status=400)


@app.errorhandler(KeyError)
def handle_key_error(exception):
    return Response(f'JSON was missing key "{exception.args[0]}"', status=400)
