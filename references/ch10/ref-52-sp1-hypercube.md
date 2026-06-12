---
ref_id: 52
chapters: [10, 11]
type: web
source_url: https://blog.succinct.xyz/sp1-hypercube/
fetched: 2026-06-12
fetched_with: fetcher
citation: 'Succinct Labs. SP1 Hypercube: Proving Ethereum in Real-Time. Blog, May 2025.'
---

# Succinct Labs. SP1 Hypercube: Proving Ethereum in Real-Time. Blog, May 2025.

SP1 Hypercube: Proving Ethereum in Real-Time
Home
Case Studies
Learn
About Us

                    Subscribe
                    
Home
Case Studies
Learn
About Us
Subscribe
Blog
/
SP1 Hypercube: Proving Ethereum in Real-Time
SP1 Hypercube: Proving Ethereum in Real-Time
by 
Succinct
May 20, 2025
4 min read
Outline
We’re excited to introduce SP1 Hypercube, our next generation zkVM, that delivers real-time proving for Ethereum. SP1 Hypercube is built from the ground up with a brand new proof system architected with multilinear polynomials. It achieves state of the art results in latency and cost, up to 5x better than SP1 Turbo, 
and
can prove over 93% of Ethereum blocks in under 12 seconds.
Real-Time Proving Is Here
Real-time Ethereum proving, aka the ability to prove mainnet Ethereum blocks in < 12 seconds, is the “space race” of zero-knowledge: a technical and symbolic breakthrough that felt out of reach, even 1 year ago. The ability to generate these low latency proofs has tremendous implications on Ethereum’s roadmap–including massively scaling the L1 without sacrificing verifiability, enabling more secure native rollups, and offering better interoperability throughout the ecosystem. By launching the 
EthProofs
 dashboard to track progress, the Ethereum Foundation ignited fierce competition amongst zkVM teams to claim the milestone first. 
With SP1 Hypercube, we combined novel cryptography techniques and relentless performance engineering to be the first to achieve this moonshot.
Benchmarks: 
We define real-time Ethereum proving as the ability to prove 90%+ of Ethereum mainnet blocks in under 12 seconds (given the block and merkle proof witnesses needed for stateless execution). With SP1 Hypercube, we've surpassed that benchmark: in our tests, 93% of blocks were proved in under 12 seconds, with an average proving time of just 10.3 seconds. 
For transparency, our measurements exclude the time required to fetch Merkle proofs via Ethereum RPCs (aka the required witness fetching for stateless execution). As for the remaining 7% of blocks, we believe performance can be further improved by adjusting Ethereum’s gas schedule to more accurately reflect the actual workload of the prover, better aligning computational cost with proof generation complexity.
SP1 Hypercube introduces end-to-end improvements across the entire prover stack, from efficient execution of individual RISC-V instructions to low-latency recursion. These optimizations enable real-time proving on Ethereum while requiring significantly fewer GPUs than SP1 Turbo (roughly 2x). From our benchmarks, a cluster capable of real-time proving > 90% of mainnet blocks with SP1 Hypercube requires ~160 4090 GPUs and can be built for ~$300-400k. With more cost-efficient hardware, we estimate that the cost to set up a cluster could reach ~$100k, and with our open-source prover and cluster implementation (to be released after the SP1 Hypercube audit finishes), we expect this to make it feasible for anyone to run their own real-time Ethereum prover.
A New Proof System, Purpose-Built for zkVMs
SP1 Hypercube marks a fundamental shift in how we design and implement proof systems for zkVMs. While previous versions of SP1, including SP1 Turbo, were built on a STARK-based architecture using Plonky3, we’ve spent the past year deeply investigating multilinear-based proof systems with our head of cryptography Ron Rothblum. What started as an exploration has become conviction: multilinears represent the future of zero-knowledge proofs. Over the past 6 months, we designed and implemented a brand new proof system from scratch to accelerate the field towards this reality.
Unlike traditional STARKs, which rely on univariate polynomials, SP1 Hypercube is built entirely on multilinear polynomials. That single shift unlocks powerful new capabilities. To understand the advantage, imagine polynomials as shapes: univariates are like spheres, elegant but inefficiently packed. Multilinears, on the other hand, are like rectangles, easy to tile, leaving no wasted space. This "packing efficiency" translates directly into faster prover performance and lower resource costs.
At the heart of the system is a new polynomial commitment scheme, the Jagged PCS, which enables a “pay only for what you use” architecture. This is paired with a highly optimized implementation of LogUp GKR, a multilinear-friendly sumcheck protocol, and together they form the foundation of SP1 Hypercube's performance gains. A research paper describing the jagged PCS is available 
here
.
We use this architecture to reach state-of-the-art proving speeds on consumer GPUs, with up to a 5x improvement for compute heavy workloads like loop and fibonacci and up to 2x for precompile-heavy workloads like Ethereum proving vs. SP1 Turbo (our previous state of the art zkVM).
While we’ve long focused on arithmetization and hardware performance, SP1 Hypercube reflects our growing focus on the full stack of zkVM performance, including theory and proof system design.	
Stay Tuned
SP1 Hypercube’s verifier and our codebase for proving Ethereum blocks are open-source 
here
 and 
here
 respectively. Over the next few months, SP1 Hypercube will be undergoing an audit. After the audit finalizes, we will be releasing a production-ready version with an open-source prover and cluster implementation that will allow anyone to run their own real-time Ethereum prover.
Reach out to us if you’re interested in being an early user of SP1 Hypercube or have a use case that can utilize real-time proving.

                            Written by 
Succinct
Recent Posts
An Experiment in Formal Verification with Claude
by 
Succinct
May 20, 2026
Written by Rahul Dalal

A few weeks ago, we announced VEIL, a compiler that adds zero-knowledge to hash-based multilinear proof systems with only ~3% prover overhead. 

The compiler relies on thirty pages of new cryptographic arguments that have not been peer-reviewed yet. As an additional check, we
Continue Reading
Introducing Confidential Transactions to OP Succinct
by 
Succinct
May 12, 2026
OP Succinct now supports data confidentiality, letting chains keep transaction data private while still settling to Ethereum. 

Polygon CDK is the first production-ready implementation to use this feature, letting institutions keep customer data private without fragmenting liquidity.
Continue Reading
Base Adds ZK Proofs to Base Azul with SP1
by 
Succinct
May 4, 2026
Base is partnering with Succinct to prove $7.4 billion in deposits with zero-knowledge proofs.
Continue Reading
Socials
Twitter / X
LinkedIn
GitHub
Succinct
Documentation
Careers
About Us
Explorer
Prove the World's Software
