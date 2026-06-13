---
ref_id: 22
chapters: [1]
type: web
source_url: https://docs.nebra.one/
fetched: 2026-06-13
fetched_with: fetcher
citation: 'Nebra, "Universal Proof Aggregation" (UPA whitepaper, 2023)'
---

# Nebra, "Universal Proof Aggregation" (UPA whitepaper, 2023)

Introduction | NEBRA Docs
NEBRA Docs
⌘
Ctrl
k
NEBRA Home
Github
More
NEBRA Docs
Introduction
What is NEBRA UPA?
How it works
Quickstart
Developer Guide
UPA protocol specification
Integrating with zkVMs
Security and Transparency
Powered by GitBook
On this page
For the complete documentation index, see 
llms.txt
. This page is also available as 
Markdown
.
Copy
On this page
Introduction
Scale and compose zero-knowledge proofs on Ethereum.
NEBRA is a research & development organization working to make the zero-knowledge future a reality. We research and build technologies, infrastructure, and products to facilitate the mass adoption of zero-knowledge proofs. 
Our first step towards this goal is to scale the proof settlement capabilities of Ethereum in a trustless and censorship resistant manner. To achieve this, we are developing 
Universal Proof Aggregation
 technologies, to aggregate proofs generated from different circuits, different proof systems and different parties. 
The Problem: expensive ZKP onchain settlement
One of the biggest problems preventing the zero-knowledge future from becoming reality is the high cost of onchain settlement (verification). The table below shows the cost of verifying different kinds of zero-knowledge proofs on Ethereum today:
Proof System
Gas Cost
FIAT cost (30 gwei gas/ Ether 3000 USD)
Groth16
250,000
22.5 US Dollar
Halo2-KZG
400,000
36 US Dollar
STARK-FRI
1,500,000
105 US Dollar
This expensive proof verification cost means that only a few kinds of applications can be built today (namely those that can justify the high verification cost), and only a subset of users (those that can afford it) have access to proof verification. We believe that a future where onboarding to vote privately on a DAO costs $20 will exclude a majority of the world, a majority who we believe blockchain technology should also serve.
NEBRA proposes using zero knowledge proofs themselves to scale zero knowledge proof verification. As a result, zero knowledge proof settlement on Ethereum can be more accessible to the general public. The core idea is to use highly efficient recursive SNARKs (
IVCs
/
PCDs
) to get a near unlimited amount of recursion (almost) for free. This means we can recursively prove multiple zero-knowledge proofs 
off-chain
, and verify only 
a single aggregated proof
onchain
. This significantly improves on the status quo, and provides nearly unbounded efficiency.
Next
What is NEBRA UPA?
Last updated 
2 years ago
