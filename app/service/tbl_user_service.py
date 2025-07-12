from ..model.tbl_user import TblUser
from .. import db
from flask import abort
from ..utils.serializer import model_to_dict, models_to_list

def get_all_users_service(limit=3):
    users = TblUser.query.limit(limit).all()
    return models_to_list(users)

def get_user_by_id_service(user_id):
    user = TblUser.query.get_or_404(user_id)
    return user.to_dict()

def get_user_by_npwp_service(npwp):
    user = TblUser.query.filter_by(npwp15=npwp).first()

    if not user:
        abort(404, description=f"User with Username {npwp} not found")

    return model_to_dict(user)

def get_user_by_username_service(username):
    user = TblUser.query.filter_by(username=username).first()

    if not user:
        abort(404, description=f"User with Username {username} not found")

    return model_to_dict(user)

def get_user_by_npwp_and_email_service(npwp, email):
    user = TblUser.query.filter_by(npwp15=npwp, email=email).first()
    
    if not user:
        abort(404, description=f"User with NPWP {npwp} and email {email} not found")
    
    return model_to_dict(user)