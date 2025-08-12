from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.service.l3_other_parties_service import get_l3_other_parties_by_returnsheet_record_id_service,insert_prefill_withholding_by_returnsheet_record_id_service

l3_other_parties_bp = Blueprint("l3OtherPartiesBlueprint", __name__, url_prefix="/api/l3otherparties")

@l3_other_parties_bp.route("/getl3otherpartiesbyreturnsheetrecordid/<string:recordid>", methods=["GET"])
@jwt_required()
def get_l3_other_parties_by_returnsheet_record_id_routes(recordid):
    l3OtherParties = get_l3_other_parties_by_returnsheet_record_id_service(recordid)

    response = {
        "status": 200,
        "message": "data found" if l3OtherParties else "no data found",
        "data": l3OtherParties
    }
    return jsonify(response), 200

@l3_other_parties_bp.route("/setprefillwithholdingbyreturnsheetrecordid", methods=["POST"])
@jwt_required()
def insert_prefill_withholding_by_returnsheet_record_id_routes():
    data = request.get_json()

    if 'prefillForm' in data:
        form_data = data['prefillForm']
    else:
        form_data = data

    returnsheet_record_id = form_data.get("returnSheetRecordId")
    option = form_data.get("prefillWithholdingOption")
    insert_prefill_withholding_by_returnsheet_record_id_service(returnsheet_record_id, option)

    return jsonify({"message": "success"}), 200