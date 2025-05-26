from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv(override=True) 

from src.config.config import config
from src.api.ransomware_controller import ransomware_bp
from src.api.risk_controller import risk_bp
from src.config.loggers import setup_logging
from src.api.web.error_handler import register_error_handlers


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config)
    context_path = app.config['CONTEXT_PATH']
    register_error_handlers(app)
    setup_logging()

    @app.route(f'{context_path}/health')
    def health():
        return "OK"

    app.register_blueprint(ransomware_bp, url_prefix=f'{context_path}/ransomware')
    app.register_blueprint(risk_bp, url_prefix=f'{context_path}/ransomware/risk')

    return app