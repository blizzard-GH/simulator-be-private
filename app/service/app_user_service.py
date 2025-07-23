from ..model.app_user import APPUSER
from flask import abort
from ..utils.serializer import model_to_dict

def get_app_user_by_personal_tin(personal_tin):
    appUser = APPUSER.query.filter_by(PERSONAL_TIN=personal_tin).first()

    if not appUser:
        abort(404, description=f"User with TIN {personal_tin} not found")

    return model_to_dict(appUser)