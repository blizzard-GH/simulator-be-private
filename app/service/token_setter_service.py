from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, set_refresh_cookies

from app.service.app_user_service import update_last_login_date_by_tin_service

def token_setter(user, identity):
    additional_claims = {
        "role": user.ROLE,
        "tin": user.TIN,
        "name": user.NAME,
        "last_login_date": user.LAST_LOGIN_DATE,
        "z_taxpayer_aggregate_identifier": user.Z_TAXPAYER_AGGREGATE_IDENTIFIER
    }

    access_token = create_access_token(
        identity=identity,
        additional_claims=additional_claims
    )
    
    refresh_token = create_refresh_token(
        identity=user.TIN,
        additional_claims=additional_claims
    )

    response = jsonify(access_token=access_token)
    set_refresh_cookies(response, refresh_token)
    update_last_login_date_by_tin_service(user.TIN)
    return response
