from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from app.model.app_user import APPUSER

auth_bp = Blueprint("auth", __name__, url_prefix="/api")

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = APPUSER.query.filter_by(PERSONAL_TIN=data['username']).first()

    if user and user.check_password(data['password']):

        additional_claims = {
            "personal_tin": user.PERSONAL_TIN,
            "personal_name": user.PERSONAL_NAME,
            "corporate_tin": user.CORPORATE_TIN,
            "corporate_name": user.CORPORATE_NAME,
            "last_login_date":user.LAST_LOGIN_DATE
        }

        # Generate and return JWT token
        access_token = create_access_token(
            identity=user.PERSONAL_TIN,
            additional_claims=additional_claims)
        
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Invalid credentials"}), 401
