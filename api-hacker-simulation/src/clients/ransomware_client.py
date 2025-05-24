import requests

from src.config.config import Config

class RansomwareClient:

    BASE_URL = Config().RANSOMWARE_BASE_URL

    def base_fetch(self, path: str):
        try:
            url = f'{self.BASE_URL}/{path}'
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return []

    def get_all_cyberattacks(self):
        return self.base_fetch('allcyberattacks')
    
    def get_info(self):
        return self.base_fetch('info')

    def get_recent_victims(self):
        return self.base_fetch('recentvictims')
    
    def get_country_victims(self, country_code: str):
        return self.base_fetch(f'countryvictims/{country_code}')

    def get_certs_by_country(self, country_code: str):
        return self.base_fetch(f'certs/{country_code}')
