---
type: community
cohesion: 0.24
members: 10
---

# Quantum-Vulnerable Crypto & PQC Schedule

**Cohesion:** 0.24 - loosely connected
**Members:** 10 nodes

## Members
- [[Approval-status terms acceptable, deprecated, disallowed, legacy use]] - paper - references/ch07/ref-26-nist-ir-8547.pdf
- [[DeprecationDisallowance Schedule 112-bit deprecated after 2030, RSAECC disallowed after 2035]] - paper - references/ch07/ref-26-nist-ir-8547.pdf
- [[ECDSA (Elliptic Curve Digital Signature Algorithm)]] - paper - references/ch07/ref-26-nist-ir-8547.pdf
- [[Litinski (2023) computing a 256-bit ECC private key with ~50M Toffoli gates]] - paper - references/ch14/ref-63-harvest-now-decrypt-later.pdf
- [[Quantum-vulnerable digital signatures (ECDSA, EdDSA, RSA per FIPS 186)]] - paper - references/ch07/ref-26-nist-ir-8547.pdf
- [[Quantum-vulnerable key establishment (Finite FieldEC DH & MQV per SP 800-56A, RSA per SP 800-56B)]] - paper - references/ch07/ref-26-nist-ir-8547.pdf
- [[RSA Cryptosystem]] - paper - references/ch07/ref-24-shor.pdf
- [[RSA public-key cryptosystem (Rivest-Shamir-Adleman 1978)]] - paper - references/ch07/ref-24-shor.pdf
- [[RSA-2048 and ECC-256 (discrete log) are asymmetric schemes broken by Shor's algorithm; symmetric crypto is more resilient via larger keys]] - paper - references/ch14/ref-63-harvest-now-decrypt-later.pdf
- [[Shor's Algorithm]] - paper - references/ch07/ref-24-shor.pdf

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Quantum-Vulnerable_Crypto__PQC_Schedule
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Harvest-Now-Decrypt-Later]]
- 2 edges to [[_COMMUNITY_Folding & Lattice Crypto]]
- 2 edges to [[_COMMUNITY_Shor's Quantum Algorithms]]
- 2 edges to [[_COMMUNITY_PQC Transition (NIST IR 8547)]]
- 2 edges to [[_COMMUNITY_Shor Factoring Internals]]
- 1 edge to [[_COMMUNITY_Pairing & Discrete-Log Security]]

## Top bridge nodes
- [[Shor's Algorithm]] - degree 7, connects to 4 communities
- [[DeprecationDisallowance Schedule 112-bit deprecated after 2030, RSAECC disallowed after 2035]] - degree 5, connects to 2 communities
- [[RSA-2048 and ECC-256 (discrete log) are asymmetric schemes broken by Shor's algorithm; symmetric crypto is more resilient via larger keys]] - degree 4, connects to 2 communities
- [[RSA Cryptosystem]] - degree 5, connects to 1 community
- [[Quantum-vulnerable key establishment (Finite FieldEC DH & MQV per SP 800-56A, RSA per SP 800-56B)]] - degree 3, connects to 1 community