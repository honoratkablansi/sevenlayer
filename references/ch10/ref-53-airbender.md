---
ref_id: 53
chapters: [10, 11]
type: web
source_url: https://www.zksync.io/airbender
fetched: 2026-06-12
fetched_with: fetcher
citation: 'ZKsync. Airbender: GPU-Accelerated RISC-V Proving. June 2025.'
---

# ZKsync. Airbender: GPU-Accelerated RISC-V Proving. June 2025.

Airbender | ZKsync | ZKsync
New
Reflexivity: $600B+ in U.S. Bank Deposits Coming Onchain with ZKsync
$600B+ Bank Deposits Coming Onchain
→
 — read the announcement
Solutions
Products
Developers
Discover
Contact us
ZKsync Airbender
Fast proofs. Low costs.
Verifiable at scale.
Airbender is the world's fastest open source RISC-V prover, purpose-built to deliver block proofs in seconds at a fraction of a cent and scale efficiently on commodity hardware.
View documentation
Talk to our team
The Airbender advantage
Best-in-class performance
Airbender reaches 21.8 MHz on a single H100 GPU, more than 6x faster than competing zkVMs. Proofs cost as little as $0.0001 per transfer, making high-volume and even fee-free applications sustainable.
Fast proofs → fast finality
: Airbender provides sub-second block proofs and minutes-to-Ethereum finality
RISC-V proving
Airbender proves plain Rust code and any program compiled to RISC-V 32I+M, including EVM bytecode, WASM, and custom languages. No rewrites or proprietary formats required.
Commodity hardware
Airbender can prove an entire Ethereum block on a single GPU. From RTX 4090s to H100s, it delivers enterprise-grade performance without the need for massive clusters, keeping infrastructure simple and costs predictable.
Secure and adaptable
Built on STARKs and a modular design, Airbender is resilient against quantum threats and flexible enough to integrate new cryptographic standards as they emerge. Enterprises can adapt without costly re-engineering, ensuring long-term safety and compliance.
Open source
Airbender is MIT-licensed and fully transparent, including the GPU prover. Benchmarks and workflows are published on GitHub with reproducible results, so proofs can be verified independently without vendor lock-in.
Metric
Airbender
SP1 Turbo
Risc Zero
Proving throughput (H100)
21.8 MHz
3.45 MHz
1.1 MHz
GPUs per Ethereum block
1
50-160
30-80
Proof time per Ethereum block
~35 s
0s
45s
90s
~12 s (multi-GPU)
0s
45s
90s
~90 s
0s
45s
90s
License
MIT
Apache-2
BUSL
Hardware modes
CPU • 1 GPU • multi-GPU
1-GPU+
1-GPU+
Airbender
Proving throughput (H100)
21.8 MHz
GPUs per Ethereum block
1
Proof time per Ethereum block
~35 s
0s
45s
90s
License
MIT
Hardware modes
CPU • 1 GPU • multi-GPU
SP1 Turbo
Proving throughput (H100)
3.45 MHz
GPUs per Ethereum block
50-160
Proof time per Ethereum block
~12 s (multi-GPU)
0s
45s
90s
License
Apache-2
Hardware modes
1-GPU+
Risc Zero
Proving throughput (H100)
1.1 MHz
GPUs per Ethereum block
30-80
Proof time per Ethereum block
~90 s
0s
45s
90s
License
BUSL
Hardware modes
1-GPU+
Numbers sourced from public benchmark reports as of June 2025. Only open-sourced provers with reproducible results are included. Airbender results reproduced in open GitHub workflows.
Enterprise applications
Liquidity-Sensitive Finance
Order books, perps, and AMMs depend on fast clearing to reduce manipulation risk. Airbender’s high-throughput proofs shorten settlement delays, giving exchanges and market makers confidence to operate at scale with reduced counterparty exposure.
Regulated Asset Settlement
Tokenized securities and FX trades cannot wait minutes or hours to finalize. With Airbender generating fast proofs and ZKsync Connect enabling secure interoperability, ZKsync chains can shorten settlement cycles while meeting compliance-driven SLAs.
On-Chain AI Verification
Enterprises running AI models face growing pressure for auditability. Airbender allows ML inference results to be proven on affordable GPUs, creating a verifiable audit trail for regulators without adding prohibitive costs.
Distributed Proving
Global institutions face regulatory requirements for local processing. Airbender supports regional and branch-node proving, enabling proofs to be generated close to where data resides. This improves resilience, reduces latency for local users, and ensures regulatory alignment.
Accelerate your chain.
Lower your costs. Prove at scale.
Talk to our team
Documentation
Frequently asked questions
Everything you need to know about Airbender
Is Airbender ready for production?
Yes, Airbender is live on mainnet today. It is currently deployed in production powering chains which leverage the ZKsync Atlas Upgrade, delivering high-performance RISC-V proving with reproducible benchmarks.
Can it integrate with our existing systems?
Yes! Airbender is general purpose and can prove anything that can be compiled to RISC-V, including custom programs or entire chains.
When can ZKsync Chains use Airbender?
New ZKsync chains can ship immediately with Airbender.
What's the minimum hardware?
Development: laptop CPU. Production: Any GPU with 22GB RAM including 4090s, 5090s, L4s, or H100s.
Why does proof speed matter if Ethereum settlement takes minutes?
Faster proofs shorten chain-level finality, improve liquidity flow, and reduce counterparty risk well before Ethereum anchoring. In addition, Airbender is what enables ~1 second interoperability between chains within the Elastic Network, so assets and state can move across ZKsync chains almost instantly.
Won't hardware costs explode as throughput scales?
No. Airbender proves 9,700,000 cycles/sec on a single RTX 4090 and scales linearly across GPUs. This avoids runaway OPEX and GPU farm dependency.
Is Airbender vendor-locked to Matter Labs?
No. Airbender is MIT-licensed, fully open source, and reproducible from public repos. Enterprises can run it themselves or with any hosting provider.
What about quantum security?
Airbender is STARK-based and resilient against quantum attacks today. Its modular design allows upgrades as new cryptographic standards emerge.
Does Airbender support our existing stack?
Yes. Any program compiled to RISC-V can be proven, including EVM bytecode, WASM, Rust, or custom languages.
How much does proving cost in practice?
Proof costs can be as low as $0.0001 per transfer, verified in reproducible benchmarks.
Still have questions?
Can't find the answer you're looking for? Please talk to our team.
Get in touch
Where can I learn more?
Technical Deep-Dive
GitHub Repository
Solutions
Fintech
Intraday repo
Cross-border payments
Tokenized Deposits
Treasury Management
Products
ZKsync Stack
Prividium®
Airbender
solx
Developers
Documentation
Quick start
Support center
GitHub Discussions
Status page
What's happening
Blog
Community
Terms of Service
Privacy Policy
Cookie Policy
Brand
API License
Prividium Evaluation License
Prividium is a registered trademark of Matter Labs in the United States.
