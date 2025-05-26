import logging
import requests

from src.services.cache.generic_cache_service import GenericCacheService
from src.services.cache.cache_policy import CachePolicyEnumType
from src.exceptions.exceptions import RansomwareException

logger = logging.getLogger(__name__)

class RestCountriesClient:
    def __init__(self):
        self.api_url = "https://restcountries.com/v3.1/all"
        self.cache = GenericCacheService(
            fetch_fn=self._fetch_country_data,
            key="restcountries",
            policy=CachePolicyEnumType.STATIC
        )

    def _fetch_country_data(self):
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            raw_data = response.json()

            countries = []
            for country in raw_data:
                common = country.get("name", {}).get("common")
                latlng = country.get("latlng")
                cca2 = country.get("cca2")

                if common and latlng and cca2:
                    countries.append({
                        "common": common,
                        "lat": latlng[0],
                        "lng": latlng[1],
                        "cca2": cca2
                    })

            return countries

        except requests.RequestException as e:
            logger.error(f"[RestCountriesClient] Error fetching countries: {e}")
            raise RansomwareException(message='Error fetching countries info', code=500)

    def get_country_info(self):
        """
        Returns countries list with (common, cca2, lat and lng),
        using local cache if already exists
        """
        return self.cache.get()
