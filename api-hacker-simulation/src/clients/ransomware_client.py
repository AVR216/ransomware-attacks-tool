import requests

from src.config.config import Config

class RansomwareClient:

    BASE_URL = Config().RANSOMWARE_BASE_URL

    def base_fetch(self, path: str):
        try:
            url = f'{self.BASE_URL}/{path}'
            print("url", url)
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return []

    def get_all_cyberattacks(self):
        return self.base_fetch('allcyberattacks')
