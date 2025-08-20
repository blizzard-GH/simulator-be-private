from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from app.service.returnsheet_form_data_service import get_returnsheet_form_data_by_record_id_service, get_returnsheet_main_form_data_by_record_id_service, get_returnsheet_form_data_by_aggregate_identifier_service, get_returnsheet_main_form_data_by_aggregate_identifier_service

returnsheet_form_data_bp = Blueprint("returnsheetFormDataBlueprint", __name__, url_prefix="/api/returnsheetformdata")

@returnsheet_form_data_bp.route("/getreturnsheetformdatabyrecordid/<string:recordid>", methods=["GET"])
@jwt_required()
def get_returnsheet_form_data_by_record_id_route(recordid):
    claims = get_jwt()
    tai = claims.get('z_taxpayer_aggregate_identifier')
    returnsheetFormData = get_returnsheet_form_data_by_record_id_service(recordid, tai)

    response = {
        "status": 200,
        "message": "data found" if returnsheetFormData else "no data found",
        "data": returnsheetFormData
    }
    return jsonify(response), 200

@returnsheet_form_data_bp.route("/getreturnsheetformdatabyaggregateidentifier/<string:aggregateidentifier>", methods=["GET"])
@jwt_required()
def get_returnsheet_form_data_by_aggregate_identifier_route(aggregateidentifier):
    returnsheetFormData = get_returnsheet_form_data_by_aggregate_identifier_service(aggregateidentifier)

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

@returnsheet_form_data_bp.route("/getreturnsheetmainformdatabybyaggregateidentifier/<string:aggregateidentifier>", methods=["GET"])
@jwt_required()
def get_returnsheet_main_form_data_by_aggregate_identifier__route(aggregateidentifier):
    returnsheetMainFormData = get_returnsheet_main_form_data_by_aggregate_identifier_service(aggregateidentifier)

    response = {
        "status": 200,
        "message": "data found" if returnsheetMainFormData else "no data found",
        "data": returnsheetMainFormData
    }
    return jsonify(response), 200