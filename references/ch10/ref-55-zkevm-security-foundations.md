---
ref_id: 55
chapters: [10, 11]
type: web
source_url: https://blog.ethereum.org/2025/12/18/zkevm-security-foundations
fetched: 2026-06-12
fetched_with: fetcher
citation: 'Kadianakis, George. Shipping an L1 zkEVM #2: The Security Foundations. Ethereum Foundation Blog, December 2025.'
---

# Kadianakis, George. Shipping an L1 zkEVM #2: The Security Foundations. Ethereum Foundation Blog, December 2025.

Shipping an L1 zkEVM #2: The Security Foundations | Ethereum Foundation Blog
EF Blog
Search
Skip to content
Categories
R&D
Research & Development
Events
Events
Org
Organizational
ESP
Ecosystem Support Program
ETH.org
Ethereum.org
Sec
Security
Protocol
Protocol Announcements
Funding
Funding Coordination
EcoDev
Ecosystem Development
Languages
Search
Shipping an L1 zkEVM #2: The Security Foundations
Posted by George Kadianakis on December 18, 2025
Research & Development
Thanks to Arantxa Zapico, Benedikt Wagner, and Dmitry Khovratovich from the EF cryptography team for their contributions, and to Ladislaus, Kev, Alex, and Marius for the careful review and feedback.
The zkEVM ecosystem has been sprinting for a year. And it worked! We crossed the finish line for real-time proving!
Now comes the next phase: building something mainnet-grade.
From speed to security
In July, 
we published a north-star definition
 for realtime proving. Nine months later, the 
ecosystem crushed it
: proving latency dropped from 16 minutes to 16 seconds, costs collapsed 45×, and zkVMs now prove 99% of all Ethereum blocks in under 10 seconds on target hardware.
While the major performance bottlenecks have been cleared by the zkEVM teams, security still remains the elephant in the room.
The case for 128-bit provable security
Many STARK-based zkEVMs today rely on unproven mathematical conjectures to hit their security targets. Over the past months, STARK security has 
been going through a lot
, with foundational conjectures getting mathematically 
disproven
 by researchers. Each conjecture that falls takes bits of security with it: what was advertised as 100 bits might actually be 80.
The only reasonable 
path forward
 is 
provable security
, and 128 bits remains the 
target
. It's the security level 
recommended by standardization bodies
 and validated by real-world 
computational milestones
.
For zkEVMs, this isn't academic. A soundness issue is not like other security issues. If an attacker can forge a proof, they can forge anything: mint tokens from nothing, rewrite state, steal funds. For an L1 zkEVM securing hundreds of billions of dollars, the security margin is not negotiable.
Three Milestones
For us, security and proof size are both critical—but they're also in tension. More security typically means larger proofs, and proofs must stay small enough to propagate across Ethereum's P2P network reliably and in time.
We are setting three milestones:
Milestone 1: soundcalc integration
Deadline: End of February 2026
To measure security consistently, we created 
soundcalc
: a tool that estimates zkVM security based on the latest cryptographic security bounds and proof system parameters. It's a living tool and we plan to keep integrating the latest research and known attacks.
By this deadline, participating zkEVM teams should have their proof system components and all of their circuits integrated with soundcalc. This gives us a common ground for the security assessments that follow. (For reference, see examples of previous integrations: 
#1
, 
#2
)
Milestone 2: Glamsterdam
Deadline: End of May 2026
100-bit provable security (as estimated by soundcalc)
Final proof size ≤ 600 KiB
Compact description of recursion architecture and sketch of its soundness
Milestone 3: H-star
Deadline: End of 2026
128-bit provable security (as estimated by soundcalc)
Final proof size ≤ 300 KiB
Formal security argument for the soundness of the recursion architecture
Recent cryptographic and engineering advances make hitting the above milestones tractable: compact polynomial commitment schemes like 
WHIR
, techniques like 
JaggedPCS
, a bit of 
grinding
, and a well-structured 
recursion topology
 can all contribute to a viable path forward.
Recursion is particularly worth highlighting. Modern zkEVMs involve many circuits composed with recursion in custom ways, with lots of glue in between. Each team does it differently. Documenting this architecture and its soundness is essential for the security of the entire system.
The path forward
There's a strategic reason to lock in on zkEVM security now.
Securing a moving target is hard. Once teams have hit these targets and zkVM architectures stabilize, the formal verification work 
we've been investing in
 can reach its full potential. By H-star, we hope the proof system layer will have mostly 
settled
. Not frozen forever, but stable enough to formally verify critical components, finalize security proofs, and write specifications that match deployed code.
This is the foundation that is required to get to secure L1 zkEVMs.
Building foundations
A year ago, the question was whether zkEVMs could prove fast enough. That question is answered. The new question is whether they can prove soundly enough. We are confident they can.
On our end:
In January, we'll publish a post clarifying and formalizing the milestones above.
We will follow up with a technical post outlining proof system techniques for reaching the security and proof size targets.
At the same time, we will be updating Ethproofs to reflect this shift: highlighting security alongside performance.
We are here to help throughout this process. Reach out to the EF cryptography team.
The performance sprint is over. Now let's strengthen the foundations.
Previous post
Next post
Stay Updated
Subscribe to get email notifications about the topics you care about. Choose from research, events, security updates, and more.
Subscribe to Newsletter
Ethereum Foundation
•
Ethereum.org
•
ESP
•
Bug Bounty Program
•
Do-not-Track
•
Archive
Categories
Research & Development
•
Events
•
Organizational
•
Ecosystem Support Program
•
Ethereum.org
•
Security
•
Protocol Announcements
•
Funding Coordination
•
Ecosystem Development
