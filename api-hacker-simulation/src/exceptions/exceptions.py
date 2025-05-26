class RansomwareException(Exception):
    """Base class for all exceptions related to ransomware detection."""
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.message = message
        self.code = code
