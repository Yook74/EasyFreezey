from flask import request, Blueprint

from server.models import db, Recipient

blueprint = Blueprint('recipient', __name__, url_prefix='/recipient')


@blueprint.post('')
def post_recipient():
    """
    Expects JSON with a "name" key specifying the new recipient's name.
    You may also specify "phone" and "email" for this recipient. The values for "phone" and "email" should be strings.
    :return: the ID of the new recipient
    """
    recipient = Recipient(
        name=request.json['name'],
        email=request.json.get('email'),
        phone=request.json.get('phone')
    )
    db.session.add(recipient)
    db.session.commit()
    return str(recipient.id)
