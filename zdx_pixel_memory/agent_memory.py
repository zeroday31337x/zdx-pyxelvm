"""
agent_memory.py — High-level memory interface for ZerodriveX AI agents.

Usage
-----
    from zdx_pixel_memory import ZDXAgentMemory

    mem = ZDXAgentMemory(agent_id="agent_01")
    mem.remember("user_name", "Zara")

    # Spatial mode packs all keys into one standards-valid PNG raster.
    spatial = ZDXAgentMemory(agent_id="agent_01", spatial=True)
    spatial.remember("task_history", ["search docs", "draft reply"])
"""

from .store import PixelStore
from .spatial_store import SpatialPixelStore


class ZDXAgentMemory:
    """Pixel-backed memory for a single ZerodriveX agent instance.

    ``spatial=False`` preserves the original one-PNG-per-key PixelStore.
    ``spatial=True`` packs the agent dictionary into the storage plane of one
    spatial PNG, allowing X/Y raster position to serve as the physical address
    space while preserving the same public memory API.
    """

    def __init__(
        self,
        agent_id: str = "default",
        base_dir: str = "zdx_memory/",
        *,
        spatial: bool = False,
        spatial_width: int = 256,
        spatial_height: int = 256,
        spatial_execution_rows: int = 0,
    ):
        self.agent_id = agent_id
        self.spatial = spatial
        if spatial:
            self._store = SpatialPixelStore(
                path=f"{base_dir}{agent_id}/memory.spatial.png",
                width=spatial_width,
                height=spatial_height,
                execution_rows=spatial_execution_rows,
            )
        else:
            self._store = PixelStore(store_dir=f"{base_dir}{agent_id}/")

    def remember(self, key: str, value) -> str:
        return self._store.write(key, value)

    def recall(self, key: str, default=None):
        return self._store.read(key, default=default)

    def forget(self, key: str) -> bool:
        return self._store.delete(key)

    def exists(self, key: str) -> bool:
        return self._store.exists(key)

    def keys(self) -> list:
        return self._store.keys()

    def snapshot(self) -> dict:
        return self._store.all()

    def update(self, data: dict):
        for key, value in data.items():
            self._store.write(key, value)

    def clear(self):
        if hasattr(self._store, "clear"):
            self._store.clear()
            return
        for key in self._store.keys():
            self._store.delete(key)

    def append(self, key: str, item):
        current = self._store.read(key, default=[])
        if not isinstance(current, list):
            raise TypeError(f"Memory key '{key}' is not a list")
        current.append(item)
        self._store.write(key, current)

    def recall_list(self, key: str) -> list:
        value = self._store.read(key, default=[])
        if not isinstance(value, list):
            raise TypeError(f"Memory key '{key}' is not a list")
        return value

    @property
    def capacity_bytes(self):
        return getattr(self._store, "capacity_bytes", None)

    def __repr__(self) -> str:
        keys = self._store.keys()
        mode = "spatial" if self.spatial else "pixel"
        return f"ZDXAgentMemory(agent_id={self.agent_id!r}, mode={mode!r}, keys={keys})"
