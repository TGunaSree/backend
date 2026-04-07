from flask import Blueprint, jsonify

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/", methods=["GET"])
def auth_home():
    return jsonify({"message": "Auth API working"})
