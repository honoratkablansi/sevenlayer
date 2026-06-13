---
ref_id: 54
chapters: [3]
type: web
source_url: https://ethereum-magicians.org/t/a-rollup-centric-ethereum-roadmap/4698
fetched: 2026-06-13
fetched_with: fetcher
citation: 'Ethereum rollup-centric roadmap materials (Buterin, "A rollup-centric ethereum roadmap")'
---

# Ethereum rollup-centric roadmap materials (Buterin, "A rollup-centric ethereum roadmap")

A rollup-centric ethereum roadmap - ethereum-roadmap - Fellowship of Ethereum Magicians
Fellowship of Ethereum Magicians
A rollup-centric ethereum roadmap
layer-2
, 
            
ethereum-roadmap
vbuterin

                    October 2, 2020,  6:46am
                  
1
What would a rollup-centric ethereum roadmap look like?
Last week the Optimism team 
announced
 the launch of the first stage of their testnet, and the roadmap to mainnet. They are not the only ones; 
Fuel
 is moving toward a testnet and 
Arbitrum
 has one. In the land of ZK rollups, 
Loopring
, 
Zksync
 and the Starkware-tech-based 
Deversifi
 are already live and have users on mainnet. With 
OMG network’s mainnet beta
, plasma is moving forward too. Meanwhile, gas prices on eth1 are climbing to new highs, to the point where 
some non-financial dapps are being forced to shut down
 and 
others
 are running on testnets.
The eth2 roadmap offers scalability, and the earlier phases of eth2 are approaching quickly, but base-layer scalability for applications is only coming as the last major phase of eth2, which is still years away. In a further twist of irony, eth2’s usability as a data availability layer for rollups comes in phase 1, long before eth2 becomes usable for “traditional” layer-1 applications. These facts taken together lead to a particular conclusion: 
the Ethereum ecosystem is likely to be all-in on rollups (plus some plasma and channels) as a scaling strategy for the near and mid-term future
.
If we start from this premise, we can see that it leads to some particular conclusions about what the priorities of Ethereum core development and ecosystem development should be, conclusions that are in some cases different from the current path. But what are some of these conclusions?
The Short Term: Advancing Eth1 for Rollups
In the short term, one major outcome of this is that 
Ethereum base-layer scaling would primarily be focused on scaling how much data blocks can hold, and not efficiency of on-chain computation or IO operations
. The only determinant of the scalability of a rollup is how much data the chain can hold, and any increase beyond the current ~60 kB/sec will help increase rollups’ scalability further.
There are some things that would continue to matter at the base layer:
EIP 2929
, to ensure that the chain is safe against DoS attacks at current gas levels
EIP 1559
, both for the ETH burn and for the benefit of making it easy to send transactions that almost certainly get into the next block (which rollups still depend on for confirmations)
New elliptic curve precompiles, to fully support what people want to do with ZK rollups
The hex -> binary tree change and other changes to advance support for stateless clients (as stateless clients are valuable regardless of how the chain is being used)
Account abstraction is somewhat less important, because it can be implemented on L2 regardless of whether or not L1 supports it. Other “clever base layer features” also become relatively less important.
Eth1 clients could be repurposed as optimistic rollup clients
. Optimistic rollups still need to have full nodes, and if the rollup’s internal state transition rules are essentially ethereum-like with a few modifications (as is the goal of eg. Optimism), then existing code could be repurposed to run these full nodes. The work of separating out the consensus engine from the state transition engine is already being done 
in the context of the eth1+eth2 merge
, which can also help with this goal. Note in particular that this implies that 
projects like TurboGeth are still very important
, except it would be high-throughput rollup clients, rather than base-layer eth1 clients, that would benefit the most from them.
The Short Term: Adapting Infrastructure for Rollups
Currently, users have accounts on L1, ENS names on L1, applications live entirely on L1, etc. All of this is going to have to change. We would need to adapt to a world where users have their primary accounts, balances, assets, etc entirely inside an L2. There are a few things that follow from this:
ENS needs to support names being registered and transferred on L2
; see 
here
 for one possible proposal of how to do this.
Layer 2 protocols should be built into the wallet
, not webpage-like dapps. Currently, L2 integration into dapps/quasidapps (eg. Gitcoin’s zksync integration) requires the user to fully trust the dapp, which is a great decrease in security from the status quo. We ideally want to make L2s part of the wallet itself (metamask, status, etc) so that we can keep the current trust model. This support should be standardized, so that an application that supports zksync payments would immediately support zksync-inside-Metamask, zksync-inside-Status, etc.
We need more work on cross-L2 transfers
, making the experience of moving assets between different L2s as close to instant and seamless as possible.
More explicitly standardize on Yul or something similar as an intermediate compiling language
. Ethereum’s base-layer EVM and the OVM used in the Optimism rollup are slightly different compiling targets, but both can be compiled to from Solidity. To allow an ecosystem with different compiling targets, but at the same time avoid a Solidity monoculture and admit multiple languages, it may make sense to more explicitly standardize on something like Yul as an intermediate language that all HLLs would compile to, and which can be compiled into EVM or OVM. We could also consider a more explicitly formal-verification-friendly intermediate language that deals with concepts like variables and ensures basic invariants, making formal verification easier for any HLLs that compile to it.
Economic Sustainability Benefits of Rollup-Centrism
It’s an inescapable fact that a crypto project must be financially sustainable, and in 2020 this means millions or even tens of millions of dollars of funding. Some of this can be covered by common public-good-funding entities such as Gitcoin Grants or the Ethereum Foundation, but the scale of these mechanisms is just not sufficient to cover this level of funding. However, layer 2 projects launching their own token 
is
 sufficient - provided, of course, that the token is backed by genuine economic value (ie. prediction of future fees captured by the L2).
An important secondary benefit of a rollup-centric roadmap is that it leaves open space for L2 protocols, and these L2 protocols have the ability to collect fees/
MEV
 that can fund development, either directly or indirectly (by backing a token that funds development). The Ethereum base layer has an important need to be credibly neutral, making in-protocol public goods funding difficult (imagine ACD calls trying to agree on who deserves how much money), but L2s having their own public goods funding mechanisms (and/or contributing to Gitcoin Grants) is much less contentious. Leaving open this space can thus be a good strategic move for the long-term economic sustainability of Ethereum as a whole.
In addition to the funding issues, the most creative researchers and developers often 
want
 to be in a position of great influence on their own little island, and not in a position of little influence arguing with everyone else on the future of the Ethereum protocol as a whole. Furthermore, there are many 
already existing projects
 trying to create platforms of various kinds. A rollup-centric roadmap offers a clear opportunity for all of these projects to become part of the Ethereum ecosystem while still maintaining a high degree of local economic and technical autonomy.
The Long Term
In addition to these short-term concerns, a rollup-centric roadmap could also imply a re-envisioning of 
eth2’s long-term future: as a single high-security execution shard that everyone processes, plus a scalable data availability layer
.
To see why this is the case, consider the following:
Today, Ethereum has ~15 TPS.
If everyone moves to rollups, we will soon have ~3000 TPS.
Once phase 1 comes along and rollups move to eth2 sharded chains for their data storage, we go up to a theoretical max of ~100000 TPS.
Eventually, phase 2 will come along, bringing eth2 sharded chains with native computations, which give us… ~1000-5000 TPS.
It seems very plausible to me that when phase 2 finally comes, essentially no one will care about it. Everyone will have already adapted to a rollup-centric world whether we like it or not, and by that point it will be easier to continue down that path than to try to bring everyone back to the base chain for no clear benefit and a 20-100x reduction in scalability.
This implies a “
phase 1.5 and done
” approach to eth2, where the base layer retrenches and focuses on doing a few things well - namely, consensus and data availability
.
This may actually be a better position for eth2 to be in, because 
sharding data availability is much safer than sharding EVM computation
. While dishonest-majority-proof verification of sharded EVM computation requires fraud proofs, which require a strict and potentially risky two-epoch synchrony assumption, data availability sampling (if done with ZKPs or polynomial commitments) is safe under asynchrony.
This will help Ethereum distinguish itself as having a stronger security model than other sharded L2 chains, which are all going in the direction of having sharded execution of some form; eth2 would be the 
base layer that’s just powerful enough to have functionality escape velocity
, and no more powerful.
What could eth2 focus on in the long run?
Staggering block times on different shards, so that at any time there will always be some shard scheduled to propose a block within a few hundred milliseconds. This allows rollups that operate across multiple shards to have ultra-low latency, without the risks of the chain itself having ultra-low latency
Improving and solidifying its consensus algorithm
Adjusting the EVM to be more friendly to fraud proof verifications (eg. this could imply some kind of “frame” feature that prevents code from breaking out of a sandbox or allows SLOAD/SSTORE to be remapped to using something other than account storage as their data source)
ZK-SNARKing everything
Compromise Proposals
If you are not convinced to go “all the way” on the “phase 1.5 and done” direction, there is a natural compromise path to take: having a small number of execution shards (eg. 4-8) and many more data shards. The goal would be that the number of execution shards would still be low enough that in exceptional situations, regular computers would be able to fully validate all of them, but there would still be considerably more base-layer space than there is today.
Base-layer space cannot be minimized 
too
 much, as users and applications still need it to eg. move between rollups, submit fraud proofs, submit ZK proofs in ZK rollups, publish root ERC20 token contracts (sure, most users will live in rollups, but the base contract has to live 
somewhere
…), etc. And it would still be a large UX loss if those things cost $140 per transaction. Hence, if necessary, having 4-8 execution shards instead of 1 could provide significant relief. And it would still be possible for one computer to verify all shards; today, verifying eth1 blocks on average takes ~200-500 ms every 13 seconds, so verifying eight threads of such execution for short periods of time is completely feasible. One can imagine clients have policies like “if network latency appears low or committees are >80% full, rely on fraud proofs and committees, under exceptional conditions verify all shards directly”.
68 Likes
L2 Future Session 1: "Starting with L2s" - Intro, review of solutions, mapping out needs
Rollup-centric ethereum with sharding or rollup-centric sharding?
L2 Future Session 2 : “dApp development” - Intro, review of solutions, mapping out needs
L2 Future Session 3 : “users” - Expanding on what is needed to make L2s usable
Some medium-term dust cleanup ideas
EIP-4844: Shard Blob Transactions - Cancun upgrade
Taking a closer look at data availability policies in (Ethereum) rollups
souptacular

                    October 2, 2020,  8:41am
                  
2
I’m optimistic about most of this plan, but have some worries. Most of it comes down to how to implement much of this Layer 2 future while still keeping it simple enough for users and beginner devs of the system to not:
get tricked into losing ether/tokens/NFTs/etc.
have to decide on difficult trade-offs when they need to chose between multiple L2s.
have to keep up with various protocols/technologies to know if their tokens/things of value are secure.
It’s already pretty complicated for an average person to use Ethereum in the first place, let alone use it consistently without falling for scams. Incorporating different layers with different security guarantees and different requirements will put a lot of pressure on multiple areas of the ecosystem, especially user adoption and usability. I’m not saying we shouldn’t innovate and move forward and change when needed, but we do need to keep some of the things I listed in mind and spend more resources ideating on solutions. Otherwise we are just building Ethereum for the niche tech. people and not for the world.
20 Likes
vbuterin

                    October 2, 2020,  9:00am
                  
3
I absolutely agree with this. I do think it’s important to note that at least in the short term, as far as I can tell we have no choice. The L1 is nearly unusable for many classes of applications, and there’s no non-L2 path that can get us to scalability in the short-to-medium term. The $17.76 in fees it took me to make a bet on Augur last week itself makes present-day Augur very much “for the niche people and not for the world”. That said, I think there are ways to minimize the tradeoffs!
One major thing that I think we are already doing is to avoid (at least at first) trying to use layer 2s as an opportunity to try to “make a better VM”; instead, we should try to just keep things as close to the current EVM as possible. Also, we should maintain a hard commitment of what security properties a “legitimate layer 2” should have: if you have an asset inside the layer 2, you should be able to follow some procedure to unilaterally withdraw it, even if everyone else in the layer 2 system is trying to cheat you. We should put a lot of resources into security-auditing the major layer 2’s, and making sure they actually satisfy this requirement, and steer people toward the more solid and established solutions. Additionally (perhaps most importantly?), we should work with major wallets (metamask, status, imtoken?) to integrate support for the major L2s. L2s being inside the wallet and wallets being relatively trusted reduces the risk of people putting their coins into “fake L2s”.
I expect that a lot of the work will be done by the major defi projects, who have a large incentive to economize on fees and to make sure that their systems continue to be easy to use; we can do a lot by leaning on them as highly motivated early adopters. Even Gitcoin has already helped the ecosystem ease quite a bit into seeing what an L2-centric world will look like.
24 Likes
Beyond Stage 2: The Case for Unstoppable Ethereum Rollups
neverlander

                    October 2, 2020, 10:11am
                  
4
You mentioned a few rollup projects. Most of them are using fraud proofs as their security model (apart from Zksync and Deversifi). There seems to be a lot of excitement around these optimistic constructions, but don’t they suffer from the same drawbacks as Plasma? Shouldn’t ZK rollups be the preferred rollup system? The only drawback I see with ZKRs today is the proof generating complexity for arbitrary computation (or feasibility in the first place) but Matter labs’ Zinc and Starkware’s Cairo look promising. Would love to hear your thoughts on this.
6 Likes
vbuterin

                    October 2, 2020, 10:36am
                  
5
I definitely think that ZK rollups are better if possible for the reasons you mention!
The challenge with ZK rollups is that at present they’re not capable of supporting general-purpose EVM computation (though that may soon change, see Starkware’s efforts!), so at present we have to work with the optimistic variety. And the optimistic constructions are not that bad IMO; they suffer from 
some
 of the drawbacks of plasma, but not all; in particular, unlike plasma, optimistic rollups are easily extensible to generic EVM applications, which makes them much more suited to “scaling ethereum” generally, whereas plasma is only effective for payments, DEX and a few other use cases.
15 Likes
neverlander

                    October 2, 2020, 11:12am
                  
6
I wonder if in the future when ZKRs support general purpose computation, ORs (although less ‘elegant’) will still be the more popular variety. For these reasons:
There develops an attractive fraud proof market that pushes the OR narrative to a wider audience
Trusted service providers in the vein of Infura/Metamask emerge that provide a watcher service to automatically submit fraud proofs and an automated resolution service
DAOs that submit and resolve fraud proofs
Service providers that facilitate instant settlement to L1 for a fee (for taking on fraud risk)
Narrative that ZK proof construction requires special knowledge and/or relies on not so decentralized proof construction infrastructure
5 Likes
shogochiai

                    October 2, 2020, 11:40am
                  
7
I guess RU centric contract design might be needed especially for minting including contract -  all contracts have to have their “primary” contract in the L1 and secondary (=scalable) contract on the RU.
Eg, ERC-20 on the L1 and RU will have each own token issuance limit and those would run parallelly. How can those contract keep consistency when a mint function fired on RU?
My hottake is RU-specific ERC-20 (eg, ruDAI) tokens and enabling 1:1 conversion with general ERC-20. Anyway, some investigation of secure RU contract design would be needed.
2 Likes
gluk64

                    October 2, 2020, 11:58am
                  
8
Once ZKRs support full migration from Solidity, it’s game over. No single advantage left to ORs:
ZKRs have short finality/exit times (minutes vs. days in ORs).
ZKRs are cheaper (addresses, signatures and intermediate state hashes can be omitted).
ZKRs are A LOT 
more secure with large value locked in them
.
ZKRs support low-cost privacy (at least 100x more expensive in ORs).
ZKP generation can be much better decentralized due to its self-verifying nature than OR aggregation.
Fraud proof markets are a solution to the problem, they cannot drive adoption once the problem is not relevant anymore. It’s like saying that people won’t stream movies over the Internet because the video rental shops will push against it 
4 Likes
neverlander

                    October 2, 2020, 12:14pm
                  
9
I am bullish on ZKRs too but want to see if I can make a case for OR’s relevance once ZKRs for general computation is a reality
axic

                    October 2, 2020,  2:20pm
                  
10
 vbuterin:
More explicitly standardize on Yul or something similar as an intermediate compiling language
 . Ethereum’s base-layer EVM and the OVM used in the Optimism rollup are slightly different compiling targets, but both can be compiled to from Solidity. To allow an ecosystem with different compiling targets, but at the same time avoid a Solidity monoculture and admit multiple languages, it may make sense to more explicitly standardize on something like Yul as an intermediate language that all HLLs would compile to, and which can be compiled into EVM or OVM. We could also consider a more explicitly formal-verification-friendly intermediate language that deals with concepts like variables and ensures basic invariants, making formal verification easier for any HLLs that compile to it.
We (the Solidity team) had a discussion with the Optimisim team a few months ago, when they still had their Javascript/Typescript based transcompiler (which tried to identify functions based on the Solidity EVM output). We agreed that using Yul is a better direction,  and our estimate for “feature completeness” of the Solidity to Yul step (“Yul IR”) was the end of this year. The compiler progressed pretty well and a lot of well known contracts can be compiled to Yul now (such as Uniswap, Gnosis Safe, etc.)
I did not know there was a deadline for launch though, and obviously the Yul IR work is planned to take longer.
Besides that, we were lately talking about this exact topic you raise, to consider the requirements of layer 2 systems when designing the Solidity language. We are in the process of discussing a standard library and some ideas regarding dialects, which would definitely be helpful.
When the gas prices were close to 1000 gwei and given how Eth1x/Eth2 is progressing, I was rather worried that contracts become more like “system contracts” and every “user contract” moves to layer 2 – which means a shrinking user base for Solidity if we don’t support layer 2 systems.
3 Likes
masher

                    October 2, 2020,  3:23pm
                  
11
Very interesting trade-offs!
I have made a claim about this proposal on The Ether, which allows for signalling of if you are 
for
 the more roll-up centric road-map or 
against
 the more roll-up centric roadmap.
Additionally, it will allow you to see the top arguments on the 
for
 and 
against
 side.
I did my best to summarize the core points of 
@vbuterin
 and 
@souptacular
 discussion so far, but feel free to write your own arguments that are better than mine in order to flesh out the trade-offs
https://theether.io/claim/ethereum-should-move-to-being-roll-up-centric
snjax

                    October 2, 2020,  5:54pm
                  
12
How could you reach 100x advantage vs optimistic rollup?
For optimistic zk rollup we need to publish 2 nullifiers and 2 new utxos per transaction and one proof (2 compressed g1 and one g2 point).
This is 
20*2+20*2+4*32=208
 bytes per tx, published onchain.
Also, to keep the rollup working we should publish anywhere encrypted messages from users. A simple note is (amount, owner, salt), we should publish at least one note and ephemeral public key per tx. So, it is about 100 bytes and this cost should be the same for both zk and optimistic constructions.
1 Like
matt

                    October 2, 2020,  8:26pm
                  
13
I would like to throw 
EIP-726
 in the mix of protocol changes that would really help facilitate ORUs 
4 Likes
CryptoBlockchainTech

                    October 3, 2020,  7:11am
                  
14
You are a product of your own inability to take action against ASICs for almost 3 years now. They have increased network security costs so high that none of the GPU community was healthy enough to voluntarily take a cut in fees due to them finally getting to break even.
Very simple, remove ASICs from the network and you will have a very robust GPU mining community that has the ability to trim it’s belts in times of need to bolster the community.
Remove ASICs and bring back solid GPU mining to Ethereum and you would be suprised what we will do in return as some of the largest HODLrs.
2 Likes
vbuterin

                    October 3, 2020,  7:16am
                  
15
A zk zk rollup can go down to just publishing the nullifiers and utxos, and you can get the nullifiers down to 10 bytes as you don’t need collision resistance, so that’s 60 bytes (assuming an 80 bit security margin as you appear to be).
2 Likes
gluk64

                    October 3, 2020,  7:57am
                  
16
Besides:
There are schemes where the recipient does not need to transact immediately (cutting the data cost again by half).
@snjax
, you are talking about Groth16 with an app-specific trusted setup, which is hard to consider a viable, practical and trustworthy solution in 2020. You need a universal PLONK at the very least, but eventually you want to move to fully transparent proof systems (STARKs, RedShift, Halo). In either scenario the compressed proof size is on the order of kilobytes—and must be posted on-chain by optimistic rollups.
Of course, you could aggregate the proofs for many transactions in the block without checking them on-chain, but this construction would not be an optimistic rollup—it would be a ZK rollup with optimistic verification: combining the worst of both worlds.
1 Like
snjax

                    October 3, 2020, 10:55am
                  
17
You compare optimistic rollup with proving system, developed for zk rollup (in proving single transactions case) with zk zk rollups.
As you mentioned, the proof size will be some kilobytes. When for groth16 in optimistic rollup it’s 128 bytes per tx.
1 Like
gluk64

                    October 3, 2020, 11:31am
                  
18
Ok. Optimistic rollup is ~5x worse with Groth16, ~100x worse with anything without an app-specific trusted setup. We’ll let the reader make conclusions.
1 Like
snjax

                    October 3, 2020, 10:23pm
                  
19
Btw, is there any community approved methods to store off-chain data for private transactions (like encrypted utxo)? If both user and data storage forget the data, assets will be stuck. Also, if data storage forgets the data and the user could not send it directly to the receiver, assets will be stuck too.
1 Like
vbuterin

                    October 4, 2020, 12:04pm
                  
20
 gluk64:
Ok. Optimistic rollup is ~5x worse with Groth16, ~100x worse with anything without an app-specific trusted setup. We’ll let the reader make conclusions.
Wait, why 100x worse? PLONK proofs are only around 500 bytes, no?
1 Like
next page →
Home 
Categories 
Guidelines 
Terms of Service 
Privacy Policy 
Powered by 
Discourse
, best viewed with JavaScript enabled
