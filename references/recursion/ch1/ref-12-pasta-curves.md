---
ref_id: 12
chapters: [1]
type: web
source_url: https://electriccoin.co/blog/the-pasta-curves-for-halo-2-and-beyond/
fetched: 2026-06-13
fetched_with: fetcher
citation: 'Hopwood, "The Pasta Curves" (Zcash, 2020)'
---

# Hopwood, "The Pasta Curves" (Zcash, 2020)

The Pasta Curves for Halo 2 and Beyond - Electric Coin Company
Skip to content
Blog post
Electric Coin Company
ECC Blog
General
/
The Pasta Curves for Halo 2 and Beyond
The Pasta Curves for Halo 2 and Beyond

										Daira Hopwood					
November 23, 2020
One of the most enjoyable things we do at ECC is working on cutting-edge cryptography. In our continued effort to ensure that Zcash benefits as much as possible from groundbreaking crypto innovations, part of what we do is to design our own cryptographic constructs to improve performance and security. For the 
Halo 2 project
, we have designed a new cycle of elliptic curves, Pallas and Vesta, which we collectively refer to as the 
Pasta
 curves.
Using the same elliptic curves as other projects is helpful in numerous ways. As an example, the pairing-friendly curve 
BLS12-381
 that we designed for 
Sapling
 is now a 
de facto
 standard in the cryptocurrency world, being deployed in fundamental components of protocols 
such as Ethereum 2
. This has allowed us to benefit from other projects’ research and development in BLS12-381, and it has increased the opportunities for cross-platform interoperability.
Since we originally presented the Tweedle cycle of curves in the 
Halo paper
, we’ve had time to learn more about which engineering and cryptographic properties are useful (particularly the low-degree isogeny and 2-adicity tweaks described below). We invite projects that plan to deploy protocols using ideas from Halo to employ the same curve cycle, so that we can collectively benefit from shared analysis and engineering effort.
Curve Parameters
Pallas: y
2
 = x
3
 + 5 over GF(0x40000000000000000000000000000000224698fc094cf91b992d30ed00000001)

Vesta:  y
2
 = x
3
 + 5 over GF(0x40000000000000000000000000000000224698fc0994a8dd8c46eb2100000001)

Like the Tweedle curves, the Pasta curves form a cycle with one another: the order of each curve is exactly the base field of the other. This property is 
critical to the efficiency of recursive proof systems
. They are designed to be highly 2-adic, meaning that a large power-of-two multiplicative subgroup exists in each field. This is important for the performance of polynomial arithmetic over their scalar fields and is essential for protocols similar to 
PLONK
.
Several other criteria are meant to ensure that the curves perform well and have nice symmetries:
Unlike with the Tweedle curves, both Pallas and Vesta have low-degree 
isogenies
 (both of degree 3) from curves with a nonzero j-invariant. This is 
useful
 when hashing to the curve using the “
simplified SWU
” algorithm, and perhaps for other not-yet-known purposes.
They have the same 2-adicity, 32, unlike the Tweedle curves that had 2-adicity of 33 and 34. This simplifies implementations and may assist in square root performance (used for point decompression and internally to Halo 2) due to 
a new algorithm recently discovered
; 32 is more convenient for this algorithm.
They are both constructed over 255-bit prime fields. This gives 126-bit security against 
Pollard rho
 attacks, and allows the compressed representation of points to be an even 32 bytes.
Both moduli have sparse bit representations in order to improve the performance of 
Montgomery reduction
 and other common operations.
They both support an endomorphism that can be used to improve performance of scalar multiplication, similar to that available for secp256k1. This is even more useful after the 
recent expiry of related patents
.
They have the same curve equation, 
y
2
 = x
3
 + 5
. For curves using this cycle construction it is also the case that an 
x
-coordinate of zero is not valid, which allows a convenient representation of all zeroes for the point at infinity.
Both fields do not have 5-order, 7-order, etc. multiplicative subgroups, so that exponentiation by these small primes is a permutation — a crucial requirement for algebraic hash functions such as Rescue and Poseidon.
These curves can be reproducibly obtained 
using a curve search utility we’ve published
. The tool uses 
various techniques
 to quickly search the large space of elliptic curves for a pair that satisfies our performance and security goals. For the Tweedle curves we also ensured that the quadratic twist security for both curves was high; this criterion has been dropped for the Pasta curves because it was only defence-in-depth (for curve formulae that we do not recommend using) and was too strict of a requirement that precluded other more important design considerations.
Naming
Pasta is a portmanteau of 
Pa
llas and Ve
sta
 — two minor planets in the solar system: 
2 Pallas
 and 
4 Vesta
. Like the curves, the minor planets are close in size; Pallas is the smaller minor planet and also the curve over the smaller base field. Pallas and Vesta were two of the earliest minor planets to be discovered, both by the German astronomer 
Heinrich Olbers
. They are visible with binoculars when in favourable positions [
2 Pallas
, 
4 Vesta
].
An unpublished 1805 work of 
Carl Friedrich Gauss
 connects 2 Pallas to the Halo proof system: Gauss developed a method of computing 
discrete Fourier transforms
, which are used in Halo, partly to track the orbit of this minor planet. His method was very similar to the one published in 1965 by 
James Cooley
 and 
John Tukey
, who are generally credited for the invention of the modern generic FFT algorithm.
In Greek mythology, Pallas (or 
Pallas Athena
) is a goddess associated with wisdom, handicraft, and warfare, while 
Vesta
 is a goddess of the hearth, home, and family. In the original 
Temple of Vesta
 in Rome stood the 
Palladium
, a statue of Pallas Athena. The 
sacred fire of Vesta
 and the Palladium were both held to be symbols of the safety and prosperity of Rome — just as we aim for these curves to provide a foundation for the future security of the Zcash protocol.
Pallas Athena
 and 
Vesta
 have another connection to Halo: they are the names of Artificial Intelligences in the universe of the 
Halo
 video games.
ECC engineers Sean Bowe and Jack Grigg contributed to this article.
General
Halo
The Zcash ecosystem: A 2020 recap
Zcash Gitcoin Grants round 1 retrospective
Recent blog posts:
Zashi 2.4.9 Is Faster!
Reorganizing Around Zcash User
Gemini Sets the Standard for Privacy on CEXs With Shielded ZEC Withdrawals
ECC Roadmap: Q4 2025
See all
Zodl
Blog
Careers
Zcash website
Manage cookies
Can we store cookies?
We sometimes use cookies to improve the performance of our website. Choose what you allow.
Customize
No
Yes
Consent Preferences
Close
Our Features
We sometimes use cookies to improve the performance of our website. Choose what you allow.

                                Essential                            
 Essential 

                                    Always Enabled                                
This includes key features like page navigation and logging you in. The website cannot function without this.


Who do we share data with?
Description
Google Analytics
Google Optimize
Google Tag Manager
New Relic
Sendgrid
Does this policy need cookies to work?


Yes.

                                Marketing                            
marketing
This tells us it's okay for us to use your information for marketing specifically.


Who do we share data with?
Description
Hotjar
Does this policy need cookies to work?


Yes.
No
Save My Preferences
Yes
