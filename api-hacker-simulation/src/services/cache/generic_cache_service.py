from src.services.cache.cache_policy import CachePolicyEnumType
from src.services.cache.cache_strategies import (
    StaticCacheStrategy,
    ParamCacheStrategy,
    MetadataAwareCacheStrategy
)

class GenericCacheService:
    def __init__(self, fetch_fn, key, policy: CachePolicyEnumType, metadata_fn=None, metadata_key=None):
        self.fetch_fn = fetch_fn
        self.key = key

        if policy == CachePolicyEnumType.STATIC:
            self.strategy = StaticCacheStrategy()
        elif policy == CachePolicyEnumType.PARAMETERIZED:
            self.strategy = ParamCacheStrategy()
        elif policy == CachePolicyEnumType.METADATA:
            if not metadata_fn or not metadata_key:
                raise ValueError("metadata_fn and metadata_key are required for METADATA cache policy.")
            self.strategy = MetadataAwareCacheStrategy(metadata_fn, metadata_key)
        else:
            raise ValueError(f"Unsupported cache policy: {policy}")

    def get(self, *args, **kwargs):
        return self.strategy.get(self.fetch_fn, self.key, *args, **kwargs)
