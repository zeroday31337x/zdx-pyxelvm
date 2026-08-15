# Open-Pyxel System Architecture Agreement

## Purpose

This document defines the coherence requirements between Open-Pyxel subsystems, ensuring that all features reinforce the primary mission:

**Fair distributed computation through verifiable, secure, and trustworthy systems.**

Every subsystem must be evaluated against these principles:

- Does it improve trust?
- Does it improve fairness?
- Does it improve verifiability?
- Does it preserve secure decentralized operation?

---

# Identity and Trust Chain

The network trust model follows:

Identity
→ Authentication
→ Verified Actions
→ Contribution History
→ Reputation
→ Network Trust
→ Permissions

Requirements:

- Identity must be cryptographically verifiable.
- Trust must be earned through observable behavior.
- Permissions must not bypass protocol rules.
- Reputation must be based on verified events.

---

# Compute Contribution Model

The compute lifecycle follows:

Work Assignment
→ Node Execution
→ Deterministic VM Result
→ Verification
→ Contribution Record
→ Trust/Credit Calculation

Requirements:

- Nodes cannot self-award contribution.
- Results must be reproducible.
- Metering must be authoritative.
- Verification must be independent from submission.

---

# Spatial PNG Machine Model

Spatial PNG is a first-class machine representation, not a transport disguise or a source-code wrapper.

Execution follows:

Standards-valid PNG
→ Raster Decode
→ X/Y + RGB Machine Cells
→ 16-Opcode VM Dispatch
→ Deterministic State Transition

Requirements:

- The PNG must remain standards-valid.
- Exact X/Y location is part of the machine semantics.
- RGB cells must execute directly after raster decode; no source-language or secondary-bytecode reconstruction is permitted in the execution path.
- Executable rows and non-executable storage rows must be separated by an explicit spatial layout contract.
- Storage pixels must never enter the instruction scheduler.
- The existing 16-opcode ISA remains the compatibility baseline unless a future version explicitly negotiates an ISA change.
- Frame identity is SHA-256 of the exact PNG bytes.
- Network transport must not decode and re-save a frame before verification or execution.
- Spatial workloads may only be assigned to nodes that explicitly advertise the required spatial VM capability.

---

# Security Model Alignment

Security flow:

Authentication
→ Authorization
→ Verification
→ Reputation
→ Enforcement

Requirements:

- Security events must affect trust appropriately.
- Enforcement must be evidence-based.
- Revocation paths must be defined.
- Recovery mechanisms must exist where appropriate.
- Spatial frame geometry and exact frame hash must be validated before execution.
- A node must fail closed when a spatial workload requires capabilities it did not advertise.

---

# Governance Alignment

Normal operation:

Protocol Rules
→ Network Operation

Exceptional situations:

Exceptional Event
→ Governance Review
→ Approved Decision

Requirements:

- No hidden creator authority.
- Security exceptions remain limited in scope.
- Future authority expansion requires network approval.

---

# Agent Architecture Alignment

Agents must follow:

Agent Identity
→ Authorization
→ Actions
→ Verification
→ Reputation

Agents must be:

- identifiable
- auditable
- containable
- subject to the same integrity standards

When agent memory uses spatial PNG storage, model-generated data must be written only to explicitly declared non-executable regions unless a separate compiler/authorization step intentionally creates executable machine cells.

---

# Economic Alignment

Future status, credits, and reputation must reflect:

- verified contribution
- reliability
- security participation
- trustworthy behavior

They must not be based on:

- ownership
- privileged access
- hidden advantages

---

# Review Requirement

Before major feature expansion:

1. Architecture impact review
2. Security impact review
3. Incentive alignment review
4. Documentation update
5. Testing requirements

Open-Pyxel development prioritizes:

Integrity → Security → Correctness → Maintainability → Features
