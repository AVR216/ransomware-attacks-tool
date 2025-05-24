from collections import defaultdict, Counter
from datetime import datetime

from src.clients.rest_countries_client import RestCountriesClient
from src.clients.ransomware_client import RansomwareClient
from src.services.cache.generic_cache_service import GenericCacheService
from src.services.cache.cache_policy import CachePolicyEnumType

class HeatmapService:

    def __init__(self):
        self.web_client = RansomwareClient()
        self.rest_countries_client = RestCountriesClient()

        self.cache_all_cyberattacks = GenericCacheService(
            fetch_fn=self.web_client.get_all_cyberattacks,
            key="all_cyberattacks",
            policy=CachePolicyEnumType.METADATA,
            metadata_fn=self.web_client.get_info,
            metadata_key=["Cyberattacks", "Last Update json"]
        )

        self.cache_recent_victims = GenericCacheService(
            fetch_fn=self.web_client.get_recent_victims,
            key="recentvictims",
            policy=CachePolicyEnumType.METADATA,
            metadata_fn=self.web_client.get_info,
            metadata_key=["Victims", "Last Update json"]
        )



    def get_heatmap_info(self):
    # 1. Obtener ataques
        attacks = self.cache_all_cyberattacks.get()
        country_counts = {}

        for attack in attacks:
            code = attack.get("country")
            if not code:
                continue
            country_counts[code] = country_counts.get(code, 0) + 1

        sorted_data = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)

        # 2. Obtener recent victims para agrupar por país y grupo
        recent_victims = self.cache_recent_victims.get()
        country_groups = {}

        for victim in recent_victims:
            code = victim.get("country")
            group = victim.get("group")
            if not code or not group:
                continue
            code = code.upper()
            if code not in country_groups:
                country_groups[code] = {}
            country_groups[code][group] = country_groups[code].get(group, 0) + 1

        # 3. Encontrar el grupo más frecuente por país
        top_group_by_country = {}
        for code, group_counts in country_groups.items():
            top_group = max(group_counts.items(), key=lambda x: x[1])[0]
            top_group_by_country[code] = top_group

        # 4. Cargar info de países
        country_list = self.rest_countries_client.get_country_info()
        country_lookup = {
            c["cca2"]: {
                "name": c["common"],
                "lat": c["lat"],
                "lng": c["lng"]
            }
            for c in country_list
        }

        # 5. Construir resultado enriquecido
        result = []
        for code, victims in sorted_data:
            info = country_lookup.get(code.upper())
            result.append({
                "country": code,
                "victims": victims,
                "name": info["name"] if info else "Unknown",
                "lat": info["lat"] if info else 0.0,
                "lng": info["lng"] if info else 0.0,
                "top_group": top_group_by_country.get(code.upper(), "Unknown")
            })

        return result


    def info_by_country(self, country_code: str) -> dict:
        """
        Devuelve información relevante de un país usando la cache de recent victims,
        agrupa víctimas, sectores, grupos y stats de infostealer, con chequeos seguros.
        """
        victims = self.cache_recent_victims.get(country_code)
        if not victims:
            return {
                "country": country_code,
                "total_victims": 0,
                "top_groups": [],
                "top_sectors": {},
                "last_attack": None,
                "infostealers": {}
            }

        total_victims = len(victims)
        group_counter = Counter()
        sector_counter = Counter()
        last_attack_date = None
        infostealer_counter = Counter()

        for v in victims:
            # Grupos atacantes
            group = v.get("group")
            if group:
                group_counter[group] += 1

            # Sectores (vacíos → "Unknown")
            sector = v.get("activity") or "Unknown"
            sector_counter[sector] += 1

            # Última fecha de ataque
            discovered = v.get("discovered")
            if discovered:
                try:
                    dt = datetime.fromisoformat(discovered)
                    if not last_attack_date or dt > last_attack_date:
                        last_attack_date = dt
                except Exception:
                    pass

            # Stats de infostealer, chequeo de tipo
            inf = v.get("infostealer")
            if isinstance(inf, dict):
                stats = inf.get("infostealer_stats") or {}
                for name, count in stats.items():
                    infostealer_counter[name] += count

        return {
            "country": country_code,
            "total_victims": total_victims,
            "top_groups": [g for g, _ in group_counter.most_common(3)],
            "top_sectors": dict(sector_counter.most_common(3)),
            "last_attack": last_attack_date.strftime("%Y-%m-%d %H:%M:%S") if last_attack_date else None,
            "infostealers": dict(infostealer_counter.most_common(3))
        }

    

    def get_cert_info_by_country(self, country_code: str):
        certs = self.web_client.get_certs_by_country(country_code)
        return certs
