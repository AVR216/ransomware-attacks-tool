from abc import ABC, abstractmethod
from typing import List, Any

class CacheableEndpoint(ABC):

    @abstractmethod
    def cache_key(self) -> str:
        """Unique name for cache file"""
        pass

    @abstractmethod
    def fetch_data(self) -> List[Any]:
        """Fecth data from external API"""
        pass

    @abstractmethod
    def get_remote_last_updated(self) -> str:
        """Get last updated timestamp from remote API"""
        pass
