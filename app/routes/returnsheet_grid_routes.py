from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..service.returnsheet_grid_service import get_all_returnsheet_grid_service

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