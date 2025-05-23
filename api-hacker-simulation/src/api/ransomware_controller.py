from flask import Blueprint, jsonify

from src.services.ransomware_service import RansomwareService

ransomware_bp = Blueprint('ransomware', __name__)
ransomware_service = RansomwareService()

@ransomware_bp.route('/heatmap', methods=['GET'])
def heatmap():
    response = ransomware_service.get_heatmap_info()
    return jsonify({"heatmap_info": response}), 200


@ransomware_bp.route('/country', methods=['GET'])
def victims_by_country():
    return jsonify({"message": "getting victims by country"}), 200


@ransomware_bp.route('/certs', methods=['GET'])
def get_cert_info_by_country():
    return jsonify({"message": "getting cert info by country"}), 200