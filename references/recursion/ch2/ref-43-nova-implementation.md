---
ref_id: 43
chapters: [2]
type: web
source_url: https://github.com/microsoft/Nova
fetched: 2026-06-13
fetched_with: fetcher
citation: 'Nova reference implementation (github.com/microsoft/Nova)'
---

# Nova reference implementation (github.com/microsoft/Nova)

GitHub - microsoft/Nova: Nova: High-speed recursive zero-knowledge arguments from folding schemes · GitHub
Skip to content
Navigation Menu
Toggle navigation

            Sign in
          
Appearance settings
Platform
AI CODE CREATION
GitHub Copilot
Write better code with AI
GitHub Copilot app
Direct agents from issue to merge
MCP Registry
New
Integrate external tools
DEVELOPER WORKFLOWS
Actions
Automate any workflow
Codespaces
Instant dev environments
Issues
Plan and track work
Code Review
Manage code changes
APPLICATION SECURITY
GitHub Advanced Security
Find and fix vulnerabilities
Code security
Secure your code as you build
Secret protection
Stop leaks before they start
EXPLORE
Why GitHub
Documentation
Blog
Changelog
Marketplace
View all features
Solutions
BY COMPANY SIZE
Enterprises
Small and medium teams
Startups
Nonprofits
BY USE CASE
App Modernization
DevSecOps
DevOps
CI/CD
View all use cases
BY INDUSTRY
Healthcare
Financial services
Manufacturing
Government
View all industries
View all solutions
Resources
EXPLORE BY TOPIC
AI
Software Development
DevOps
Security
View all topics
EXPLORE BY TYPE
Customer stories
Events & webinars
Ebooks & reports
Business insights
GitHub Skills
SUPPORT & SERVICES
Documentation
Customer support
Community forum
Trust center
Partners
View all resources
Open Source
COMMUNITY
GitHub Sponsors
Fund open source developers
PROGRAMS
Security Lab
Maintainer Community
Accelerator
GitHub Stars
Archive Program
REPOSITORIES
Topics
Trending
Collections
Enterprise
ENTERPRISE SOLUTIONS
Enterprise platform
AI-powered developer platform
AVAILABLE ADD-ONS
GitHub Advanced Security
Enterprise-grade security features
Copilot for Business
Enterprise-grade AI features
Premium Support
Enterprise-grade 24/7 support
Pricing
Search or jump to...
Search code, repositories, users, issues, pull requests...

        Search
      
Clear
Search syntax tips

        Provide feedback
      
We read every piece of feedback, and take your input very seriously.
Include my email address so I can be contacted
    Cancel

    Submit feedback


        Saved searches
      
Use saved searches to filter your results more quickly
Name
Query

            To see all available qualifiers, see our 
documentation
.
          
    Cancel

    Create saved search


                Sign in
              

                Sign up
              
Appearance settings
Resetting focus
You signed in with another tab or window. 
Reload
 to refresh your session.
You signed out in another tab or window. 
Reload
 to refresh your session.
You switched accounts on another tab or window. 
Reload
 to refresh your session.
Dismiss alert
{{ message }}

        microsoft

/
Nova
Public
Notifications

You must be signed in to change notification settings
Fork
    
248

          Star

853
Code
Issues
10
Pull requests
12
Discussions
Actions
Projects
Models
Security and quality
0
Insights
Additional navigation options

          Code


          Issues


          Pull requests


          Discussions


          Actions


          Projects


          Models


          Security and quality


          Insights

microsoft/Nova
 main
Branches
Tags
Go to file
Code
Open more actions menu
Folders and files
Name
Name
Last commit message
Last commit date
Latest commit
History
378 Commits
378 Commits
.github/
workflows
.github/
workflows
benches
benches
examples
examples
src
src
.clippy.toml
.clippy.toml
.gitignore
.gitignore
CODE_OF_CONDUCT.md
CODE_OF_CONDUCT.md
Cargo.toml
Cargo.toml
LICENSE
LICENSE
README.md
README.md
SECURITY.md
SECURITY.md
SUPPORT.md
SUPPORT.md
rustfmt.toml
rustfmt.toml
View all files
Repository files navigation
README
Code of conduct
MIT license
Security
Nova: High-speed recursive arguments from folding schemes
Nova is a high-speed recursive SNARK (a SNARK is type cryptographic proof system that enables a prover to prove a mathematical statement to a verifier with a short proof and succinct verification, and a recursive SNARK enables producing proofs that prove statements about prior proofs).
More precisely, Nova achieves 
incrementally verifiable computation (IVC)
, a powerful cryptographic primitive that allows a prover to produce a proof of correct execution of a "long running" sequential computations in an incremental fashion. For example, IVC enables the following: The prover takes as input a proof 
$\pi_i$
 proving the first 
$i$
 steps of its computation and then update it to produce a proof 
$\pi_{i+1}$
 proving the correct execution of the first 
$i + 1$
 steps. Crucially, the prover's work to update the proof does not depend on the number of steps executed thus far, and the verifier's work to verify a proof does not grow with the number of steps in the computation. IVC schemes including Nova have a wide variety of applications such as Rollups, verifiable delay functions (VDFs), succinct blockchains, incrementally verifiable versions of 
verifiable state machines
, and, more generally, proofs of (virtual) machine executions (e.g., EVM, RISC-V).
A distinctive aspect of Nova is that it is the simplest recursive proof system in the literature, yet it provides the fastest prover. Furthermore, it achieves the smallest verifier circuit (a key metric to minimize in this context): the circuit is constant-sized and its size is about 10,000 multiplication gates. Nova is constructed from a simple primitive called a 
folding scheme
, a cryptographic primitive that reduces the task of checking two NP statements into the task of checking a single NP statement.
Details of the library
This repository provides 
nova-snark,
 a Rust library implementation of Nova over a cycle of elliptic curves. Our code supports three curve cycles: (1) Pallas/Vesta, (2) BN254/Grumpkin, and (3) secp/secq.
At its core, Nova relies on a commitment scheme for vectors. Compressing IVC proofs using Spartan relies on interpreting commitments to vectors as commitments to multilinear polynomials and prove evaluations of committed polynomials. Our code implements three commitment schemes and evaluation arguments:
Pedersen commitments with IPA-based evaluation argument
 (supported on all three curve cycles)
HyperKZG commitments and evaluation argument
 (supported on curves with pairings, e.g., BN254)
Mercury commitments and evaluation argument
 (supported on curves with pairings, e.g., BN254) - Mercury is an optimized variant that provides faster verification than HyperKZG
For more details on using HyperKZG or Mercury, please see the test 
test_ivc_nontrivial_with_compression
. Both HyperKZG and Mercury require a universal setup (the so-called "powers of tau"). See the 
Universal Setup
 section below for details on loading setup parameters.
We also implement a SNARK, based on 
Spartan
, to compress IVC proofs produced by Nova. There are two variants, one that does 
not
 use any preprocessing and another that uses preprocessing of circuits to ensure that the verifier's run time does not depend on the size of the step circuit. The preprocessing variant of Spartan is called MicroSpartan and is described in the 
MicroNova
 paper.
Prior to compression, the IVC proof is folded with a random instance, which makes the proof zero-knowledge. The details of this technique are described in the HyperNova paper.
Supported front-ends
A front-end is a tool to take a high-level program and turn it into an intermediate representation (e.g., a circuit) that can be used to prove executions of the program on concrete inputs. There are three supported ways to write high-level programs in a form that can be proven with Nova.
The native APIs of Nova accept circuits expressed with bellman-style circuits. See 
minroot.rs
 or 
sha256.rs
 for examples.
Circom: A DSL and a compiler to transform high-level program expressed in its language into a circuit. There exist middleware to turn output of circom into a form suitable for proving with Nova. See 
Nova Scotia
 and 
Circom Scotia
. In the future, we will add examples in the Nova repository to use these tools with Nova.
Cargo Features
The library provides several optional features:
Feature
Description
io
 (default)
Enables loading commitment keys from Powers of Tau files
evm
Enables EVM-friendly serialization
experimental
Enables experimental features like NeutronNova
test-utils
Enables insecure test utilities (random tau generation) - 
do not use in production
Example usage:
#
 Default features (includes io)

cargo build


#
 With EVM verifier support

cargo build --features evm


#
 With experimental NeutronNova

cargo build --features experimental
Tests and examples
By default, we enable the 
asm
 feature of an underlying library (which boosts performance by up to 50%). If the library fails to build or run, one can pass 
--no-default-features
 to 
cargo
 commands noted below.
To run tests (we recommend the release mode to drastically shorten run times):
cargo test --release

To run an example:
cargo run --release --example minroot

References
The following paper, which appeared at CRYPTO 2022, provides details of the Nova proof system and a proof of security:
Nova: Recursive Zero-Knowledge Arguments from Folding Schemes

Abhiram Kothapalli, Srinath Setty, and Ioanna Tzialla 

CRYPTO 2022
For efficiency, our implementation of the Nova proof system is instantiated over a cycle of elliptic curves. The following paper specifies that instantiation and provides a proof of security:
Revisiting the Nova Proof System on a Cycle of Curves

Wilson Nguyen, Dan Boneh, and Srinath Setty 

IACR ePrint 2023/969
The zero-knowledge property is achieved using an idea described in the following paper:
HyperNova: Recursive arguments for customizable constraint systems

Abhiram Kothapalli and Srinath Setty 

CRYPTO 2024
The following paper describes an on-chain efficient version of Nova. We have open-sourced components of MicroNova including the HyperKZG polynomial commitment scheme and the MicroSpartan SNARK (which is provided in 
ppsnark.rs
):
MicroNova: Folding-based arguments with efficient (on-chain) verification

Jiaxing Zhao, Srinath Setty, Weidong Cui, and Greg Zaverucha 

IEEE S&P 2025
Experimental: NeutronNova
The library includes an experimental implementation of NeutronNova. Enable with 
--features experimental
. Note that experimental features may have breaking changes between releases.
Universal Setup for HyperKZG and Mercury
HyperKZG and Mercury polynomial commitment schemes require a universal setup to generate the structured reference string (SRS). The setup is "universal" in the sense that a single setup can be reused across different circuits, and the same setup parameters can be shared with other KZG-based proof systems (such as Plonk and its variants).
For production deployments, you should use parameters from a ceremony such as the 
Ethereum Perpetual Powers of Tau
, which has 80+ participants providing strong security guarantees (only one honest participant needed for security).
Using Powers of Tau Files
Download PPOT files
 from the PSE S3 bucket:
https://pse-trusted-setup-ppot.s3.eu-central-1.amazonaws.com/pot28_0080/

Files are named 
ppot_0080_XX.ptau
 (powers 15-27) and 
ppot_0080_final.ptau
 (power 28).
(Optional) Prune files
 to reduce size (~18x smaller):
cargo run --example ppot_prune --features io -- --power 20 --output ./ptau_files
This creates 
ppot_pruned_XX.ptau
 files containing only the G1/G2 points needed for HyperKZG.
Load in your application
:
use
 nova_snark
::
nova
::
PublicParams
;
use
 std
::
path
::
Path
;
let
 pp = 
PublicParams
::
setup_with_ptau_dir
(
&
circuit
,
&
*
S1
::
ck_floor
(
)
,
&
*
S2
::
ck_floor
(
)
,
Path
::
new
(
"./ptau_files"
)
,
)
?
;
The library automatically selects the smallest available file with sufficient capacity for your circuit.
File Size Reference
Power
Max Constraints
Pruned Size
Original Size
15
32K
2 MB
36 MB
18
256K
16 MB
288 MB
20
1M
64 MB
1.1 GB
23
8M
512 MB
9 GB
28
256M
~16 GB
288 GB
Testing Only (Insecure)
For testing purposes only, you can generate keys with a random tau:
cargo run --example ptau_test_setup --features test-utils,io
Warning:
 These keys are insecure and must not be used in production.
Contributing
This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit 
https://cla.opensource.microsoft.com
.
When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.
This project has adopted the 
Microsoft Open Source Code of Conduct
.
For more information see the 
Code of Conduct FAQ
 or
contact 
opencode@microsoft.com
 with any additional questions or comments.
Additional guidelines
This codebase implements a sophisticated cryptographic protocol, necessitating proficiency in cryptography, mathematics, security, and software engineering. Given the inherent complexity, the introduction of subtle bugs is a pervasive concern, rendering the acceptance of substantial contributions exceptionally challenging. Consequently, external contributors are kindly urged to submit incremental, easily reviewable pull requests (PRs) that encapsulate well-defined changes.
Our preference is to maintain code that is not only simple, but also easy to comprehend and maintain. This approach facilitates the auditing of code for correctness and security. To achieve this objective, we may prioritize code simplicity over minor performance enhancements, particularly when such improvements entail intricate, challenging-to-maintain code that disrupts abstractions.
In the event that you propose performance-related changes through a PR, we anticipate the inclusion of reproducible benchmarks demonstrating substantial speedups across a range of typical circuits. This rigorous benchmarking ensures that the proposed changes meaningfully enhance the performance of a diverse set of applications built upon Nova. Each performance enhancement will undergo a thorough, case-by-case evaluation to ensure alignment with our commitment to maintaining codebase simplicity.
Lastly, should you intend to submit a substantial PR, we kindly request that you initiate a GitHub issue outlining your planned changes, thereby soliciting feedback prior to committing substantial time to the implementation of said changes.
Trademarks
This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow

Microsoft's Trademark & Brand Guidelines
.
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
About

        Nova: High-speed recursive zero-knowledge arguments from folding schemes
      
Resources

        Readme

License

     MIT license
    
Code of conduct

        Code of conduct
      
Security policy

        Security policy
      
        Uh oh!

There was an error while loading. 
Please reload this page
.
Activity
Custom properties
Stars
853

        stars
Watchers
19

        watching
Forks
248

        forks

          Report repository

Releases
No releases published
Packages
      
0
        Uh oh!

There was an error while loading. 
Please reload this page
.
        Uh oh!

There was an error while loading. 
Please reload this page
.
Contributors
        Uh oh!

There was an error while loading. 
Please reload this page
.
Languages
Rust
100.0%
Footer

        © 2026 GitHub, Inc.
      
Footer navigation
Terms
Privacy
Security
Status
Community
Docs
Contact

       Manage cookies
    

      Do not share my personal information
    

    You can’t perform that action at this time.
