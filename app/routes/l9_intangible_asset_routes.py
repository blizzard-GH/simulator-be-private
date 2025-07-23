from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.service.l9_intangible_asset_service import get_l9_intangible_asset_by_returnsheet_record_id_service

l9_intangible_asset_bp = Blueprint("l9IntangibleAsset", __name__, url_prefix="/api/l9intangibleasset")

@l9_intangible_asset_bp.route("/getl9intangibleassetbyreturnsheetrecordid/<string:recordid>", methods=["GET"])
@jwt_required()
def get_l9_intangible_asset_by_returnsheet_record_id_routes(recordid):
    l9IntangibleAsset = get_l9_intangible_asset_by_returnsheet_record_id_service(recordid)

    response = {
        "status": 200,
        "message": "data found" if l9IntangibleAsset else "no data found",
        "data": l9IntangibleAsset
    }
    return jsonify(response), 200