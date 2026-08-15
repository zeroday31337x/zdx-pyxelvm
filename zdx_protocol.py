"""ZDX protocol metadata helpers.

Protocol version 1 remains wire-compatible. Spatial PNG is negotiated as an
optional feature descriptor so older v1 nodes can still exchange ordinary
messages while spatial workloads require an explicit capability match.
"""

from __future__ import annotations

import time


PROTOCOL_VERSION = 1
SPATIAL_FRAME_VERSION = 1
SPATIAL_PNG_FEATURE = "spatial-png-v1"


def envelope(message_type, payload=None, *, features=None):
    message = {
        "protocol_version": PROTOCOL_VERSION,
        "type": message_type,
        "timestamp": time.time(),
        "payload": payload or {},
    }
    if features:
        message["features"] = list(features)
    return message


def is_compatible(message):
    return message.get("protocol_version") == PROTOCOL_VERSION


def spatial_descriptor(layout) -> dict:
    """Return a wire-safe description of a spatial PNG execution contract."""
    if hasattr(layout, "to_dict"):
        layout = layout.to_dict()
    if not isinstance(layout, dict):
        raise TypeError("layout must be a dict or expose to_dict()")
    required = {"width", "height", "execution_rows"}
    missing = sorted(required.difference(layout))
    if missing:
        raise ValueError(f"spatial layout missing required fields: {', '.join(missing)}")
    return {
        "feature": SPATIAL_PNG_FEATURE,
        "spatial_version": SPATIAL_FRAME_VERSION,
        "layout": dict(layout),
    }
