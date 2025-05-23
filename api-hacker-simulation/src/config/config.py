import os
from dotenv import load_dotenv

class Config:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            load_dotenv()
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_env_variables()
            print('nueva instancia')
        print('misma instancia')
        return cls._instance
    
    def _load_env_variables(self):
        # Load environment variables from .env file
        self.HOST = os.getenv('HOST', '0.0.0.0')
        self.PORT = int(os.getenv('PORT', '5000'))
        self.CONTEXT_PATH = os.getenv('CONTEXT_PATH', '/api/v1')
        self.RANSOMWARE_BASE_URL = f'{os.getenv('RANSOMWARE_API_PROTOCOL', 'http')}://{os.getenv('RANSOMWARE_BASE_URL')}' 
        self.API_USAGE_LIMIT = int(os.getenv('API_USAGE_LIMIT', 200))