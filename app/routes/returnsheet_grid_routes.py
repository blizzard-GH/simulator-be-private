from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from ..service.returnsheet_grid_service import get_all_returnsheet_grid_service,get_not_submitted_returnsheet_grid_by_tai_service,get_submitted_returnsheet_grid_by_tai_service,get_waiting_for_payment_returnsheet_grid_by_tai_service,get_canceled_returnsheet_grid_by_tai_service,get_rejected_returnsheet_grid_by_tai_service

returnsheet_grid_bp = Blueprint("returnsheetGridBlueprint", __name__, url_prefix="/api/returnsheetgrid")

@returnsheet_grid_bp.route("/getallreturnsheetgrid", methods=["GET"])
@jwt_required()
def get_returnsheet_grid_route():
    returnsheetGrid = get_all_returnsheet_grid_service()

    response = {
        "status": 200,
        "message": "data found" if returnsheetGrid else "no data found",
        "data": returnsheetGrid
    }
    return jsonify(response), 200

@returnsheet_grid_bp.route("/getnotsubmittedreturnsheetgrid", methods=["GET"])
@jwt_required()
def get_not_submitted_returnsheet_grid_by_tai_route():
    claims = get_jwt()
    tai = claims.get('z_taxpayer_aggregate_identifier')

    returnsheetGrid = get_not_submitted_returnsheet_grid_by_tai_service(tai)

    response = {
        "status": 200,
        "message": "data found" if returnsheetGrid else "no data found",
        "data": returnsheetGrid
    }
    return jsonify(response), 200

@returnsheet_grid_bp.route("/getsubmittedreturnsheetgrid", methods=["GET"])
@jwt_required()
def get_submitted_returnsheet_grid_by_tai_route():
    claims = get_jwt()
    tai = claims.get('z_taxpayer_aggregate_identifier')

    returnsheetGrid = get_submitted_returnsheet_grid_by_tai_service(tai)

    response = {
        "status": 200,
        "message": "data found" if returnsheetGrid else "no data found",
        "data": returnsheetGrid
    }
    return jsonify(response), 200

@returnsheet_grid_bp.route("/getwaitingforpaymentreturnsheetgrid", methods=["GET"])
@jwt_required()
def get_waiting_for_payment_returnsheet_grid_by_tai_route():
    claims = get_jwt()
    tai = claims.get('z_taxpayer_aggregate_identifier')

    returnsheetGrid = get_waiting_for_payment_returnsheet_grid_by_tai_service(tai)

    response = {
        "status": 200,
        "message": "data found" if returnsheetGrid else "no data found",
        "data": returnsheetGrid
    }
    return jsonify(response), 200

@returnsheet_grid_bp.route("/getcanceledreturnsheetgrid", methods=["GET"])
@jwt_required()
def get_canceled_returnsheet_grid_by_tai_route():
    claims = get_jwt()
    tai = claims.get('z_taxpayer_aggregate_identifier')

    returnsheetGrid = get_canceled_returnsheet_grid_by_tai_service(tai)

    response = {
        "status": 200,
        "message": "data found" if returnsheetGrid else "no data found",
        "data": returnsheetGrid
    }
    return jsonify(response), 200

@returnsheet_grid_bp.route("/getrejectedreturnsheetgrid", methods=["GET"])
@jwt_required()
def get_rejected_returnsheet_grid_by_tai_route():
    claims = get_jwt()
    tai = claims.get('z_taxpayer_aggregate_identifier')

    returnsheetGrid = get_rejected_returnsheet_grid_by_tai_service(tai)

    response = {
        "status": 200,
        "message": "data found" if returnsheetGrid else "no data found",
        "data": returnsheetGrid
    }
    return jsonify(response), 200