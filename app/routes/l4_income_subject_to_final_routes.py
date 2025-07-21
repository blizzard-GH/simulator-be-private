from flask import Blueprint, jsonify, request

from app.service.l4_income_subject_to_final_service import get_l4_income_subject_to_final_by_returnsheet_record_id_service

l4_income_subject_to_final_bp = Blueprint("l4IncomeSubjectToFinal", __name__, url_prefix="/api/l4incomesubjecttofinal")

@l4_income_subject_to_final_bp.route("/getl4incometsubjecttofinalbyreturnsheetrecordid/<string:recordid>", methods=["GET"])
def get_l4_income_subject_to_final_by_returnsheet_record_id_routes(recordid):
    l4IncomeSubjectToFinal = get_l4_income_subject_to_final_by_returnsheet_record_id_service(recordid)

    response = {
        "status": 200,
        "message": "data found" if l4IncomeSubjectToFinal else "no data found",
        "data": l4IncomeSubjectToFinal
    }
    return jsonify(response), 200