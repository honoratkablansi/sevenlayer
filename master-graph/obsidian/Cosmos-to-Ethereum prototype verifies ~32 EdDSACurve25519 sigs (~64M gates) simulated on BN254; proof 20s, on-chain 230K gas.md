---
source_file: "references/recursion/ch3/ref-59-zkbridge.pdf"
type: "paper"
community: "Community 65"
location: "§6.1, §6.2"
tags:
  - graphify/paper
  - graphify/EXTRACTED
  - community/Community_65
---

# Cosmos-to-Ethereum prototype: verifies ~32 EdDSA/Curve25519 sigs (~64M gates) simulated on BN254; proof <20s, on-chain <230K gas

## Connections
- [[Block header relay network permissionless nodes relay C1 headers with ZK correctness proofs (trusted only for liveness)]] - `conceptually_related_to` [EXTRACTED]
- [[Data-parallel circuit N identical copies of a sub-circuit with no inter-copy wiring (e.g. N signature-verification copies)]] - `conceptually_related_to` [EXTRACTED]
- [[Groth16 outer wrapper proving the deVirgo verification circuit 131-byte proof, ~227K gas, 3 pairings on EVM-native BN254]] - `assumes` [EXTRACTED]
- [[deVirgo distributed zero-knowledge proof system parallelizing Virgo over M machines with perfect linear scalability and no proof-size overhead]] - `assumes` [EXTRACTED]
- [[zkBridge trustless cross-chain bridge via succinct proofs of consensus  light-client state transitions]] - `conceptually_related_to` [EXTRACTED]

#graphify/paper #graphify/EXTRACTED #community/Community_65