from src.clients.ransomware_client import RansomwareClient
from src.services.cache.base import CacheableEndpoint


class CyberattacksEndpoint(CacheableEndpoint):
    def __init__(self):
        self.client = RansomwareClient()

    def cache_key(self) -> str:
        return "cyberattacks"

    def fetch_data(self):
        return self.client.get_all_cyberattacks()

    def get_remote_last_updated(self):
        info = self.client.base_fetch("info")
        return info.get("Cyberattacks", {}).get("Last Update json")
