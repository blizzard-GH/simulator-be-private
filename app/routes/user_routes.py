from flask import Blueprint, jsonify, request
from ..service.tbl_user_service import get_all_users_service, get_user_by_npwp_service, get_user_by_username_service

user_test_bp = Blueprint("usertest", __name__, url_prefix="/api/userstest")

# @user_bp.route("/", methods=["GET"])
# def get_user():
#     username = request.args.get("username")
#     npwp = request.args.get("npwp")

#     if username:
#         return jsonify(get_user_by_username_service(username))
#     elif npwp:
#         return jsonify(get_user_by_npwp_service(npwp))
#     else:
#         return jsonify(get_all_users_service())

@user_test_bp.route("/getuserbyusername/<string:username>", methods=["GET"])
def get_user_by_username(username):
    return jsonify(get_user_by_username_service(username))

@user_test_bp.route("/", methods=["GET"])
def get_users():
    # users = TblUser.query.all()
    user_list = get_all_users_service()

    response = {
        "status": 200,
        "message": "data found" if user_list else "no data found",
        "data": user_list
    }
    return jsonify(response), 200