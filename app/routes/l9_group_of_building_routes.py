from flask import Blueprint, jsonify, request

from app.service.l9_group_of_building_service import get_l9_group_of_building_by_returnsheet_record_id_service

l9_group_of_building_bp = Blueprint("l9GroupOfBuilding", __name__, url_prefix="/api/l9groupofbuilding")

@l9_group_of_building_bp.route("/getl9groupofbuildingbyreturnsheetrecordid/<string:recordid>", methods=["GET"])
def get_l9_group_of_building_by_returnsheet_record_id_routes(recordid):
    l9GroupOfBuilding = get_l9_group_of_building_by_returnsheet_record_id_service(recordid)

    response = {
        "status": 200,
        "message": "data found" if l9GroupOfBuilding else "no data found",
        "data": l9GroupOfBuilding
    }
    return jsonify(response), 200