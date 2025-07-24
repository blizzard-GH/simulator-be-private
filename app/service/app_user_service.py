from ..model.app_user import APPUSER
from flask import abort
from ..utils.serializer import model_to_dict

def get_app_user_by_tin_service(tin):
    appUser = APPUSER.query.filter_by(TIN=tin).first()

    if not appUser:
        abort(404, description=f"User with TIN {tin} not found")

    return model_to_dict(appUser)

def get_corporate_user_by_personal_tin_service(tin):
    appUser = APPUSER.query.filter_by(TIN_PERSONAL=tin).first()

    if not appUser:
        abort(404, description=f"User with TIN {tin} not found")

    return model_to_dict(appUser)