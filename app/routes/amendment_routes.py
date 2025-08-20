from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from app.service.amendment_service import create_amendment_service

amendment_bp = Blueprint("amendmentBlueprint", __name__, url_prefix="/api/amendment")

@amendment_bp.route("/createamendment", methods=["POST"])
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
    return create_amendment_service(tai,taxType, taxReturnPeriodType, taxYear, taxReturnModel)

    # return jsonify({"message": "success"}), 200