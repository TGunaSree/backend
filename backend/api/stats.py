from flask import Blueprint, jsonify

stats_bp = Blueprint('stats', __name__)

@stats_bp.route("/", methods=["GET"])
def stats_home():
    return jsonify({"message": "Stats API working"})
