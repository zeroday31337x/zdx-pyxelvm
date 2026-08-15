"""
ZDX node capability reporting.

Provides a portable description of node resources without executing remote
workloads. Spatial PNG support is advertised explicitly so schedulers can avoid
assigning spatial workloads to nodes that only understand legacy linear frames.
"""

from __future__ import annotations

import os
import platform
import uuid
from dataclasses import dataclass, asdict


SPATIAL_VM_FEATURES = [
    "spatial-png-v1",
    "xy-addressing",
    "rgb24-isa16",
    "spatial-storage",
]


@dataclass
class NodeCapabilities:
    node_id: str
    os: str
    architecture: str
    cpu_count: int
    gpu: bool
    npu: bool
    vm_features: list[str]

    def to_payload(self):
        return asdict(self)


def detect_capabilities() -> NodeCapabilities:
    return NodeCapabilities(
        node_id=str(uuid.uuid4()),
        os=platform.system(),
        architecture=platform.machine(),
        cpu_count=os.cpu_count() or 1,
        gpu=False,
        npu=False,
        vm_features=[
            "pyxel-vm",
            "frame-hash",
            "deterministic-execution",
            *SPATIAL_VM_FEATURES,
        ],
    )


def supports_required_features(capabilities, required_features) -> bool:
    """Return True when a capability payload/node object satisfies a workload."""
    if isinstance(capabilities, NodeCapabilities):
        available = capabilities.vm_features
    elif isinstance(capabilities, dict):
        available = capabilities.get("vm_features", [])
    else:
        available = getattr(capabilities, "vm_features", [])
    return set(required_features or []).issubset(set(available or []))


def capability_message():
    from zdx_network import ZDXMessage

    return ZDXMessage(
        kind="capability_report",
        payload=detect_capabilities().to_payload(),
    )
