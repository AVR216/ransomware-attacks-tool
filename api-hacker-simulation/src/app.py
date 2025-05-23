from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv(override=True) 

from src.config.config import Config
from src.api.ransomware_controller import ransomware_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config())
    context_path = app.config['CONTEXT_PATH']

    @app.route(f'{context_path}/health')
    def health():
        return "OK"

    app.register_blueprint(ransomware_bp, url_prefix=f'{context_path}/ransomware')

    return app