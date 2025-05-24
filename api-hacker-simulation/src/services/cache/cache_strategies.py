import os
import json
from abc import ABC, abstractmethod


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
    def __init__(self, cache_dir: str = "src/data/cache"):
        super().__init__(cache_dir)

    def get(self, fetch_fn, key: str, *args, **kwargs):
        file_path = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(file_path):
            with open(file_path) as f:
                return json.load(f)
        data = fetch_fn(*args, **kwargs)
        with open(file_path, "w") as f:
            json.dump(data, f)
        return data

    
class ParamCacheStrategy(BaseCacheStrategy):
    def __init__(self, cache_dir: str = "src/data/cache"):
        super().__init__(cache_dir)

    def get(self, fetch_fn, key: str, param: str, *args, **kwargs):
        file_path = os.path.join(self.cache_dir, f"{key}_{param}.json")
        if os.path.exists(file_path):
            with open(file_path) as f:
                return json.load(f)
        data = fetch_fn(param, *args, **kwargs)
        with open(file_path, "w") as f:
            json.dump(data, f)
        return data



class MetadataAwareCacheStrategy(BaseCacheStrategy):
    def __init__(self, metadata_fn, metadata_path: list[str], cache_dir: str = 'src/data/cache'):
        super().__init__(cache_dir)
        self.metadata_fn = metadata_fn
        self.metadata_path = metadata_path
        self.meta_file = os.path.join(self.cache_dir, "metadata.json")

    def _get_nested_key(self, data: dict, path: list[str]):
        current = data
        for key in path:
            if not isinstance(current, dict):
                return None
            current = current.get(key)
        return current

    def _set_nested_key(self, data: dict, path: list[str], value):
        current = data
        for key in path[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]
        current[path[-1]] = value

    def _get_cached_metadata_ts(self):
        if not os.path.exists(self.meta_file):
            return None
        try:
            with open(self.meta_file) as f:
                metadata = json.load(f)
                return self._get_nested_key(metadata, self.metadata_path)
        except Exception:
            return None

    def _save_metadata_ts(self, ts: str):
        data = {}
        if os.path.exists(self.meta_file):
            try:
                with open(self.meta_file) as f:
                    data = json.load(f)
            except Exception:
                pass
        self._set_nested_key(data, self.metadata_path, ts)
        with open(self.meta_file, "w") as f:
            json.dump(data, f)

    def get(self, fetch_fn, key: str, *args, **kwargs):
        json_path = os.path.join(self.cache_dir, f"{key}.json")

        remote_metadata = self.metadata_fn()
        current_ts = self._deep_get(remote_metadata, self.metadata_path)

        if current_ts is None:
            print(f"[MetadataCache] path not found {self.metadata_path} in metadata.")
        else:
            print(f"[MetadataCache] Remote date found: {current_ts}")

        cached_ts = self._get_cached_metadata_ts()

        if current_ts != cached_ts or not os.path.exists(json_path):
            print(f"[MetadataCache] Invalid or expired cache for '{key}'. Updating...")
            data = fetch_fn(*args, **kwargs)

            with open(json_path, "w") as f:
                json.dump(data, f)

            if current_ts:
                self._save_metadata_ts(current_ts)

            return data

        print(f"[MetadataCache] Invalid cache '{key}'.")
        with open(json_path) as f:
            return json.load(f)


    def _deep_get(self, data: dict, keys: list[str]):
        """
        Recursively get a value from a nested dictionary using a list of keys.
        """
        for key in keys:
            if not isinstance(data, dict):
                return None
            data = data.get(key)
            if data is None:
                return None
        return data

