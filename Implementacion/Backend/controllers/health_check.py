from flask import Blueprint, jsonify
from config.database import Database

health_bp = Blueprint('health_check', __name__)
db = Database()

@health_bp.route("/", methods=["GET"])
def health_check():
    if db.check_connection():
        return jsonify({"status": "OK"})
    return jsonify({"status": "ERROR"})