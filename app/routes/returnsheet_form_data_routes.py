from flask import Blueprint, jsonify, request

from app.service.returnsheet_form_data_service import get_returnsheet_form_data_by_record_id_service

returnsheet_form_data_bp = Blueprint("returnsheetformdata", __name__, url_prefix="/api/returnsheetformdata")

@returnsheet_form_data_bp.route("/getreturnsheetformdatabyrecordid/<string:recordid>", methods=["GET"])
def get_returnsheet_form_data_by_record_id_route(recordid):
    returnsheetFormData = get_returnsheet_form_data_by_record_id_service(recordid)

    response = {
        "status": 200,
        "message": "data found" if returnsheetFormData else "no data found",
        "data": returnsheetFormData
    }
    return jsonify(response), 200