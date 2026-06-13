---
ref_id: 27
chapters: [1]
type: web
source_url: https://docs.succinct.xyz/docs/sp1/introduction
fetched: 2026-06-13
fetched_with: fetcher
citation: 'Succinct, SP1 technical documentation'
---

# Succinct, SP1 technical documentation

Introduction | Succinct Docs
Skip to main content
Succinct Docs
SP1
Prover Network
Overview
Provers
Solutions
OP Succinct
SP1 Helios
GitHub
Search
Overview
Introduction
What is a zkVM?
Usecases
Getting Started
Installation
Quickstart
Hardware Requirements
Recommended Workflow
Migrating from V5 to V6
Writing Programs
Basics
Setup
Compiling Programs
Proof Aggregation
Proving
Basics
Proof Types
Hardware Acceleration
Advanced
Offchain Verification
Optimization & Profiling
Basics
Precompiles
Precompile Specification
Prover Gas
Cycle Tracking
Profiling
Prover Network
Quickstart
Advanced Usage
Reserved Capacity
Migrate to Mainnet
Troubleshooting
FAQ
TEE 2FA
TEE Private Proving
On-Chain Verification
Setup
Contract Addresses
Solidity Verifier
Troubleshooting & CI
Common Issues
Usage in CI
Upgrade Guides
SP1 Proof System
Introduction
Shard Proofs
Main Trace Commitment
LogUp GKR
Zerocheck
Jagged PCS
Dense PCS
Global Memory Argument
Recursion
Security
Security Model
Safe Usage of SP1 Precompiles
Security Policy
Security Advisories
Audit Reports
Bug Bounty
Resources
Explorer (Mainnet)
Explorer (Reserved)
Staking
Overview
Introduction
On this page
Introduction
Documentation for developers that want to use SP1 to build ZK applications
.
SP1 is a zero‑knowledge virtual machine (zkVM) that proves the correct execution of programs compiled for the RISC-V architecture. This means it can run and prove programs written in Rust, C++, C, or any language that compiles to RISC-V.
SP1 V6 introduces Hypercube, a new multilinear proof system that delivers significant performance improvements through advanced polynomial commitment schemes and optimized recursion. See the 
upgrade guide
 for migration details.
SP1 is feature-complete, consistently delivers state-of-the-art performance on industry-standard benchmarks, and has been rigorously audited by top security firms. It's trusted in production by leading teams across blockchains, cryptography, and beyond.
With SP1, developers can write provable programs using ordinary code in familiar languages like Rust. There's no need for custom circuit design or cryptography expertise, just write your logic, compile it, and generate a proof. It’s ZK as intuitive and programmable as traditional computing.
Why Use SP1
​
If you're building with zero-knowledge proofs today, SP1 gives you the fastest path to production, without compromising on performance, flexibility, or developer experience. Here are three reasons why teams are choosing SP1:
Maintainability
. Write ZK programs in standard Rust without custom DSLs or complex circuits. SP1 makes your codebase easier to understand, audit, and evolve over time.
Faster Development
. Skip months of low-level ZK engineering. SP1 drastically shortens timelines, helping you go from idea to mainnet faster.
Performance
. SP1 delivers state-of-the-art proving speed and efficiency, benchmarked and battle-tested in real-world production environments.
Open Source
​
SP1 includes open-source implementations of both the prover and verifier, released under the MIT and Apache 2.0 licenses.
Next
What is a zkVM?
Why Use SP1
Open Source
