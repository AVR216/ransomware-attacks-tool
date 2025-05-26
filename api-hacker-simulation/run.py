from src.app import create_app

app = create_app()

if __name__ == '__main__':
    from src.config.config import config
    app.run(debug=True, host=config.HOST, port=config.PORT)