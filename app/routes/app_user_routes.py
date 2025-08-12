from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.service.app_user_service import get_app_user_by_tin_service, get_corporate_user_by_personal_tin_service, check_passphrase_service

app_user_bp = Blueprint("appUserBlueprint", __name__, url_prefix="/api/user")

@app_user_bp.route("/getuser", methods=["GET"])
@jwt_required()
def get_app_user_by_tin_route():
    tin = get_jwt_identity()
    appUser = get_app_user_by_tin_service(tin)

    response = {
        "status": 200,
        "message": "data found" if appUser else "no data found",
        "data": appUser
    }
    return jsonify(response), 200

@app_user_bp.route("/getcorporateuser", methods=["GET"])
@jwt_required()
def get_corporate_user_by_personal_tin_route():
    tin = get_jwt_identity()
    appUser = get_corporate_user_by_personal_tin_service(tin)

    response = {
        "status": 200,
        "message": "data found" if appUser else "no data found",
        "data": appUser
    }
    return jsonify(response), 200

@app_user_bp.route("/checkpassphrase", methods=["POST"])
@jwt_required()
def check_passphrase_route():
    data = request.get_json()
    
    # Handle nested signDocForm structure
    if 'signDocForm' in data:
        form_data = data['signDocForm']
    else:
        form_data = data
    
    tin = form_data.get("SignerNIK")
    passphrase = form_data.get("Passphrase")
    signerProvider = form_data.get("SignerProvider")
    signingType = form_data.get("SigningType")
    
    response = {
        "status": 200 if check_passphrase_service(tin, passphrase) else 400,
        "message": "passphrase is correct" if check_passphrase_service(tin, passphrase) else "passphrase is incorrect",
        "data": check_passphrase_service(tin, passphrase)
    }
    return jsonify(response), response["status"]