---
ref_id: 56
chapters: [3]
type: web
source_url: https://ethereum.org/en/roadmap/
fetched: 2026-06-13
fetched_with: fetcher
citation: 'ethereum.org zkEVM roadmap page'
---

# ethereum.org zkEVM roadmap page

Ethereum roadmap | ⁦ethereum.org⁩
Skip to main content
Overview
What is Ethereum?
What is the Ethereum network?
What is ether (ETH)?
What is Web3?
Ethereum vs Bitcoin
Smart contracts
Ethereum wallets
Gas fees
What are layer 2 networks?
Staking
Privacy on Ethereum
Ethereum security and scam prevention
Support
Test your knowledge
Videos
Start here
Choose your wallet
Get ETH
Explore apps
See all guides
Payments
Stablecoins
Prediction markets
See all use cases
Solo staking
Run a node
Pooled staking
Staking with a service
Layer 2 networks
Find an L2 network
Blockchain bridges
Builder's home
Builder tools & apps
Code tutorials
Learn by coding
Overview
Foundational topics
Ethereum stack
UX/UI design fundamentals
Founders
Institution & enterprise
Privacy for institutions and technical solutions
Community hub
Events calendar
Online communities
Devcon
Where to start
Grants
About ethereum.org
Contributing to ethereum.org
Translation Program
ethereum.org collectibles
Brand assets
Ethereum Whitepaper
Reports
Governance
Overview
Improved security
Cheaper transactions
Better user experience
Future-proofing
EIPs - Ethereum improvement proposals
ERCs
Bug bounty
Trillion-dollar security
Energy consumption
History & founders
Technical history
Open research
Data & analytics tools
Ethereum Foundation
Ethereum's development is community-driven and subject to change.
Ethereum roadmap
The path to more scalability, security and sustainability for Ethereum.
In production
Paris (The Merge)
September 15, 2022
In production
Shapella
April 12, 2023
In production
Dencun
March 13, 2024
In production
Pectra
May 7, 2025
In production
Fusaka
December 3, 2025
In development
Glamsterdam
H2 2026
In development
Hegotá
H2 2026
Previous slide
Next slide
Paris (The Merge)
September 15, 2022
Main features
Transition to Proof of Stake
Replaced energy-intensive mining with staking-based consensus
Reduced Ethereum's energy consumption by ~99.95%
Beacon Chain Integration
Merged the Beacon Chain with the Ethereum mainnet
Enabled the full transition to PoS consensus mechanism
Difficulty Bomb Removal
Removed the difficulty bomb that was increasing mining difficulty
Ensured smooth transition to the new consensus mechanism
Learn more
Shapella
April 12, 2023
Main features
Staking withdrawals
Enabled validators to withdraw their staked ETH and rewards
Introduced partial and full withdrawal capabilities
EIP-4895: Beacon chain push withdrawals
Added a new system-level operation for withdrawals
Ensured secure and efficient processing of withdrawal requests
EIP-3651: Warm COINBASE
Reduced gas costs for accessing the COINBASE address
Improved efficiency of certain smart contract operations
Learn more
Dencun
March 13, 2024
Main features
Proto-danksharding (EIP-4844)
Introduced blob transactions to significantly reduce rollup transaction costs
Added a new transaction type that stores data temporarily and cheaply
EIP-1153: Transient storage opcodes
Added TSTORE and TLOAD opcodes for temporary storage during transaction execution
Enables more efficient smart contract patterns and reduces gas costs
EIP-4788: Beacon block root in the EVM
Exposes consensus layer information to smart contracts
Enables new trust-minimized applications and cross-chain bridges
Learn more
Pectra
May 7, 2025
Main features
Enhance EOA wallets with smart contract functionality
Users can set their address to be represented by a code of an existing smart contract and gain benefits such as transaction batching, transaction fee sponsorship or better recovery mechanisms
Increase the max effective balance
Stakers can now choose an arbitrary amount of ETH to stake and receive rewards on every 1 ETH above the minimum
Blob throughput increase
The blob count will be increased from 3 to 6 targets, with a maximum of 9, resulting in cheaper fees in Ethereum rollups
Learn more
Track changes
 (opens in a new tab)
Fusaka
December 3, 2025
Main features
PeerDAS (Peer-to-Peer Data Availability Sampling)
Enables more efficient data availability for rollups
Makes running a node more accessible while maintaining decentralization
Blob Parameter Only (BPO) Forks
Allows flexible blob count increases between major upgrades
Enables faster adaptation to L2 scaling needs without waiting for coordinated hard forks
Gas Limit & DoS Hardening
Transaction gas limit cap of 16.7M gas per transaction
Default gas limit increase to ~60M (from current 45M)
Learn more
Track changes
 (opens in a new tab)
Glamsterdam
H2 2026
Main features
Enshrined proposer-builder separation
Separates block agreement from processing, helping L1 scale by allowing validators to process more data
Natively integrates builders so validators can safely outsource block assembly without trusting external software
Block-level access lists
Introduces mandatory access lists at the block level, rather than for individual transactions
Maps dependencies upfront for faster syncs, parallel execution, and parallel disk reads
Lowers gas for state-heavy apps and improves gas cost predictability
Learn more
Track changes
 (opens in a new tab)
Hegotá
H2 2026
Main features
Planned for Hegotá
Proposals are currently under discussion
Track changes
 (opens in a new tab)
Previous slide
Next slide
What changes are coming to Ethereum?
Ethereum
 is already a powerful platform, but it is still being improved. An ambitious set of improvements will upgrade Ethereum from its current form into a fully scaled, maximally resilient platform.
Cheaper transactions
Rollups are too expensive and rely on centralized components, causing users to place too much trust in their operators. The roadmap includes fixes for both of these problems.
More on reducing fees
Extra security
Ethereum is already very secure but it can be made even stronger, ready to withstand all kinds of attack far into the future.
More on security
Better user experience
More support for smart contract wallets and light-weight nodes will make using Ethereum simpler and safer.
More on user experience
Future-proofing
Ethereum researchers and developers are solving tomorrow's problems today, readying the network for future generations.
More on future-proofing
Why does Ethereum need a roadmap?
Ethereum gets regular upgrades that enhance its scalability, security, or sustainability. One of Ethereum's core strengths is adapting as new ideas emerge from research and development. Adaptability gives Ethereum the flexibility to tackle emerging challenges and keep up with the most advanced technological breakthroughs.
How the roadmap is defined
The roadmap is mostly the result of years of work by researchers and developers - because the protocol is very technical - but any motivated person can participate.
Ideas usually start off as discussions on a forum such as 
ethresear.ch
 (opens in a new tab)
, 
Ethereum Magicians
 (opens in a new tab)
 or the Eth R&D discord server. They may be responses to new vulnerabilities that are discovered, suggestions from organizations working in the application layer (such as dapps and exchanges) or from known frictions for end users (such as costs or transaction speeds).
When these ideas mature, they can be proposed as 
Ethereum Improvement Proposals
 (opens in a new tab)
. This is all done in public so that anyone from the community can weigh in at any time.
More on Ethereum governance
What technical upgrades are coming to Ethereum?
Danksharding
Danksharding makes L2 rollups much cheaper for users by adding "blobs" of data to Ethereum blocks.
Learn more
Single slot finality
Instead of waiting for fifteen minutes, blocks could get proposed and finalized in the same slot. This is more convenient for apps and difficult to attack.
Learn more
Account abstraction
Account abstraction is a class of upgrades that support smart contract wallets natively on Ethereum, rather than having to use complex middleware.
Learn more
Statelessness
Stateless clients will be able to verify new blocks without having to store large amounts of data. This will provide all the benefits of running a node with only a tiny fraction of today's costs.
Learn more
zkEVM
Zero-knowledge proofs could allow validators to verify Ethereum blocks without re-executing transactions, enabling higher gas limits without raising hardware requirements.
Learn more
What is the timeline for these upgrades?
Will Ethereum's roadmap change over time?
More
Yes—almost definitely.
 The roadmap is the current plan for upgrading Ethereum, covering both near-term and future plans. We expect the roadmap to change as new information and technology become available.
Think of Ethereum's roadmap as a set of intentions for improving Ethereum; it is the core researchers' and developers' best hypothesis of Ethereum's most optimal path forward.
When will the roadmap be finished?
More
Some upgrades are lower priority and likely not to be implemented for the next 5-10 years (e.g. quantum resistance). 
Giving precise timing of each upgrade is complicated
 to predict as many roadmap items are worked on in parallel and developed at different speeds. The urgency of an upgrade can also change over time depending on external factors (e.g. a sudden leap in the performance and availability of quantum computers may make quantum-resistant cryptography more urgent).
One way to think about Ethereum development is by analogy to biological evolution. A network that is able to adapt to new challenges and maintain fitness is more likely to succeed than one that is resistant to change, although as the network becomes more and more performant, scalable and secure fewer changes to the protocol will be required.
Do I have to do anything to prepare for these upgrades?
More
Upgrades tend not to impact end-users except by providing better user-experiences and a more secure protocol and perhaps more 
options
 for how to interact with Ethereum. 
Regular users are not required to actively participate in an upgrade, nor are they required to do anything** to secure their assets.
Node
 operators will need to update their clients to prepare for an upgrade. Some upgrades may lead to changes for application developers. For example, history expiry upgrades may lead application developers to grab historical data from new sources.
What about sharding?
More
Sharding is splitting up the Ethereum blockchain so that subsets of 
validators
 are only responsible for a fraction of the total data. This was originally intended to be the way for Ethereum to scale. However, 
layer 2
 rollups have developed much faster than expected and have provided a lot of scaling already, and will provide much more after Proto-Danksharding is implemented. This means "shard chains" are no longer needed and have been dropped from the roadmap.
Was this page helpful?
Yes
No
Website last updated: June 11, 2026
Go to top
ethereum.org
Learn
Learn Hub
What is Ethereum?
What is ether (ETH)?
Ethereum wallets
What is Web3?
Smart contracts
Gas fees
Run a node
Ethereum security and scam prevention
Quiz Hub
Ethereum glossary
Use
Guides
Choose your wallet
Get ETH
Application explorer
Stablecoins
NFTs - Non-fungible tokens
DeFi - Decentralized finance
DAOs - Decentralized autonomous organizations
Decentralized identity
Stake ETH
Layer 2
Build
Builder's home
Tutorials
Documentation
Start building
Learn Ethereum development
Grants
Foundational topics
UX/UI design fundamentals
Enterprise - Mainnet Ethereum
 (opens in a new tab)
Founders
Participate
Community hub
Online communities
Ethereum events
Contributing to ethereum.org
Translation Program
Ethereum bug bounty program
Ethereum Foundation
Ethereum Foundation Blog
 (opens in a new tab)
Ecosystem Support Program
 (opens in a new tab)
Devcon
 (opens in a new tab)
Research
Ethereum Whitepaper
Ethereum roadmap
Improved security
Technical history of Ethereum
Open research
Ethereum Improvement Proposals
Ethereum governance
Reports
Trillion dollar security project
GitHub
 (opens in a new tab)
Farcaster
 (opens in a new tab)
X
 (opens in a new tab)
Discord
 (opens in a new tab)
About us
Ethereum brand assets
Code of conduct
Jobs
Privacy policy
Terms of use
Cookie policy
Press Contact
 (opens email client)
