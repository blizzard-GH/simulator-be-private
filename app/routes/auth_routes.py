from flask import Blueprint, make_response, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required, create_refresh_token, set_refresh_cookies

from app.model.app_user import APPUSER
from app.service.app_user_service import create_app_user_service
from app.service.username_validation_service import UsernameValidator

auth_bp = Blueprint("authBlueprint", __name__, url_prefix="/api")

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = APPUSER.query.filter_by(TIN=data['username']).first()

    if user and user.check_password(data['password']):

        additional_claims = {
            "role": user.ROLE,
            "tin": user.TIN,
            "name": user.NAME,
            "last_login_date": user.LAST_LOGIN_DATE,
            "z_taxpayer_aggregate_identifier": user.Z_TAXPAYER_AGGREGATE_IDENTIFIER
        }

        # Generate and return JWT token
        access_token = create_access_token(
            identity=user.TIN,
            additional_claims=additional_claims)
        
        # refresh_token = create_refresh_token(identity=user.TIN)
        refresh_token = create_refresh_token(
            identity=user.TIN,
            additional_claims = {
                "role": user.ROLE,
                "tin": user.TIN,
                "name": user.NAME,
                "last_login_date": user.LAST_LOGIN_DATE,
                "z_taxpayer_aggregate_identifier": user.Z_TAXPAYER_AGGREGATE_IDENTIFIER
            }
        )
        response = jsonify(access_token=access_token)
        set_refresh_cookies(response, refresh_token)
        return response
    else:

        usernameValidator = UsernameValidator()
        if usernameValidator.validate(data['username'], data['password'])[0]:
            createUserResponse = create_app_user_service(data['username'])
            newUser = APPUSER.query.filter_by(TIN=data['username']).first()
            additional_claims = {
                "role": newUser.ROLE,
                "tin": newUser.TIN,
                "name": newUser.NAME,
                "last_login_date": newUser.LAST_LOGIN_DATE,
                "z_taxpayer_aggregate_identifier": newUser.Z_TAXPAYER_AGGREGATE_IDENTIFIER
            }

            # Generate and return JWT token
            access_token = create_access_token(
                identity=newUser.TIN,
                additional_claims=additional_claims)
            
            # refresh_token = create_refresh_token(identity=user.TIN)
            refresh_token = create_refresh_token(
                identity=newUser.TIN,
                additional_claims = {
                    "role": newUser.ROLE,
                    "tin": newUser.TIN,
                    "name": newUser.NAME,
                    "last_login_date": newUser.LAST_LOGIN_DATE,
                    "z_taxpayer_aggregate_identifier": newUser.Z_TAXPAYER_AGGREGATE_IDENTIFIER
                }
            )
            response = jsonify(access_token=access_token)
            set_refresh_cookies(response, refresh_token)
            return response

        return jsonify({"msg": "Invalid credentials"}), 401
    
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()

    user = APPUSER.query.filter_by(TIN=get_jwt().get("tin")).first()

    safe_claims = {
        "role": user.ROLE,
        "tin": user.TIN,
        "name": user.NAME,
        "last_login_date": user.LAST_LOGIN_DATE,
        "z_taxpayer_aggregate_identifier": user.Z_TAXPAYER_AGGREGATE_IDENTIFIER
    }

    new_access_token = create_access_token(identity=current_user, additional_claims=safe_claims)
    return jsonify(access_token=new_access_token), 200

    
@auth_bp.route('/switchidentity', methods=['POST'])
@jwt_required()
def switch_identity():
    current_tin = get_jwt_identity()
    data = request.get_json()
    new_tin = data.get('selectedTIN')

    if not new_tin:
        return jsonify({"msg": "TIN not provided"}), 400

    # Optional: verify the new TIN is associated with current user
    user = APPUSER.query.filter_by(TIN=current_tin).first()
    impersonate_user = APPUSER.query.filter_by(TIN=new_tin).first()

    if not user or not impersonate_user:
        return jsonify({"msg": "Invalid user or TIN"}), 401
    
    additional_claims = {
        "role": impersonate_user.ROLE,
        "tin": impersonate_user.TIN,
        "name": impersonate_user.NAME,
        "last_login_date": impersonate_user.LAST_LOGIN_DATE,
        "z_taxpayer_aggregate_identifier": impersonate_user.Z_TAXPAYER_AGGREGATE_IDENTIFIER
    }

    # ✅ Create new token with new sub
    new_token = create_access_token(
        identity=current_tin,
        additional_claims=additional_claims)
    
    # refresh_token = create_refresh_token(identity=user.TIN)
    refresh_token = create_refresh_token(
        identity=user.TIN,
        additional_claims = {
            "role": impersonate_user.ROLE,
            "tin": impersonate_user.TIN,
            "name": impersonate_user.NAME,
            "last_login_date": impersonate_user.LAST_LOGIN_DATE,
            "z_taxpayer_aggregate_identifier": impersonate_user.Z_TAXPAYER_AGGREGATE_IDENTIFIER
        }
    )
    response = jsonify(access_token=new_token)

    set_refresh_cookies(response, refresh_token)

    return response