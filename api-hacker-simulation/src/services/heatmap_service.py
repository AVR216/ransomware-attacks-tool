from collections import Counter
from datetime import datetime
import logging


from src.clients.rest_countries_client import RestCountriesClient
from src.clients.ransomware_client import RansomwareClient
from src.services.cache.generic_cache_service import GenericCacheService
from src.services.cache.cache_policy import CachePolicyEnumType
from src.exceptions.exceptions import RansomwareException

logger = logging.getLogger(__name__)

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
        """Return all info for create a heatmap"""
        # Get all atacks from its cacheable endpoint
        attacks = self.cache_all_cyberattacks.get()
        country_counts = {}

        for attack in attacks:
            code = attack.get("country")
            if not code:
                continue
            country_counts[code] = country_counts.get(code, 0) + 1

        sorted_data = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)

        # Get recent victims to group by country and groups
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

        # Find the most frequently group
        top_group_by_country = {}
        for code, group_counts in country_groups.items():
            top_group = max(group_counts.items(), key=lambda x: x[1])[0]
            top_group_by_country[code] = top_group

        # Load countries info
        country_list = self.rest_countries_client.get_country_info()
        country_lookup = {
            c["cca2"]: {
                "name": c["common"],
                "lat": c["lat"],
                "lng": c["lng"]
            }
            for c in country_list
        }

        # Build enriched result
        result = []
        for code, victims in sorted_data:
            info = country_lookup.get(code.upper())
            result.append({
                "country": code,
                "victims": victims,
                "name": info.get("name", "Unknown") if info else "Unknown",
                "lat": info.get("lat", 0.0) if info else 0.0,
                "lng": info.get("lng", 0.0) if info else 0.0,
                "top_group": top_group_by_country.get(code.upper(), "Unknown")
            })

        logger.info('Get heatmap info process successfully')

        return result


    def info_by_country(self, country_code: str) -> dict:
        """
        Returns a country-level summary combining:
        - Historical victims (/countryvictims)
        - Recent victims (/recentvictims), filtered by country
        It aggregates total historical and recent counts, top groups, top sectors, last attack date, and infostealer statistics.
        """
        code = country_code.upper()

        # Historical by country and ALL cached recent data
        data_by_country = self.web_client.get_country_victims(code) or []
        all_recent = self.cache_recent_victims.get() or []

        # Filter only the recent ones from this country
        recent = [
            r for r in all_recent
            if r.get("country", "").upper() == code
        ]

        if not data_by_country and not recent:
            return {
                "country": code,
                "total_recent": 0,
                "top_groups": [],
                "top_sectors": {},
                "last_attack": None,
                "infostealers": {}
            }

        # Initialize counters and date
        total_recent = len(recent)
        group_counter = Counter()
        sector_counter = Counter()
        last_attack_date = None
        infostealer_counter = Counter()

        # Processing historical and recents filtered
        for v in data_by_country + recent:
            # Groups
            grp = v.get("group_name")
            if grp:
                group_counter[grp] += 1

            # Sectors (empty → "Unknown")
            sec = v.get("activity") or "Unknown"
            sector_counter[sec] += 1

            # Last attack date
            dt_str = v.get("discovered") or v.get("attackdate")
            if dt_str:
                try:
                    dt = datetime.fromisoformat(dt_str)
                    if not last_attack_date or dt > last_attack_date:
                        last_attack_date = dt
                except Exception:
                    raise RansomwareException('Error getting last attack date', 500)

            # Infostealers
            inf = v.get("infostealer")
            if isinstance(inf, dict):
                stats = inf.get("infostealer_stats", {})
                for name, cnt in stats.items():
                    infostealer_counter[name] += cnt

        logger.info('Info by country process successfully')

        # Build and return
        return {
            "country": code,
            "total_recent": total_recent,
            "top_groups": [g for g, _ in group_counter.most_common(3)],
            "top_sectors": dict(sector_counter.most_common(3)),
            "last_attack": (last_attack_date.strftime("%Y-%m-%d %H:%M:%S")
                            if last_attack_date else None),
            "infostealers": dict(infostealer_counter.most_common(3))
        }


    
    def get_cert_info_by_country(self, country_code: str):
        certs = self.web_client.get_certs_by_country(country_code)
        return certs
