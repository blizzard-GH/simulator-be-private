from flask import Blueprint, jsonify, request

from app.service.l3_other_parties_service import get_l3_other_parties_by_returnsheet_record_id_service

l3_other_parties_bp = Blueprint("l3OtherPartiesBlueprint", __name__, url_prefix="/api/l3otherparties")

@l3_other_parties_bp.route("/getl3otherpartiesbyreturnsheetrecordid/<string:recordid>", methods=["GET"])
def get_l3_other_parties_by_returnsheet_record_id_routes(recordid):
    l3OtherParties = get_l3_other_parties_by_returnsheet_record_id_service(recordid)

    response = {
        "status": 200,
        "message": "data found" if l3OtherParties else "no data found",
        "data": l3OtherParties
    }
    return jsonify(response), 200