# ZDX Parallel Pyxel VM Networking

## Architecture

The networking layer wraps the deterministic PyxelVM without changing execution.

```text
zdx_network.py
      |
zdx_node.py
      |
zdx_server.py
      |
zdx_sync.py
      |
zdx_cli.py
```

## Spatial Frame Transport

Spatial PNG support does not change the network's fundamental role: **transport moves frame bytes and metadata only**.

For a spatial workload the network may carry:

- exact PNG bytes
- SHA-256 of those exact bytes
- execution model (`spatial-png`)
- spatial version
- width / height
- executable row count
- optional named-region metadata
- required VM capabilities

The receiver validates the frame hash and geometry contract before local execution. Transport must not decode and re-save the PNG because doing so would change the exact artifact identity.

## Node Commands

Start a node:

```bash
python zdx_cli.py serve --port 8765
```

Ping a node:

```bash
python zdx_cli.py ping 127.0.0.1
```

Hash a frame:

```bash
python zdx_cli.py hash program.png
```

## Synchronization Model

Frames are identified by SHA-256 checksums.

Nodes exchange:

- identity messages
- heartbeat messages
- capability reports
- frame manifests
- spatial layout metadata when applicable
- integrity verification results

A spatial workload must only be assigned to a node that advertises `spatial-png-v1` and the other required VM features.

Network transport moves data only. VM execution remains deterministic and local:

```text
network receives exact PNG
        |
        v
hash + capability/layout verification
        |
        v
local PNG raster decode
        |
        v
local spatial PyxelVM execution
```

There is no network-side PNG-to-source or PNG-to-bytecode translation stage.

## Attribution

Developed by ZeroDriveX LLC.

https://zerodrivex.com
