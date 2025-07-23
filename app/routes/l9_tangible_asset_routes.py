from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.service.l9_tangible_asset_service import get_l9_tangible_asset_by_returnsheet_record_id_service

l9_tangible_asset_bp = Blueprint("l9TangibleAsset", __name__, url_prefix="/api/l9tangibleasset")

@l9_tangible_asset_bp.route("/getl9tangibleassetbyreturnsheetrecordid/<string:recordid>", methods=["GET"])
@jwt_required()
def get_l9_tangible_asset_by_returnsheet_record_id_routes(recordid):
    l9TangibleAsset = get_l9_tangible_asset_by_returnsheet_record_id_service(recordid)

    response = {
        "status": 200,
        "message": "data found" if l9TangibleAsset else "no data found",
        "data": l9TangibleAsset
    }
    return jsonify(response), 200