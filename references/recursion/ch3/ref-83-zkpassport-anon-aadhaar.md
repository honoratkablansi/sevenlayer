---
ref_id: 83
chapters: [3]
type: web
source_url: https://docs.zkpassport.id/
fetched: 2026-06-13
fetched_with: stealthy
citation: 'zkPassport and Anon-Aadhaar style document-proof systems documentation'
---

# zkPassport and Anon-Aadhaar style document-proof systems documentation

Introduction | ZKPassport Docs
Skip to main content
ZKPassport
Documentation
GitHub
Introduction
Getting Started
Examples
API Reference
FAQ
Changelog
Limitations
Introduction
On this page
Introduction
Privacy-preserving identity verification using passports and ID cards.
Overview
​
ZKPassport enables privacy-preserving identity verification using passports and ID cards. It allows you to request and verify specific identity attributes — such as age, nationality, or personhood — without exposing any unnecessary personal information. Proofs are generated on the user's phone and reveal only what you asked for, and nothing else.
Key Features
​
Privacy-first identity verification with zero-knowledge proofs
Selective disclosure of identity attributes
Support for passports, national IDs, and residence permits
A drop-in QR verification card (
@zkpassport/ui
) for React and vanilla JS
Optional no-code configuration through the 
ZKPassport Dashboard
Sample Use Cases
​
Age verification
Nationality verification
Identity attribute disclosure
Proof of personhood and KYC
Two ways to integrate
​
There are two ways to define what you ask users to prove. Both produce the same verification flow and the same results — they differ only in 
where the request is defined
.
Self-served
Dashboard
Setup
None — install the SDK and go
Register your domain at 
dashboard.zkpassport.id
Query definition
Built in code: 
.gte("age", 18).disclose("nationality")…
Defined in the dashboard, referenced by id: 
.policy("pol_xyz")
Branding
 (name & logo)
Passed to 
request()
 in code
Managed in the dashboard
Changing the request
Edit and redeploy your code
Edit the policy in the dashboard — no redeploy
Proof storage
You handle it yourself
Auditable proof storage in the dashboard
Best for
Keeping everything in code; queries that vary at runtime
Centralized config, auditable records, reuse across apps
Pick self-served
 if you want to get started immediately, keep everything in code, or build queries dynamically. Start with 
Basic Usage
.
Pick the dashboard
 if you'd rather manage branding and the request in one place, get auditable proof storage, and reuse it across apps without redeploying. See 
Dashboard & Policies
.
You don't have to choose up front — the same component and SDK support both, so you can start self-served and adopt policies later.
Check out the 
Quick Start Guide
 to begin integrating ZKPassport into your application.
Edit this page
Next
Quick Start
Overview
Key Features
Sample Use Cases
Two ways to integrate
Docs
Introduction
Quick Start
Basic Usage
FAQ
Links
GitHub
Website
X
Copyright © 2026 ZKPassport. Built with Docusaurus.
