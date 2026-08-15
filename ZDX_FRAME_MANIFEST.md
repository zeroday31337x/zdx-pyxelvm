# ZDX Frame Manifest

Frame manifests provide deterministic metadata synchronization.

## Frame Identity

The authoritative frame identity remains the SHA-256 hash of the **exact PNG bytes**. Spatial support does not re-encode the image before hashing and does not move executable data into a sidecar representation.

Current fields include:

- SHA-256 frame hash
- byte size
- creation timestamp
- frame format
- execution model
- verification helper

For spatial frames, manifests additionally include:

- `spatial_version`
- `spatial_layout.width`
- `spatial_layout.height`
- `spatial_layout.execution_rows`
- capacity and named-region information exposed by the layout contract

## Spatial Contract

The layout describes how the receiving runtime interprets the raster:

- X/Y are exact cell locations
- executable rows enter the PyxelVM scheduler
- storage rows remain non-executable
- RGB is the 24-bit machine/data cell

The manifest describes the contract but is **not** executable machine code. Execution remains PNG raster -> opcode dispatch.

Future synchronization layers can use these manifests to reject incompatible node/runtime combinations before transferring or executing a workload.
