from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.model.app_user import APPUSER
from app.service.app_user_service import create_app_user_service
from app.service.token_setter_service import token_setter
from app.service.username_validation_service import UsernameValidator

auth_bp = Blueprint("authBlueprint", __name__, url_prefix="/api")

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = APPUSER.query.filter_by(TIN=data['username']).first()

    if user and user.check_password(data['password']):
        return token_setter(user, user.TIN)
    else:
        usernameValidator = UsernameValidator()
        if usernameValidator.validate(data['username'], data['password'])[0]:
            create_app_user_service(data['username'])
            newUser = APPUSER.query.filter_by(TIN=data['username']).first()
            return token_setter(newUser, data['username'])

        return jsonify({"msg": "Invalid credentials"}), 401
    
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user_tin = get_jwt_identity()
    user = APPUSER.query.filter_by(TIN=current_user_tin).first()
    return token_setter(user, current_user_tin)

    
@auth_bp.route('/switchidentity', methods=['POST'])
@jwt_required()
def switch_identity():
    current_tin = get_jwt_identity()
    data = request.get_json()
    new_tin = data.get('selectedTIN')

    if not new_tin:
        return jsonify({"msg": "TIN not provided"}), 400

    user = APPUSER.query.filter_by(TIN=current_tin).first()
    impersonate_user = APPUSER.query.filter_by(TIN=new_tin).first()

    if not user or not impersonate_user:
        return jsonify({"msg": "Invalid user or TIN"}), 401
    
    return token_setter(impersonate_user, current_tin)