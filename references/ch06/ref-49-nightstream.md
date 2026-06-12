---
ref_id: 49
chapters: [6]
type: web
source_url: https://github.com/LFDT-Nightstream/Nightstream
fetched: 2026-06-12
fetched_with: fetcher
citation: 'LFDT-Nightstream. Nightstream: Lattice-Based Folding Implementation. GitHub, 2025.'
---

# LFDT-Nightstream. Nightstream: Lattice-Based Folding Implementation. GitHub, 2025.

GitHub - LFDT-Nightstream/Nightstream: Lattice zkVM (post-quantum zkVM) · GitHub
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

        LFDT-Nightstream

/
Nightstream
Public
Notifications

You must be signed in to change notification settings
Fork
    
8

          Star

27
Code
Issues
16
Pull requests
3
Actions
Projects
Security and quality
0
Insights
Additional navigation options

          Code


          Issues


          Pull requests


          Actions


          Projects


          Security and quality


          Insights

LFDT-Nightstream/Nightstream
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
920 Commits
920 Commits
.agents/
skills
.agents/
skills
.cargo
.cargo
.codex/
skills/
multi-ai-council
.codex/
skills/
multi-ai-council
.github/
workflows
.github/
workflows
.vscode
.vscode
crates
crates
demos
demos
formal
formal
scripts
scripts
wiki
wiki
.gitignore
.gitignore
ADOPTERS.md
ADOPTERS.md
AGENTS.md
AGENTS.md
CHANGELOG.md
CHANGELOG.md
CLAUDE.md
CLAUDE.md
CODE_OF_CONDUCT.md
CODE_OF_CONDUCT.md
CONTRIBUTING.md
CONTRIBUTING.md
Cargo.lock
Cargo.lock
Cargo.toml
Cargo.toml
LICENSE
LICENSE
MAINTAINERS.md
MAINTAINERS.md
README.md
README.md
SECURITY.md
SECURITY.md
TODO.md
TODO.md
clippy.toml
clippy.toml
file_aggregator.sh
file_aggregator.sh
rust-toolchain.toml
rust-toolchain.toml
rustfmt.toml
rustfmt.toml
show_diff.sh
show_diff.sh
View all files
Repository files navigation
README
Code of conduct
Contributing
Apache-2.0 license
Security
Nightstream: Lattice-based Folding for CCS
Nightstream is a 
post-quantum
 proving system built around a lattice-based folding scheme for 
CCS
 (SuperNeo, building on Neo, ePrint 2025/294) with a HyperNova-style recursive IVC layer. The active proving path targets CCS over the 
Goldilocks
 field with a degree-2 extension for sum-check soundness, Ajtai (module-SIS) commitments, and a Poseidon2-only transcript.
Status
: Research software under active development. 
neo-fold-clean
 is the main proving crate: it owns the lifecycle API, the F′ recursive-step circuit, and the decider. The earlier 
neo-fold-prototype
 sandbox (RV32IM/CHIP-8 end-to-end pipelines) has been removed from the tree. Chain-facing deployment wiring and independent audit are still unfinished. Not production-ready.
What Works Today
SuperNeo folding pipeline Π_CCS → Π_RLC → Π_DEC (
neo-reductions
, optimized + paper-exact engines)
IVC lifecycle in 
neo-fold-clean
: 
prove
 / 
extend
 a chain of CCS step instances, 
finish_uncompressed
 or 
compress
, then 
verify
F′ recursive-step shell: a low-norm bit-image layout, mixed-gate CCS structure, encoder, and R1CS compiler for stateful step functions
Spartan2-backed decider and terminal-CE relation checks
Red-team suites (
crates/neo-fold-clean/tests/system/lifecycle_redteam.rs
 and friends) for tamper resistance on the lifecycle path
Quick Start
Prerequisites
Rust
 stable (
rust-toolchain.toml
 at repo root)
git
C compiler (only if enabling allocators like mimalloc)
Build & Smoke Tests
cargo build --release


#
 Full workspace tests

cargo 
test
 --workspace --release


#
 Canonical end-to-end chain (encode F' steps, fold, finalize, verify)

cargo 
test
 -p neo-fold-clean --release --test system_fibonacci_bits_e2e -- --nocapture
WASM Demo (Browser)
See 
demos/wasm-demo/README.md
 for the full walkthrough. Quick build+serve:
./demos/wasm-demo/build_wasm.sh
./demos/wasm-demo/serve.sh
iOS Native (XCFramework)
Build a native iOS static library packaged as an XCFramework (for Swift/Xcode integration):
./scripts/build_ios_xcframework.sh
See 
demos/ios-demo/README.md
 and 
demos/android-demo/README.md
 for the native demo apps.
Paper-exact Reference Mode
Most tests use 
FoldingMode::Optimized
. The 
FoldingMode::PaperExact
 engine is an O(2^ℓ) brute-force reference for cross-checking only; it is not used in normal test runs.
Architecture Overview
neo-fold-clean
 is the main proving crate. Its module map:
crates/neo-fold-clean/src/
  lifecycle/        Public chain API: preprocess, prove, extend, compress,
                    finish_uncompressed, verify, verify_uncompressed(_audit)
  paper/            Paper-faithful protocol layer:
    construction2/  HyperNova-style IVC state transition + finalization
    reductions/     Π_CCS → Π_RLC → Π_DEC sequencing
    f_prime/        F′ step relation, R1CS lowering, Poseidon traces
    terminal_ce/    Terminal CE relation circuit + digest contract
    decider.rs      Decider-side x_out / state replay checks
    digest.rs       Poseidon2 structure/params/relation digests
  frontends/        F′ source-image frontends:
    f_prime/        Bit-image layout, mixed-gate structure, encoder,
                    stateful R1CS step compiler, recursive plan
    r1cs_f_prime/   Bellpepper-style R1CS → F′ instance builder
  engine/           Optimized execution: Π wrappers, CCS-native Poseidon2
                    gadgets, R1CS circuit builder, Spartan2 decider

Per-chunk Folding Flow
Each lifecycle step folds fresh CCS claims into the running accumulator via the SuperNeo triple:
incoming running accumulator + fresh CCS step claims
            │
            ▼
    ┌──────────────────┐
    │      Π_CCS       │  sum-check reduction over the CCS structure
    └────────┬─────────┘
             │   k fresh ME claims
             ▼
    ┌──────────────────┐
    │      Π_RLC       │  aggregate carry + fresh ME into one high-norm ME
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │      Π_DEC       │  decompose into k-1 low-norm ME children
    └────────┬─────────┘
             │
             ▼
   next running accumulator  →  carried to the next step

All Fiat-Shamir challenges are sampled from a Poseidon2 transcript; protocol-binding paths are Poseidon2-only.
Lifecycle API
use
 neo_fold_clean
::
lifecycle
;
let
 prep = lifecycle
::
preprocess
(
params
,
 structure
,
 public_input_len
)
?
;
let
mut
 audit = lifecycle
::
prove
(
&
prep
,
[
vec
!
[
step_0
]
]
)
?
;
// base step

audit = lifecycle
::
extend
(
&
prep
,
 audit
,
vec
!
[
step_1
]
)
?
;
// fold one more step

lifecycle
::
verify_uncompressed_audit
(
&
prep
,
&
audit
)
?
;
// replay-check the chain
let
 proof = lifecycle
::
finish_uncompressed
(
&
prep
,
 audit
)
?
;
// close the chain

lifecycle
::
verify_uncompressed
(
&
prep
,
&
proof
)
?
;
lifecycle::compress
 produces the Spartan2-compressed form checked by 
lifecycle::verify
.
Developer Onboarding
1. Read the Protocol + Implementation Docs
Doc
Purpose
docs/hypernova-paper/
HyperNova paper text (source for the IVC layer)
docs/architecture/
Design notes: terminal-CE proof, accumulator openings, perf
docs/audits/
Internal soundness-audit reports
docs/plans/
Design and implementation plans
formal/superneo-lean/README.md
Lean theorem-facing model (mathematical source of truth)
2. Run Tests
cargo 
test
 --workspace --release


#
 End-to-end F' chain: encode, fold, finalize, verify

cargo 
test
 -p neo-fold-clean --release --test system_fibonacci_bits_e2e -- --nocapture


#
 Lifecycle red-team (tamper-rejection) suite

cargo 
test
 -p neo-fold-clean --release --test system_lifecycle_redteam


#
 Reduction engines

cargo 
test
 -p neo-reductions --release
3. Where to Start in the Code
crates/neo-fold-clean/src/lifecycle/
 — the public chain API (
preprocess
, 
prove
, 
extend
, 
compress
, 
verify*
).
crates/neo-fold-clean/src/paper/construction2/
 — IVC state transition, x_out binding, finalization.
crates/neo-fold-clean/src/frontends/f_prime/
 — the F′ source image, structure, encoder, and the stateful R1CS step compiler.
crates/neo-reductions/src/api.rs
 — 
FoldingMode
 and the Π_CCS / Π_RLC / Π_DEC engine entry points.
Core Concepts (Paper → Code)
Concept
Meaning
Code entry points
CCS
Customizable Constraint System
neo_ccs::CcsStructure
MCS / CcsClaim
CCS + commitment
neo_ccs::CcsClaim
ME / CeClaim
Universal foldable claim (single-point matrix evaluation)
neo_ccs::CeClaim
Π_CCS
CCS/MCS → ME claims via sum-check
neo_reductions::api
, wrapped by 
neo-fold-clean/src/engine/
Π_RLC / Π_DEC
Aggregate then decompose (norm control)
neo-fold-clean/src/paper/reductions/
F′
Augmented recursive-step relation (HyperNova §6)
neo-fold-clean/src/frontends/f_prime/
Construction 2
IVC chain state + per-step fold proof
neo-fold-clean/src/paper/construction2/
Decider
Terminal check of the folded accumulator
neo-fold-clean/src/engine/decider.rs
, 
paper/terminal_ce/
Spartan2
Backend for compressed final proofs
crates/spartan2
Development Notes
Folding Engines
Mode
Description
FoldingMode::Optimized
Default; used in all normal tests and integration
FoldingMode::PaperExact
O(2^ℓ) reference engine, cross-check only
FoldingMode::OptimizedWithCrosscheck
Debug comparison mode
Per project policy in 
CLAUDE.md
, tests always use 
FoldingMode::Optimized
 unless the paper-exact engine is explicitly requested.
Debugging and Profiling
Perf snapshots live in 
crates/neo-fold-clean/tests/perf/
 and are 
--ignored
 by default:
#
 Lifecycle fold/IVC perf snapshot

cargo 
test
 -p neo-fold-clean --release --test perf_fibonacci_bits -- --ignored --nocapture fibonacci_bits_perf_snapshot


#
 Full-history audit-circuit R1CS shape handed to the decider

cargo 
test
 -p neo-fold-clean --release --test perf_fibonacci_bits -- --ignored --nocapture fibonacci_decider_r1cs_shape_snapshot
For CPU/memory profiling see 
scripts/profile_for_ai.sh
, 
scripts/profile_xctrace.sh
, and 
scripts/profile_memory_deep.sh
. Usage is documented in 
CLAUDE.md
.
Formal (Lean)
Subproject
Purpose
formal/superneo-lean/
Main SuperNeo theorem-facing model (source of truth)
formal/direct-ccs-fprime-lean/
Direct-CCS F′ model
formal/nightstream-lean/
Published-boundary model (prototype-era, parked)
formal/twist-shout-lean/
Twist/Shout memory-argument model
formal/opening-convergence-lean/
Opening convergence pipeline model
See 
CLAUDE.md
 for the spec/interface/implementation layout and closure standard.
Security & Correctness
Implemented Safeguards
Parameter validation
 for the RLC soundness bound (
neo-params
, SuperNeo Appendix B.2 profile)
Transcript binding
 via Poseidon2 domain separation across every phase (protocol-binding paths are Poseidon2-only)
Structure/params digests
 recomputed from authoritative inputs, never trusted from the wire
Red-team test suites
 (
crates/neo-fold-clean/tests/system/lifecycle_redteam.rs
, 
r1cs_compiler_stateful.rs
) for tamper resistance
Security Posture
Research software warning
: This repository demonstrates the protocol and transcript-binding structure but has not undergone independent review. Do not deploy without a full audit.
Specific caveats:
No independent audit or formal verification of the Rust implementation (internal audit notes live in 
docs/audits/
)
Potential side-channel issues (Rust big-int / norm computations, etc.)
Parameter selection not hardened for production
Chain-facing deployment wiring is still in progress
Workspace Layout
crates/
  neo-params/      Parameter bundles + Poseidon2 config
  neo-math/        Field/ring utilities, extension field, norms
  spartan2/        Vendored Spartan2 backend
  neo-transcript/  Poseidon2 transcript (Fiat-Shamir)
  neo-ajtai/       Ajtai (lattice) commitments; module-SIS binding
  neo-ccs/         CCS/MCS/ME relations, matrices, arithmetization
  neo-reductions/  Π_CCS / Π_RLC / Π_DEC engines (optimized + paper-exact)
  neo-fold-clean/  Main proving crate: lifecycle API, F′ recursive shell,
                   frontends, decider, terminal-CE relation

docs/
  hypernova-paper/ HyperNova paper text
  architecture/    Design notes (terminal CE, accumulator openings, perf)
  audits/          Internal soundness-audit reports
  plans/           Design and implementation plans

formal/
  superneo-lean/   Main Lean model (source of truth)
  direct-ccs-fprime-lean/ Direct-CCS F′ model
  nightstream-lean/ Published-boundary model (prototype-era, parked)
  twist-shout-lean/ Twist/Shout Lean model
  opening-convergence-lean/ Opening convergence Lean model

Roadmap
Near Term
Compact terminal-CE proof for the folded accumulator (see 
docs/architecture/compact-terminal-ce-proof-requirements.md
)
Twist/Shout memory arguments as projection protocols feeding the main fold lane (see 
docs/plans/
 and 
TODO.md
)
Criterion benchmarks
Medium Term
GPU acceleration exploration
Security audit preparation
Long Term
Production deployment tools
Broader zkVM coverage
See 
TODO.md
 for in-flight work.
References
Neo
: Wilson Nguyen & Srinath Setty, "
Neo: Lattice-based folding scheme for CCS over small fields
" (ePrint 2025/294).
HyperNova
: Abhiram Kothapalli & Srinath Setty, "HyperNova: Recursive arguments for customizable constraint systems". Local text: 
docs/hypernova-paper/
.
Spartan2
: Srinath Setty, "Spartan: Efficient and general-purpose zkSNARKs without trusted setup" (CRYPTO 2020). Vendored in 
crates/spartan2
.
Plonky3
: Goldilocks field and Poseidon2 primitives used by Nightstream.
Acknowledgements
The earlier RV32IM prototype frontend drew on the Jolt zkVM's instruction lowering and lookup-table structure. Thanks to the Jolt team for releasing their work as open source.
Contributing
Add tests
 for behavioural changes
Run formatting
: 
cargo fmt --all
 and 
cargo clippy
 before pushing
Update documentation
 for API changes
DCO sign-off
 is required on every commit (see 
CLAUDE.md
 and 
CONTRIBUTING.md
)
Governance & Policies
Code of Conduct
Security Policy
Contributing Guide
Maintainers
License
Licensed under the 
Apache License, Version 2.0
.
About

        Lattice zkVM (post-quantum zkVM)
      
Resources

        Readme

License

     Apache-2.0 license
    
Code of conduct

        Code of conduct
      
Contributing

        Contributing
      
Security policy

        Security policy
      
        Uh oh!

There was an error while loading. 
Please reload this page
.
Activity
Custom properties
Stars
27

        stars
Watchers
1

        watching
Forks
8

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
Lean
78.7%
Rust
21.0%
Other
0.3%
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
