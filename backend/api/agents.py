from flask import Blueprint, jsonify

agents_bp = Blueprint('agents', __name__)

@agents_bp.route("/", methods=["GET"])
def agents_home():
    return jsonify({"message": "Agents API working"})
