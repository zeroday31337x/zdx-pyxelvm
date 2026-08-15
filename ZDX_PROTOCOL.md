# ZDX Protocol Layer

Protocol metadata provides:

- protocol versioning
- message type envelopes
- timestamps
- compatibility checks
- optional feature negotiation
- spatial frame descriptors

## Spatial PNG Compatibility

Protocol version 1 remains the wire version for both legacy and spatial workloads. Spatial support is negotiated as an optional feature rather than forcing a protocol-version break.

Spatial-capable nodes advertise:

```text
spatial-png-v1
xy-addressing
rgb24-isa16
spatial-storage
```

A spatial workload carries:

```text
execution_model: spatial-png
spatial_version: 1
spatial_layout:
  width: <pixels>
  height: <pixels>
  execution_rows: <rows>
```

The layout is a geometry contract, not a second executable representation. The PNG remains the executable artifact and its SHA-256 remains the frame identity.

Nodes that do not advertise `spatial-png-v1` must not be assigned a spatial workload. Legacy `pixel-frame` messages remain protocol-v1 compatible.

Future upgrades can negotiate additional spatial features without breaking existing nodes.
