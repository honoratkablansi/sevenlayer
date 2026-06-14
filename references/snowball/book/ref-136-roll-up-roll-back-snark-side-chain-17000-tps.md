---
ref_id: 136
chapters: []
type: web
source_url: https://ethresear.ch/t/roll-up-roll-back-snark-side-chain-17000-tps/3675
fetched: 2026-06-14
fetched_with: fetcher
citation: 'Roll up / roll back snark side chain ~17000 tps (ethresear.ch 2018)'
---

# Roll up / roll back snark side chain ~17000 tps (ethresear.ch 2018)

Roll_up / roll_back snark side chain ~17000 tps - zk-s[nt]arks - Ethereum Research
Ethereum Research
Roll_up / roll_back snark side chain ~17000 tps
zk-s[nt]arks
zk-roll-up
barryWhiteHat

                    October 3, 2018,  2:46pm
                  
1
Authors BarryWhitehat, Alex Gluchowski, 
HarryR
, Yondon Fu, Philippe Castonguay
Overview
A snark based side chain is introduced. It requires constant gas per state transition independent of the number of transactions included in each transition. This limits scalability at the size of snark that can be economically proven, rather than the 
gasBlockLimit/gasPerTx
 as 
proposed previous
.
Given a malicious operator (the worst case), the system degrades to an on-chain token. A malicious operator cannot steal funds and cannot deprive people of their funds for any meaningful amount of time.
If data become unavailable the operator can be replaced, we can roll back to a previously valid state (exiting users upon request) and continue from that state with a new operator.
System roles
We have two roles
the users, create transactions to update the state
the operator, uses snarks to aggregate these transactions into single on-chain updates.
They use a smart contract to interact. We have a list of items in a merkle tree that relates a public key (the 
owner
) to a non-fungible token.
Tokens can be withdrawn, but only once.
In snark transactions
The users create transactions to update the ownership of the tokens which are sent to the operator off-chain. The operator creates a proof that a
previous state
set of transactions
produce the 
newState
. We then verify the proof inside the EVM and update the merkle root if and only if the proof is valid.
Priority queue
The users are also able to request a withdrawal at the smart contract level. If the operator fails to serve this queue inside a given time limit, we assume data is unavailable. We slash the operator and begin looking for a new opeartor.
It is impossible to withdraw the same leaf twice as on a withdrawl we store each leaf that has been exited and check this for all future exits.
Operator auction
If a previous operator has been slashed we begin the search for a new operator. We have an auction where users bid for the right to be the operator giving a deposit and the state from which they wish to begin.
After a certain time, the new operator will be selected based on the highest bid (above a certain minimum) with the most recent sidechain state.
Roll back
When the operator is changed, we allow users to exit. The only reason a user needs to do this is if they got their token in a state that will be rolled back.
We order these withdrawals by state and roll back the chain processing transactions in that state until we get to the state where the new operator will continue from.
Note that since it is impossible to withdraw the same leaf twice, user cannot exit the same leaf from an older state.
Discussion
The operator is forced to process requests in the priority queue, otherwise they are slashed. If they refuse to operate the snark side of the system they are still forced to allow priority queue exits. Therefore, the system will degrade to an on-chain token if the operator becomes malicious.
A new operator should only join from a state for which they possess all the data. If not, they could be slashed by a priority queue request they can’t process.
A user should not accept a leaf as being transfered unless all the data of the chain is available so that they know in the worst case they can become the new operator if a roll back happens.
It is probably outside the regular users power to become an operator, but their coin will be safe as long as there is a single honest operator who wants to take over. Also bidding on a newer state will give them an advantage over all other bids.
This however allows the current operator to again become an operator because they will know the data of the most recent state and can bid on the latest state. However we can define a minimum stake that will be slashed again if they again refuse to serve the priority que. Therefor we can guarantee that someone will come forward to process the queue or else the chain will roll back to state 0 and users can exit as we roll back.
Unlike Plasma constructions that cannot guarantee the validity of all states, this design avoids competitive withdrawals since snarks disallow invalid state transitions. As a result, we can recover from scenarios with malicious operators without forcing all users to exit (however those that wish to exit can still do so).
Appendix
Appendix 1 Calculations of tps
Currently it takes ~500k constraints per signature. With optimization we think we can reduce this to 2k constraints.
Currently our hash function (sha256) costs 50k transactions per second. We can replace this with pedersen commitments which cost 1k constraints.
If we make our merkle tree 29 layers we can hold 536,870,912 leaves.
For each transaction we must
Confirm the signatures = 2k constraints
Confirm the old leaf is in the tree = 1k * 29 = 29k constraints
Add the new leaf and recalculate the root = 1k * 29 = 29k constraints
That equals 60k constraints per transaction.
wu et al
 report that they can prove a snark with 1 billion gates.
1000000000 / 60,000 = 16666 transactions per snark confirmation
Validating a snark takes 500k gas and we have 8 million gas per block. Which means we can include 16 such updates per block.
16666 * 16 = 266656 transactions per block
266656 / 15 = 17777 transactions per second.
We can probably reach bigger tps rates than this by building bigger clusters than they have.
Note: running hardware to reach this rate may be quite expensive, but at the same time much less than the current block reward.
40 Likes
SNARK based Side-Chain for ERC20 tokens
Short S[NT]ARK exclusion proofs for Plasma
Plasma World Map - the hitchhiker’s guide to the plasma
Building a decentralized exchange using snarks
Phase One and Done: eth2 as a data availability engine
fleupold

                    October 3, 2018,  3:51pm
                  
2
Question regarding exits during roll-backs that I might be misunderstanding:
 barryWhiteHat:
When the operator is changed, we allow users to exit. The only reason a user needs to do this is if they got their token in a state that will be rolled back.
Does this mean you would be able to exit a coin you got in a block that will no longer be part of the chain after rollback (e.g. we roll back to block 42, would we be able to exit a token received in block 44)?

Assuming that data for block 44 is unavailable how would someone be able to prove the exit is valid?
barryWhiteHat

                    October 3, 2018,  3:57pm
                  
3
You will have a chance during the roll back procedure to exit your coin from state 44. If you miss this chance you will lose your coin and the sender of the coin will regain ownership of it during the roll_back.
Once you exit a leaf that same leaf can ever be used to exit even if we roll back to before it was exited.
kaibakker

                    October 3, 2018,  5:49pm
                  
4
I really like how this project has progressed, the github repo for this project is available here: 
https://github.com/barryWhiteHat/roll_up
.
Below I try to explore the question: How would you make sure there is always an honest person ready to become an operator? What fees would make sense?
As an operator there are certain costs:
Servers for snark calculation and data availability.
Gas cost to validate & withdraw
The operator could recoup these costs in certain ways:
Deposit & withdraw fees
Transaction fees
Trustless interest (maximal 0.5% through PETH or DAI interest)
It is important that there is always a profitable strategy for a new operator otherwise nobody will pay for it. If no one will take the operation, fees might increase as a way to auction the operator spot.
An example at current gas prices:
Say an operator expects to update the snark every hour. He will spend approximately 0.50$ × 24 × 356 = 3560 + 812 = 4372$ a year on gas. He will process 50000 deposits and withdraws a year. Let’s say the operator only pays 0.10$ per withdraw, which would get to another 5000$. Server costs is another 4000$ and he expects a 5628$ yearly profit.
Totaling to 20000$ in expected revenue. He could charge 0.30$ per deposit or 3x the ethereum gas cost as a withdraw fee could make this business viable. It might be interesting to split the earned fees between the operators between withdraw, deposit and everyone in between.
1 Like
barryWhiteHat

                    October 3, 2018,  6:58pm
                  
5
What fees would make sense?
It depends upon the usecase. I want roll up to be usable for non fungible tokens, decentralized social media and a bunch of other use cases. There for we do not talk about the fee in this spec. Tho you could use deposit fees, or withdraw fees (excluding the priority que of course, that would mean that your withdraw fee would have to be less than the priority que fee to prevent fee evasion) if you want to do per tx fees you may need something like plasma debit which adds its own problems and benefits. At the moment i am unsure about which makes the most sense. I would like to see some full use cases and how they work before discussing.
How would you make sure there is always an honest entity ready to become an operator?
They don’t need to be honest. We just need someone to come forward and the best way seems to be to pay them. Again this depends upon the use case.
1 Like
PhABC

                    October 3, 2018,  7:21pm
                  
6
 kaibakker:
What fees would make sense?
You are right, it’s definitely costly to run a RU/RB operator (especially the proving part), but sometimes the operator is willing to take on the cost (e.g. centralized company). Fees make a lot of sense if you want to have somewhat of a guarantee that a new operator will “always” be found.
Tx fees could be somewhat easy if each user opens a payment channel with operator with an entry fee, something like :
Bob joins the side-chain and pays a 1$ entry fee and deposit 10$ for payment channel
Bob submits a tx
Operator include tx
Bob sends sign messages with 0.01$ to the operator.
Then,
If Bob doesn’t send the sign messages, operator stop including Bob’s transaction unless it’s an exit transaction. Bob lost 1$ with entry fee.
If operator doesn’t include Bob transaction, Bob doesn’t send the sign message (and can exit if Bob is being censored).
I think your other suggestions work as well.
 kaibakker:
How would you make sure there is always an honest person ready to become an operator?
Honesty
 is the easy part : If they don’t have the data they claim, there will be some txs they will not be able to execute and will be slashed. Plus they can’t commit invalid state transitions, so nothing to worry about. However, the risks of being an operator (losing your stake) and the cost (having all the equipment to be a good operator, storing all the data regularly, etc.) can be quite prohibitive. Hence the 
ready
 part is trickier. We would want to make the roll-back as small as possible.
Fees might be enough, but there is a big risk that the chain will roll back too far in the past if no-one is actually ready and keeping track of the data on a regular basis. One solution we are currently investigating is very similar to the notary system used with Casper. Basically, you could have group of “notaries” that stake on each root update (or every 
X
 root update), stating that they attest the data is available for 
epoch T
 and are ready to become the operator starting at this 
epoch T
 if the chain starts to roll back. In exchange, these notaries (and potential future operators) would receive part of the fees.
This create a strong incentive for notaries to be ready to become an operator and not lie about the data being available at 
epoch T
 (otherwise they might be slashed if the chain gets rollbacked and they are called to replace the operator). In addition of creating an incentive to rollback the chain as little as possible, this financial data availability attestation layer can offer some economic finality. Indeed, now the users know that if their transaction was included on chain at 
epoch T
 and that notaries staked $10m on this 
epoch T
, there is a $10m statement that 
epoch T
 will not be reverted. Put to its extreme and only using economic finality, RU/RB could drastically improve UX by not requiring users to store data, not having to care about roll-backs and only caring about whether their TXs are included in epochs that are notarized (hence finalized). In this extreme, you could remove the “exit challenge” when a rollback occurs, since all users would only consider a transaction to be valid if finalized (via notaries).
A lot more to explore, like put the operator and notaries under a single role, but we can wait for Casper’s spec to be finalized before trying to move there.
2 Likes
MihailoBjelic

                    October 4, 2018,  5:06pm
                  
7
@barryWhiteHat
 kudos for this and all your previous work! 
 barryWhiteHat:
We have a list of items in a merkle tree that relates a public key (the 
owner
 ) to a non-fungible token.
Is there a specific reason why the whole design is based on NFTs, do you see it working (with some modifications, of course) for the pubkey-balance model, too?
1 Like
On-chain scaling with full data availability. Moving verification of transactions off-chain?
barryWhiteHat

                    October 4, 2018,  8:45pm
                  
8
Balance model is tricky because you can withdraw the same balance twice by moving it from one leaf to another.
We could try and build plasma debit to add adjustable balances. But need to think about it more.
MihailoBjelic

                    October 4, 2018,  9:40pm
                  
9
 barryWhiteHat:
Balance model is tricky because you can withdraw the same balance twice by moving it from one leaf to another.
Sorry, I didn’t quite get you? How can you move your balance to another leaf, you have only one leaf representing your account (and its balance)? Maybe you’re thinking in terms of using SMTs strictly? If you have time, take a look at 
@jieyilong
’s post: 
Off-chain Plasma state validation with on-chain smart contract
 (you can read “Plasma State Construct” and “Probabilistic Plasma State Validation” sections only). I was thinking of something like that, but to use SNARKs instead of random sampling?
barryWhiteHat

                    October 5, 2018, 11:05am
                  
10
Not sure we are on the same page. Here is my response i hope its answering the questions you ask.
How can you move your balance to another leaf, you have only one leaf representing your account
If you cannot move balances between leaves then you don’t have account balance because the balance can never change. If you cannot move balances between leaves (excluding plasma debit) then you just have an input output model.
I was thinking of something like that, but to use SNARKs instead of random sampling?
I had a quick look. If you want to validate the integrity of a whole merkle tree , why not just validate each transaction? Making a proof for a large tree would require alot of hashes which are quite expensive.
Let me know if i am following you correctly 
MicahZoltu

                    October 5, 2018,  4:16pm
                  
11
 barryWhiteHat:
They don’t need to be honest. We just need someone to come forward and the best way seems to be to pay them. Again this depends upon the use case.
There needs to be at least one non-corrupt/non-colluding actor watching the system and willing to come forward.  This is often simplified to “honest”.  
The problem with just having a bond or something is that if everyone remains honest for an extended period of time, people may stop watching because there is no money in paying attention. At that point, the bond doesn’t do any good because no one is checking.  Ideally we would want a system that regularly rewards people for proving they are paying attention.  e.g., the actor submitting the rollup periodically tries to cheat, to make sure that the infrastructure exists to catch them if they actually cheat.
barryWhiteHat

                    October 5, 2018,  4:51pm
                  
12
 MicahZoltu:
There needs to be at least one non-corrupt/non-colluding actor watching the system and willing to come forward. This is often simplified to “honest”. 
Well we can replace honest with a rational actor who is acting in their own interest. They want to become the operator and make money. They don’t need to be honest or trusted.
 MicahZoltu:
The problem with just having a bond or something is that if everyone remains honest for an extended period of time, people may stop watching because there is no money in paying attention. At that point, the bond doesn’t do any good because no one is checking. Ideally we would want a system that regularly rewards people for proving they are paying attention. e.g., the actor submitting the rollup periodically tries to cheat, to make sure that the infrastructure exists to catch them if they actually cheat.
In order to receive payment you need to watch. Tho we can do some probabilistic tricks to reduce the cost for light clients.
The only way for the operator (“actor submitting rollup”) them to cheat is to make data unavailable. Even if no one is watching the operator cannot steal anyone tokens. It does mean its likely that we will roll back through the state they made when no one was watching if data becomes unavailable.
1 Like
jfdelgad

                    October 15, 2018, 10:26am
                  
13
I have a very basic question, just trying to understand. What data is finally send with the individual transactions, are the fields: to, from, value, and nonce included? why the cost of storing this data is not considered (68 gas per non-zero byte)?
gluk64

                    October 16, 2018,  3:34pm
                  
14
 jfdelgad:
What data is finally send with the individual transactions, are the fields: to, from, value, and nonce included? why the cost of storing this data is not considered (68 gas per non-zero byte)?
If data availability is handled on chain, we only need: from, to, amount. 4 bytes each. Nonce does not need to be public. In this case you are right, tx data cost is a limiting factor.
1 Like
snjax

                    November 2, 2018,  5:38pm
                  
15
What about using truebit protocol for block2block verification?

Publishing one step with groth16 proof in calldata/event weights about 100k gas.
kladkogex

                    January 10, 2019,  2:26pm
                  
16
I looked at the source code, and once thing which is not clear to me is ECDSA signature validation.
Normally when Ethereum users submit transactions, they sign using ECDSA, so before a transaction succeeds the ECDSA signature is validated.
ECDSA signature length is 64 bytes so if you want to include it in SNARK you are essentially limited to 30 TPS
Essentially what you gain is not including source and destination address and using indexes
barryWhiteHat

                    January 10, 2019,  9:20pm
                  
17
We user the snark to compress signatures. We don’t need to include EDDSA signtures as teh snark is implicit evidence that the signature exists.
vishal-sys

                    August 1, 2023,  8:51am
                  
18
hello i want to make a PDK (Parachain Development Kit) based on ZK-Snark project how can i start ? plz anyone can help me
1 Like
Home 
Categories 
Guidelines 
Terms of Service 
Privacy Policy 
Powered by 
Discourse
, best viewed with JavaScript enabled
