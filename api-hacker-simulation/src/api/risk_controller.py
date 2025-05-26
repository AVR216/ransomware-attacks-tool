from flask import Blueprint, request, jsonify
from src.services.scoring_risk_service import RiskService

risk_bp = Blueprint("risk", __name__)
risk_service = RiskService()

@risk_bp.route("/groups", methods=["GET"])
def get_risk():
    level = request.args.get("level")
    top = request.args.get("top", default=5, type=int)
    try:
        result = risk_service.get_group_risk(level=level, top=top)
        return jsonify(result), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500