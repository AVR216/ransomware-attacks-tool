import os

class Config:
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '5000'))
    CONTEXT_PATH = os.getenv('CONTEXT_PATH', '/api/v1')
    RANSOMWARE_BASE_URL = (
        f"{os.getenv('RANSOMWARE_API_PROTOCOL', 'http')}://"
        f"{os.getenv('RANSOMWARE_BASE_URL', 'localhost')}"
    )
    API_USAGE_LIMIT = int(os.getenv('API_USAGE_LIMIT', '200'))

config = Config()
