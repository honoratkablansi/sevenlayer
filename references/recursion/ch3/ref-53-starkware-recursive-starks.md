---
ref_id: 53
chapters: [3]
type: web
source_url: https://www.starknet.io/blog/recursive-starks/
fetched: 2026-06-13
fetched_with: fetcher
citation: 'StarkWare, "Recursive STARKs" (2022)'
---

# StarkWare, "Recursive STARKs" (2022)

Recursive STARKs | Starknet
Skip to content
Developers
Developers Hub
SN Stack
Build with AI
Modular Ecosystem
Tools & Resources
Documentation
Cairo Book
Tutorials
Version Releases
Ecosystem
Projects and Tools
Ecosystem Projects
Crypto Wallets
Bridges & on-ramps
DeFi dApps
Block Explorers & Monitoring tools
Grants
Grants Overview
Seed Grants
Growth Grants
Community
Decentralization
Governance
Staking
Roadmap
Get Involved
Events
Ambassadors Program
Jobs
Community Forum
Online Communities
Resources
Layer 2
Discover Our Layer 2 Scaling Solutions
Account Abstraction
How AA improves Blockchain Usability
DEX Aggregator
Explore the Benefits of DEX Aggregators
AMM Crypto
Watch How AMMs Are Changing Crypto Trading
Blog
Glossary
FAQs
Media Kit
Network
Dune Dashboard
Starknet Status Page
Bridge
Earn
Menu
Home
  /  
Blog
Recursive STARKs
Aug 11, 2022 · 
 7
min read
ON THIS PAGE
TL;DR
Recursive Proving is live on Mainnet, scaling StarkEx apps as well as StarkNet with a single proof
It boosts scale, and delivers benefit in cost, and latency (a rare and exciting occurrence of scale and latency moving in tandem, and not being a tradeoff)
It sets the stage for L3 and other benefitsGo read the blog post on 
Recursive Proving
. It’s cool stuff 😉
Scaling up!
Recursive proofs — powered by Cairo’s general computation — are now in production. This marks a major boost to the power of L2 scaling with STARKs. It will quickly deliver a multifold increase in the number of transactions that can be written to Ethereum via a single proof.
Until now, STARK scaling has worked by “rolling up” tens or even hundreds of thousands of transactions into a single proof, which was written to Ethereum. With recursion, many such proofs can be “rolled up” into a single proof.
This method is now in production for a multitude of Cairo-based applications: apps running on StarkEx, StarkWare’s SaaS scaling engine, and StarkNet, the permissionless rollup.
The story so far
Since the first proof on Mainnet, in March 2020, the following developments have shaped how STARKs are used.
STARK-based scaling
In June 2020 the first STARK-based scaling solution — 
StarkEx
 — was deployed on Ethereum Mainnet. StarkEx has a Prover that performs large computations off-chain and produces a STARK-proof for their correctness, and a Verifier that verifies this proof on-chain. The constraints for this first deployment were “hand-written” by StarkWare’s engineers, thus greatly limiting feature velocity for StarkEx. We concluded that a programming language to support proving general computation is needed — Cairo.
Cairo
In the summer of 2020 Cairo made its 
first appearance on Ethereum Mainnet
. Cairo stands for CPU Algebraic Intermediate Representation (AIR), and includes a single AIR that verifies the instruction set of this “CPU”. It opened up the door for coding proofs for more complex business logic, for arbitrary computational statements, and for doing so in a faster and safer manner. A Cairo program can prove the execution of a single application’s logic. But a Cairo program can also be a concatenation of multiple such applications — SHARP.
SHARP
SHARP — a SHARed Prover — takes transactions from several separate apps, and proves them all in one single STARK-proof. Apps combine their batches of transactions, filling up the capacity of a STARK-proofs faster. Transactions are processed at an improved rate and latency. The next frontier: Recursive Proofs, but not merely for some hard-coded logic, but rather for 
general computation
.
To understand the full benefit of Recursive Proving it is worth understanding a little bit more about how (non-recursive) proving was performed by SHARP up until now. Drawing 1 depicts a typical non-recursive flow:
Here, statements arrive over time. When a certain capacity (or time) threshold is reached, a large combined statement (a.k.a Train) is generated. This combined statement is proven only once all the individual statements have been received. This proof takes a long time to prove (roughly the sum of time it takes to prove each statement individually).
Proving extremely large statements is eventually limited by available compute resources such as memory. Prior to recursion, this was effectively the limiting scalability barrier of STARK proving.
What is Recursive Proving?
With STARK proofs, the time it takes to prove a statement is roughly linear with the time it takes to execute the statement. In addition, if proving a statement takes T time, then verifying the proof takes roughly log(T) time, which is typically called “logarithmic compression”. In other words, with STARKs you spend much less time on verifying the statement than on calculating it.
Cairo
 allows expressing general computational statements that can be proven by STARK proofs and verified by the corresponding STARK verifiers.
This is where the opportunity to perform 
recursion
 kicks in: In the same way that we write a Cairo program that proves the correctness of thousands of transactions, we can also write a Cairo program that verifies multiple STARK proofs. We can generate a single proof attesting to the validity of multiple “up-stream” proofs. This is what we call Recursive Proving.
Because of the logarithmic compression and roughly linear proving time, proving a verification of a STARK proof takes relatively short time (expected to be just a few minutes in the near future).
When implementing Recursion, SHARP can prove statements upon their arrival. Their proofs can be merged over and over into recursive proofs in various patterns until, at a certain point, the resulting proof is submitted to an on-chain verifier contract. A typical pattern is depicted in Drawing 2:
Immediate Benefits of Recursive Proving
Reduced On-chain Cost
Off the bat, we achieve “compression” of multiple proofs into one, which implies lower on-chain verification cost per transaction (where each statement may include many transactions).
With recursion, the computational resources barrier (e.g. memory) that limited proofs size up until now, is eliminated, since each limited size statement can be proven separately. Hence, when using recursion, the effective Train size of recursion is almost unlimited, and the cost per transaction can be reduced by orders of magnitude.
In practical terms, the reduction depends on the acceptable latency (and the rate at which transactions arrive). In addition, since each proof is typically also accompanied by some output such as on-chain data, there are limits to the amount of data that can be written on-chain together with a single proof. Nevertheless, reducing cost by an order of magnitude and even better is trivially achievable.
Reduced Latency
The Recursive Proving pattern reduces the latency of proving large Trains of statements. This is the result of two factors:
Incoming statements can be proven 
in parallel
 (as opposed to proving an extremely large combined statement).
There is no need to wait until the last statement in the Train arrives to begin proving. Rather, proofs can be combined with new statements as they arrive. This means that the latency of the last statement joining a Train, is roughly the time it takes to prove that very last statement plus the time it takes to prove a Recursive Verifier statement (which attests to all those statements that have already “onboarded” this particular Train).
We are actively developing and optimizing the latency of proving the Recursive Verifier statement. We expect this to reach the order of a few minutes within a few months. Hence, a highly efficient SHARP can offer latencies from a few minutes up to a few hours, depending on the tradeoff versus on-chain cost per transaction. This represents a meaningful improvement to SHARP’s latency.
Facilitating L3
The development of the Recursive Verifier statement in Cairo also opens up the possibility of submitting proofs to StarkNet, as that statement can be baked into a StarkNet smart contract. This allows building 
L3 deployments on top of the public StarkNet
 (an L2 network).
The recursive pattern also applies to the aggregation of proofs from L3, to be verified by a single proof on L2. Hence, hyper-scaling is achieved there too.
More Subtle Benefits
Applicative Recursion
Recursion opens up even more opportunities for platforms and applications wishing to further scale their cost and performance.
Each STARK proof attests to the validity of a statement applied to some input known as the “public input” (or “program output” in Cairo terms). Conceptually, STARK recursion compresses two proofs with 
two
 inputs into 
one
 proof with two inputs. In other words, while the number of proofs is reduced, the number of inputs is kept constant. These inputs are then typically used by an application in order to update some state on L1 (e.g. to update a state root or perform an on-chain withdrawal).
If the recursive statement is allowed to be 
application-aware
, i.e. recognizes the semantics of the application itself, it can both compress two proofs into one 
as well as
 combine the two inputs into one. The resulting statement attests to the validity of the input combination based on the application semantics, hence the name Applicative Recursion (see Drawing 3, for an example)..
Here, Statement 1 attests to a state update from A to B and Statement 2 attests to a further update from B to C. Proofs of Statement 1 and Statement 2 may be combined into a third statement, attesting to the direct update from A to C. By applying similar logic recursively, one can reduce the cost of state updates very significantly up to the finality latency requirement.
Another important example of Applicative Recursion is to compress rollup data from multiple proofs. For example, for a Validity Rollup such as StarkNet, every storage update on L2 is also included as transmission data on L1, to ensure data availability. However, there is no need to send multiple updates for the same storage element, as only the final value of transactions attested to by the proof verified is required for data availability. This optimization is already performed within a 
single
 StarkNet block. However, by generating a proof per block, Applicative Recursion may compress this rollup data across 
multiple
 L2 blocks. This can result in significant cost reduction, enabling shorter block intervals on L2, without sacrificing the scalability of L1 updates.
Worth noting: Applicative Recursion may be combined with application-agnostic recursion as depicted earlier. These two optimizations are independent.
Reduced On-chain Verifier Complexity
The complexity of the STARK verifier depends on the kind of statements it is designed to verify. In particular, for Cairo statements, the verifier complexity depends on the specific elements allowed in the Cairo language, and, more specifically, the supported built-ins (if we use the CPU metaphor for Cairo, then built-ins are the equivalent of micro-circuits in a CPU: computations performed so frequently that they require their own optimized computation).
The 
Cairo language
 continues to evolve and offer more and more useful built-ins. On the other hand, the Recursive Verifier only requires using a small subset of these built-ins. Hence, a recursive SHARP can successfully support any statement in Cairo by supporting the full language in the recursive verifiers. Specifically, the L1 Solidity Verifier need only verify recursive proofs, and thus can be limited to a more stable subset of the Cairo language: The L1 Verifier need not keep up with the latest and greatest built-ins. In other words, verification of ever-evolving complex statements is relegated to L2, leaving the L1 Verifier to verify simpler and more stable statements.
Reduced Compute Footprint
Before recursion, the ability to aggregate multiple statements into one proof was limited by the maximal size of the statement that could be proved on available compute instances (and the time it could take to generate such proofs).
With recursion, there is no longer a need to prove such extremely large statements. As a result, smaller, less expensive and more available compute instances can be used (though more of those may be needed than with large monolithic provers). This allows deployment of prover instances in more physical and virtual environments than previously possible.
Summary
Recursive proofs of general computation now serve multiple production systems, including StarkNet, on Mainnet Ethereum.
The benefits of recursion will be realized gradually, as it continues to allow for new improvements, and it will soon deliver hyper-scale, cut gas fees, and improve latency by unlocking the potential of parallelization.
It will bring significant cost and latency benefits with it, together with new opportunities such as L3 and applicative-recursion. Further optimization of the Recursive Verifier is on-going and even better performance and cost benefits are expected to be provided over time.
Gidi Kaempfer
, Head of Core Engineering, StarkWare
Join our newsletter
Receive notifications on Starknet updates
May also interest you
Starknet’s Monthly Roundup: June 2024
Starknet's monthly recap for June 2024—covering Starknet over Bitcoin, cheaper fees, Starknet's updated roadmap, and more.
July 4, 2024
How Layer 2 scaling improves DeFi
Layer 2 scaling solutions boost DeFi by increasing transaction speed, reducing costs, and enhancing efficiency. Starknet’s implementation promises broader adoption and innovation.
June 30, 2024
What Are Layer 2 Scaling Solutions?
Built upon Layer 1 blockchains, Layer 2 scaling solutions process more transactions at lower costs, while remaining secure and decentralized.
June 23, 2024
Layer 2 ecosystem: Scaling blockchain for the future
Ethereum already fosters a thriving ecosystem of L2 solutions. We’ll focus on those here, offering brief descriptions of the major players.
June 6, 2024
Developers
Developers Hub
SN Stack
Build with AI
Modular Ecosystem
Documentation
Cairo Book
Tutorials
Version Releases
Ecosystem
Crypto Bridge
Ecosystem Projects
Crypto Wallets
Bridges & on-ramps
DeFi dApps
Starknet Grants
Starknet Status Page
Community
Events
Ambassadors Program
Jobs
Governance
Roadmap
Staking
Community Forum
Online communities
Resources
Blog
Glossary
FAQs
Media Kit
Account Abstraction
Privacy Policy
Terms & Conditions
Terms Of Use
