from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from ..service.billing_service import get_billing_by_tai_service, pay_billing_service

billing_bp = Blueprint("billingBlueprint", __name__, url_prefix="/api/billing")

@billing_bp.route("/getactivebilling", methods=["GET"])
@jwt_required()
def get_active_billing_route():
    claims = get_jwt()
    tai = claims.get('z_taxpayer_aggregate_identifier')
    billing = get_billing_by_tai_service(tai)

    response = {
        "status": 200,
        "message": "data found" if billing else "no data found",
        "data": billing
    }
    return jsonify(response), 200

@billing_bp.route("/paybilling", methods=["POST"])
@jwt_required()
def pay_billing_routes():
    claims = get_jwt()
    tai = claims.get('z_taxpayer_aggregate_identifier')
    data = request.get_json()

    z_payment_record_id = data.get('z_payment_record_id')

    if not z_payment_record_id:
        return jsonify({"msg": "Payment Record Id not provided"}), 400

    try:
        result = pay_billing_service(tai, z_payment_record_id)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
