from flask import jsonify
import logging
from src.exceptions.exceptions import RansomwareException
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    @app.errorhandler(RansomwareException)
    def handle_ransomware_exception(e: RansomwareException):
        logger.warning(f"[RansomwareException] {e.message} (code={e.code})")
        response = {
            "error": "RansomwareException",
            "message": e.message
        }
        return jsonify(response), e.code

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        if isinstance(e, HTTPException):
            logger.warning(f"[HTTPException] {e.name} - {e.description}")
            return e
        logger.exception("[Unhandled Exception] An unexpected error occurred:")
        response = {
            "error": "InternalServerError",
            "message": "An unexpected error occurred."
        }
        return jsonify(response), 500
