# ZDX Parallel Pyxel VM Architecture

## Overview

ZDX Parallel Pyxel VM is a deterministic pixel-native virtual machine with a distributed node coordination layer.

The architecture separates:

- spatial VM execution
- spatial frame storage
- networking
- node identity
- capability discovery
- scheduling
- synchronization

## Spatial Machine Model

A spatial frame is a standards-valid RGB PNG. The decoded raster is the machine representation itself.

- **X/Y coordinate** = exact cell address and execution topology
- **R channel** = opcode inside the executable plane
- **G/B channels** = operands, immediates, addresses, or reserved fields
- **rows 0..N-1** = executable thread plane
- **remaining rows** = non-executable spatial storage plane

The current ISA remains the existing **16-opcode PyxelVM ISA**. Spatial execution does not introduce a source-language or bytecode reconstruction stage.

Runtime path:

```text
standards-valid PNG
        |
        v
PNG decompression
        |
        v
RGB raster
        |
        v
X/Y + RGB machine cells
        |
        v
16-opcode dispatch
        |
        v
register/shared-memory execution
```

A 256x256 RGB spatial frame contains 65,536 addressable 24-bit cells. With 8 executable rows, 248 rows remain available as non-executable storage, providing 190,464 raw storage bytes before PNG compression.

## Current Components

### VM Layer

Responsible for deterministic execution of PyxelVM programs. `SpatialPyxelVM` preserves the existing ISA while enforcing the spatial layout contract and preventing storage rows from entering the thread scheduler.

### Compiler Layer

`SpatialCompiler` writes executable rows and named storage regions into the same standards-valid PNG. Human-readable instructions are only a compile-time convenience; execution begins from the raster.

### Spatial Storage Layer

`SpatialFrame` provides exact coordinate addressing, 24-bit cell access, byte-region access, and bounded JSON regions. `SpatialPixelStore` can pack multiple agent-memory keys into one spatial PNG rather than using one PNG per key.

### Agent Runtime Layer

`ZDXAgentRuntime.run_spatial()` executes the spatial frame and can persist register state, shared memory, and the layout contract into agent memory.

### Protocol Layer

Provides:

- protocol versions
- message envelopes
- timestamps
- compatibility checks
- optional `spatial-png-v1` feature negotiation
- spatial layout descriptors

Protocol v1 remains compatible for legacy frames. Spatial workloads explicitly require the spatial capability.

### Frame Manifest Layer

Frame identity remains SHA-256 of the exact PNG bytes. Spatial geometry is metadata alongside that identity and never changes the executable raster.

### Identity Layer

Provides persistent node identity across restarts.

### Capability Layer

Reports available resources and VM features. Spatial-capable nodes advertise:

- `spatial-png-v1`
- `xy-addressing`
- `rgb24-isa16`
- `spatial-storage`

This allows workload placement to reject nodes that do not support the spatial machine model.

### Discovery Layer

Tracks:

- node announcements
- heartbeats
- stale nodes
- advertised VM capabilities

### Scheduler Layer

Provides capability-aware node selection. Spatial workloads carry explicit required VM features in their workload manifests.

### Synchronization Layer

Frames are transferred and verified by SHA-256 without mutation. Spatial geometry travels as synchronization metadata so the receiving node can validate the execution contract before running the frame.

## Compatibility Rules

1. The 16-opcode ISA is preserved.
2. Legacy non-spatial frames remain representable as `pixel-frame` workloads.
3. Spatial frames declare `execution_model=spatial-png` and `spatial_version=1`.
4. Storage rows are never executable.
5. Network transport must not decode and rewrite the raster.
6. A frame hash identifies the exact PNG bytes, not a re-encoded image.
7. Spatial workload scheduling requires explicit node capability support.

## Design Principles

- deterministic execution
- pixels execute directly after PNG raster decode
- exact spatial addressing
- standards-valid PNG artifacts
- explicit capability reporting
- local execution boundaries
- verifiable synchronization
- backward-compatible protocol metadata
- modular expansion

## Roadmap

- enforce spatial geometry validation across every frame in a SAVE_STATE chain
- spatial-aware scheduler placement policies
- Android/runtime capability gating before spatial workload assignment
- signed spatial frame manifests
- secure enrollment
- distributed spatial-frame testing harness
- production workload authorization
