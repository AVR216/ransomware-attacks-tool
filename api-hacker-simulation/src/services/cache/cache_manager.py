import os
import json
from .base import CacheableEndpoint

class EndpointCacheManager:
    def __init__(self, endpoint: CacheableEndpoint, data_dir="src/data"):
        self.endpoint = endpoint
        self.data_dir = data_dir
        self.data_file = os.path.join(data_dir, f"{self.endpoint.cache_key()}.json")
        self.meta_file = os.path.join(data_dir, "metadata.json")
        os.makedirs(data_dir, exist_ok=True)

    def _read_metadata(self) -> dict:
        if not os.path.exists(self.meta_file):
            return {}
        try:
            with open(self.meta_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return {}

    def _write_metadata(self, metadata: dict):
        with open(self.meta_file, "w") as f:
            json.dump(metadata, f, indent=2)

    def _get_cached_last_updated(self):
        metadata = self._read_metadata()
        return metadata.get(self.endpoint.cache_key())

    def _update_metadata(self, last_updated: str):
        metadata = self._read_metadata()
        metadata[self.endpoint.cache_key()] = last_updated
        self._write_metadata(metadata)
        print(f"[CacheManager] Metadata actualizada: {self.endpoint.cache_key()} → {last_updated}")

    def _load_cached_data(self):
        if not os.path.exists(self.data_file):
            return []
        try:
            with open(self.data_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"[CacheManager] Error leyendo {self.data_file}: {e}")
            return []

    def _save_data(self, data: list):
        with open(self.data_file, "w") as f:
            json.dump(data, f)
        print(f"[CacheManager] Datos guardados: {self.data_file} ({len(data)} registros)")

    def get_data(self):
        cached_ts = self._get_cached_last_updated()
        remote_ts = self.endpoint.get_remote_last_updated()
        data_exists = os.path.exists(self.data_file) and os.path.getsize(self.data_file) > 0

        if cached_ts != remote_ts or not data_exists:
            print(f"[CacheManager] Cache actualizado para '{self.endpoint.cache_key()}'")
            data = self.endpoint.fetch_data()
            if data:
                self._save_data(data)
                if remote_ts:
                    self._update_metadata(remote_ts)
            return data
        else:
            print(f"[CacheManager] Usando cache local para '{self.endpoint.cache_key()}'")
            return self._load_cached_data()
