from werkzeug.exceptions import NotFound

from src.models import Session


def validate_session_id(session_id: int):
    if Session.query.filter_by(id=session_id).count() == 0:
        raise NotFound(f'No session was found with ID {session_id}.')
