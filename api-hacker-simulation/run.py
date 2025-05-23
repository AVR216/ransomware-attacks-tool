from src.app import create_app
from src.config.config import Config

app = create_app()

if __name__ == '__main__':
    config = Config()
    app.run(debug=True, host=config.HOST, port=config.PORT)