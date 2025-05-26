from flask import Blueprint, jsonify

from src.services.heatmap_service import HeatmapService

ransomware_bp = Blueprint('ransomware', __name__)
heatmap_service = HeatmapService()

@ransomware_bp.route('/heatmap', methods=['GET'])
def heatmap():
    response = heatmap_service.get_heatmap_info()
    return jsonify({"heatmap_info": response}), 200


@ransomware_bp.route('/country/<country_code>', methods=['GET'])
def victims_by_country(country_code: str):
    response = heatmap_service.info_by_country(country_code)
    return jsonify({"country_info": response}), 200


@ransomware_bp.route('/certs/<country_code>', methods=['GET'])
def get_cert_info_by_country(country_code: str):
    response = heatmap_service.get_cert_info_by_country(country_code)
    return jsonify({"message": response}), 200