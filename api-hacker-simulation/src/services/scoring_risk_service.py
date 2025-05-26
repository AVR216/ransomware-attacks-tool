from typing import List, Optional
import json
import logging

from src.clients.ransomware_client import RansomwareClient
from src.services.cache.generic_cache_service import GenericCacheService
from src.services.cache.cache_policy import CachePolicyEnumType
from src.utils.scoring_risk import compute_group_risk

logger = logging.getLogger(__name__)

class RiskService:
    def __init__(self):
        self.web_client = RansomwareClient()
        
        # Cache recent victims for performance
        self.cache_recent_victims = GenericCacheService(
            fetch_fn=self.web_client.get_recent_victims,
            key="recentvictims",
            policy=CachePolicyEnumType.METADATA,
            metadata_fn=self.web_client.get_info,
            metadata_key=["Victims", "Last Update json"]
        )

    def get_group_risk(
        self,
        level: Optional[str] = None,
        top: int = 5
    ) -> List[dict]:
        """
        Returns a list of groups with their risk scoring.

        :param level: Filter by 'high', 'medium', or 'low' (optional)
        :param top: Number of top results to return (default is 5)
        """
        # Get data from cache
        raw = self.cache_recent_victims.get()
        victims = json.loads(raw) if isinstance(raw, str) else (raw or [])

        # Format data for scoring
        formatted: List[dict] = []
        for v in victims:
            group = v.get("group") or v.get("group_name") or "Unknown"
            country = v.get("country") or "Unknown"

            # Get infostealer stats safely
            inf_field = v.get("infostealer", {})
            stats = {}
            if isinstance(inf_field, dict):
                stats = inf_field.get("infostealer_stats") or inf_field or {}

            # Build formatted records
            if stats:
                for tactic in stats:
                    formatted.append({
                        "group_name": group,
                        "country": country,
                        "tactic": tactic
                    })
            else:
                formatted.append({
                    "group_name": group,
                    "country": country,
                    "tactic": "unknown"
                })

        # Compute risk scoring with z-scores
        df = compute_group_risk(formatted)

        # Define risk levels based on quantiles
        q1 = df["risk_score"].quantile(0.25)
        q3 = df["risk_score"].quantile(0.75)

        def level_fn(score: float) -> str:
            if score >= q3:
                return "high"
            if score >= q1:
                return "medium"
            return "low"

        df["risk_level"] = df["risk_score"].apply(level_fn)

        # Optional filter by risk level
        if level:
            df = df[df["risk_level"] == level]

        # Select top N by risk score
        df = df.sort_values("risk_score", ascending=False).head(top)

        # Extract relevant columns
        columns = [
            "group_name",
            "freq",
            "recurrence",
            "tactics",
            "risk_score",
            "risk_level"
        ]
        records = df[columns].to_dict(orient="records")

        logger.info('Process get group risk was successfully')
        return records