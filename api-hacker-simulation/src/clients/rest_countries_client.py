import os
import json
import requests

class RestCountriesClient:
    def __init__(self):
        self.file_path = "src/data/country_data.json"
        self.api_url = "https://restcountries.com/v3.1/all"

    def get_country_info(self):
        """
        Obtiene información de países desde archivo local si existe,
        o desde la API de REST Countries si no.
        Retorna un dict ISO2 -> {name, lat, lng}
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)

        # Si no existe, consulta la API
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
                        "latlng": latlng,
                        "cca2": cca2
                    })

            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, "w") as f:
                json.dump(countries, f, indent=2)

            return countries

        except requests.RequestException as e:
            print(f"[CountryService] Error fetching countries: {e}")
            return []