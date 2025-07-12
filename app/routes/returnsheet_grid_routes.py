from flask import Blueprint, jsonify, request
from ..service.returnsheet_grid_service import get_all_returnsheet_grid_service

returnsheet_grid_bp = Blueprint("returnsheet", __name__, url_prefix="/api/returnsheets")

@returnsheet_grid_bp.route("/getallreturnsheets", methods=["GET"])
def get_returnsheet_grid_route():
    # users = TblUser.query.all()
    user_list = get_all_returnsheet_grid_service()

    response = {
        "status": 200,
        "message": "data found" if user_list else "no data found",
        "data": user_list
    }
    return jsonify(response), 200