import os
import json
from abc import ABC, abstractmethod
import logging
import re


logger = logging.getLogger(__name__)


class BaseCacheStrategy(ABC):
    """
    Abstract base class for cache strategies.
    """
    def __init__(self, cache_dir: str = 'src/data/cache'):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    @abstractmethod
    def get(self, fecth_fn, key:str, *args, **kwargs):
        """
        Fetches data from the cache or calls the provided function to fetch it.
        """
        pass

class StaticCacheStrategy(BaseCacheStrategy):
    """
    Strategy for static cache, this strategy don't require date or any param. If the cache file exists returns it directly, otherwise, call a remote function to get data.
    """
    def __init__(self, cache_dir: str = "src/data/cache"):
        super().__init__(cache_dir)

    def get(self, fetch_fn, key: str, *args, **kwargs):
        """
        This function check if exists the cache file, if not exists
        it executes fetch_fn to get the data and save it.
        """
        file_path = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(file_path):
            with open(file_path) as f:
                return json.load(f)
        data = fetch_fn(*args, **kwargs)
        with open(file_path, "w") as f:
            json.dump(data, f)
        return data

    
class ParamCacheStrategy(BaseCacheStrategy):
    """
    Strategy for Param cache, this strategy require a param like countryCode
    """
    def __init__(self, cache_dir: str = "src/data/cache"):
        super().__init__(cache_dir)

    def get(self, fetch_fn, key: str, param: str, *args, **kwargs):
        safe_param = re.sub(r'[^a-zA-Z0-9_-]', '_', param)
        file_path = os.path.join(self.cache_dir, f"{key}_{safe_param}.json")
        if os.path.exists(file_path):
            with open(file_path) as f:
                return json.load(f)
        data = fetch_fn(param, *args, **kwargs)
        with open(file_path, "w") as f:
            json.dump(data, f)
        return data



class MetadataAwareCacheStrategy(BaseCacheStrategy):
    """
    Strategy for cahce that needs updated date.
    This caching strategy compares the current timestamp of the external data with a previously saved timestamp in a metadata file (metadata.json). It only fetches the data again if it has changed.
    """
    def __init__(self, metadata_fn, metadata_path: list[str], cache_dir: str = 'src/data/cache'):
        super().__init__(cache_dir)
        self.metadata_fn = metadata_fn
        self.metadata_path = metadata_path
        self.meta_file = os.path.join(self.cache_dir, "metadata.json")

    def _get_nested_key(self, data: dict, path: list[str]):
        """
        Allows access to a nested value in a dictionary:
        """
        current = data
        for key in path:
            if not isinstance(current, dict):
                return None
            current = current.get(key)
        return current


    def _set_nested_key(self, data: dict, path: list[str], value):
        """
        Similar to _get_nested_key, but modifies or creates the nested key.
        """
        current = data
        for key in path[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]
        current[path[-1]] = value


    def _get_cached_metadata_ts(self):
        """
        Get the cache metadata file
        """
        if not os.path.exists(self.meta_file):
            return None
        try:
            with open(self.meta_file) as f:
                metadata = json.load(f)
                return self._get_nested_key(metadata, self.metadata_path)
        except Exception:
            logger.error(f'An error has ocurred getting cached data')
            return None


    def _save_metadata_ts(self, ts: str):
        """
        Read metadata file if it exists, otherwise it creates an empty {} object, after insert or update the timestamp value where were indicate. Later, save the result.
        """
        data = {}
        if os.path.exists(self.meta_file):
            try:
                with open(self.meta_file) as f:
                    data = json.load(f)
            except Exception:
                logger.error(f'An error has ocurring reading     metadata file')
                pass
        self._set_nested_key(data, self.metadata_path, ts)
        with open(self.meta_file, "w") as f:
            json.dump(data, f)


    def get(self, fetch_fn, key: str, *args, **kwargs):
        """
        - Check if the cache is up to date by comparing the remote timestamp with the local one.
        - If it's not or the cached file doesn't exist, fetch the data and save it.
        - If the cache is valid, read the file and return the data directly.
        """
        json_path = os.path.join(self.cache_dir, f"{key}.json")
        remote_metadata = self.metadata_fn()
        current_ts = self._deep_get(remote_metadata, self.metadata_path)

        if current_ts is None:
            logger.warning(f'[MetadataCache] path not found {self.metadata_path} in metadata.')

        cached_ts = self._get_cached_metadata_ts()

        if current_ts != cached_ts or not os.path.exists(json_path):
            logger.info(f"[MetadataCache] Invalid or expired cache for '{key}'. Updating...")
            data = fetch_fn(*args, **kwargs)

            with open(json_path, "w") as f:
                json.dump(data, f)

            if current_ts:
                self._save_metadata_ts(current_ts)

            return data

        logger.info(f"[MetadataCache] Valid cache '{key}'.")
        with open(json_path) as f:
            return json.load(f)

    def _deep_get(self, data: dict, keys: list[str]):
        """
        Iterative way to get a value from a nested dictionary using a list of keys.
        """
        for key in keys:
            if not isinstance(data, dict):
                return None
            data = data.get(key)
            if data is None:
                return None
        return data

    # def _deep_get(self, data: dict, keys: list[str]):
    #     """
    #     Recursively way to get a value from a nested dictionary using a list of keys."""
    #     if not isinstance(data, dict):
    #         return None
    #     if not keys:
    #         return data
    #     return self._deep_get(data.get(keys[0]), keys[1:])
