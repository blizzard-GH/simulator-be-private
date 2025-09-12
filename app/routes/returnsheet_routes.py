from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from app.service import returnsheet_grid_service
from app.service.returnsheet_service import amendment_returnsheet_service, save_returnsheet_service
from app.service.billing_service import new_billing_service

returnsheet_bp = Blueprint("returnsheetBlueprint", __name__, url_prefix="/api/returnsheet")

@returnsheet_bp.route("/amendment", methods=["POST"])
@jwt_required()
def create_amendment_routes():
    claims = get_jwt()
    tai = claims.get('z_taxpayer_aggregate_identifier')
    data = request.get_json()

    if 'returnsheetCreateForm' in data:
        form_data = data['returnsheetCreateForm']
    else:
        form_data = data

    # returnsheetCreateForm = form_data.get("returnSheetRecordId")
    taxType = form_data.get("TaxType")
    taxReturnPeriodType = form_data.get("TaxReturnPeriodType")
    taxYear = form_data.get("TaxYear")
    taxReturnModel = form_data.get("TaxReturnModel")
    return amendment_returnsheet_service(tai,taxType, taxReturnPeriodType, taxYear, taxReturnModel)

@returnsheet_bp.route("/save", methods=["POST"])
@jwt_required()
def save_returnsheet_routes():
    claims = get_jwt()
    tai = claims.get('z_taxpayer_aggregate_identifier')
    status = "DRAFT"
    data = request.get_json()

    try:
        result = save_returnsheet_service(data, status)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@returnsheet_bp.route("/submit", methods=["POST"])
@jwt_required()
def submit_returnsheet_routes():
    claims = get_jwt()
    tai = claims.get('z_taxpayer_aggregate_identifier')
    status = "SUBMITTED"
    data = request.get_json()

    try:
        result = save_returnsheet_service(data, status)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@returnsheet_bp.route("/waitingforpayment", methods=["POST"])
@jwt_required()
def waiting_for_payment_returnsheet_routes():
    claims = get_jwt()
    tai = claims.get('z_taxpayer_aggregate_identifier')
    status = "WAITINGFORPAYMENT"
    data = request.get_json()

    try:
        result = save_returnsheet_service(data, status)
        result2 = new_billing_service(tai, data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400