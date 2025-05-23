from src.services.cache.cache_manager import EndpointCacheManager
from src.services.cache.endpoints.cyberattacks import CyberattacksEndpoint
from src.clients.rest_countries_client import RestCountriesClient

class RansomwareService:
    def __init__(self):
        endpoint = CyberattacksEndpoint()
        self.cache = EndpointCacheManager(endpoint)
        self.country_client = RestCountriesClient()

    def get_heatmap_info(self):
        """
        Group victims by country and return a list of dictionaries with
        country code, number of victims, and country name.
        """
        attacks = self.cache.get_data()
        country_counts = {}

        for attack in attacks:
            code = attack.get("country")
            if not code:
                continue
            country_counts[code] = country_counts.get(code, 0) + 1

        sorted_data = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)

        country_list = self.country_client.get_country_info()
        country_lookup = {
            c["cca2"]: {
                "name": c["common"],
                "lat": c["latlng"][0],
                "lng": c["latlng"][1]
            }
            for c in country_list
        }

        result = []
        for code, victims in sorted_data:
            info = country_lookup.get(code.upper())
            result.append({
                "country": code,
                "victims": victims,
                "name": info["name"] if info else "Unknown",
                "lat": info["lat"] if info else 0.0,
                "lng": info["lng"] if info else 0.0
            })

        return result
        