from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.service.returnsheet_form_data_service import get_returnsheet_form_data_by_record_id_service, get_returnsheet_main_form_data_by_record_id_service

returnsheet_form_data_bp = Blueprint("returnsheetFormDataBlueprint", __name__, url_prefix="/api/returnsheetformdata")

@returnsheet_form_data_bp.route("/getreturnsheetformdatabyrecordid/<string:recordid>", methods=["GET"])
@jwt_required()
def get_returnsheet_form_data_by_record_id_route(recordid):
    returnsheetFormData = get_returnsheet_form_data_by_record_id_service(recordid)

    response = {
        "status": 200,
        "message": "data found" if returnsheetFormData else "no data found",
        "data": returnsheetFormData
    }
    return jsonify(response), 200


@returnsheet_form_data_bp.route("/getreturnsheetmainformdatabyrecordid/<string:recordid>", methods=["GET"])
@jwt_required()
def get_returnsheet_main_form_data_by_record_id_route(recordid):
    returnsheetMainFormData = get_returnsheet_main_form_data_by_record_id_service(recordid)

    response = {
        "status": 200,
        "message": "data found" if returnsheetMainFormData else "no data found",
        "data": returnsheetMainFormData
    }
    return jsonify(response), 200