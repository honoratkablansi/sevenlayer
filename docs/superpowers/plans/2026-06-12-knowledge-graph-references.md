# Knowledge Graph + Reference Corpus Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Download all 63 bibliography references of *Proving Nothing* into `references/ch01..ch14` via a rerunnable Scrapling script, then build a committed Graphify knowledge graph over manuscript + references + wiki.

**Architecture:** A hand-curated `references/manifest.json` is the single source of truth (ref id → chapters, type, URL, target file). `scripts/fetch_references.py` consumes it with a two-tier Scrapling fetch (curl_cffi `Fetcher`, then Camoufox `StealthyFetcher` for blocked web pages) and writes status back. Graphify then ingests the corpus (repo-root with excludes if supported, else a staged `corpus/` folder).

**Tech Stack:** Python 3.14 in `C:\sevenlayer\.venv` (`scrapling[fetchers]` 0.4.9, `graphifyy` 0.8.39, pytest), Graphify CLI + `/graphify` skill.

**Spec:** `docs/superpowers/specs/2026-06-12-knowledge-graph-references-design.md`

**Conventions for all tasks:**
- Working directory: `C:\sevenlayer`. Use the venv binaries explicitly: `.venv\Scripts\python.exe`, `.venv\Scripts\pip.exe`.
- Commit after every task with author `Charles Hoskinson <Charles.Hoskinson@gmail.com>` (already set repo-local).
- Bibliography numbering has gaps: ids 34 and 54 do not exist. Ids 47/48 are re-listings of 12/13 (same papers cited again in ch. 14) — they are manifest entries with `"duplicate_of"` set and no download.

---

### Task 1: Reference manifest

**Files:**
- Create: `references/manifest.json`
- Create: `tests/test_manifest.py`

- [ ] **Step 1: Install pytest into the venv**

Run: `.venv\Scripts\pip.exe install pytest`
Expected: `Successfully installed pytest-...`

- [ ] **Step 2: Write the failing manifest test**

Create `tests/test_manifest.py`:

```python
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "references" / "manifest.json"

EXPECTED_IDS = sorted(set(range(1, 66)) - {34, 54})  # bibliography gaps
VALID_TYPES = {"paper", "web", "stub"}


def load():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_every_bibliography_ref_present_exactly_once():
    ids = [e["id"] for e in load()]
    assert sorted(ids) == EXPECTED_IDS
    assert len(ids) == len(set(ids))


def test_entry_shape():
    for e in load():
        assert e["type"] in VALID_TYPES
        assert e["citation"].strip()
        assert e["chapters"] and all(1 <= c <= 14 for c in e["chapters"])
        if e.get("duplicate_of") is None:
            if e["type"] in ("paper", "web"):
                assert e["url"].startswith("http")
            ext = "pdf" if e["type"] == "paper" else "md"
            expected = f"references/ch{e['chapters'][0]:02d}/ref-{e['id']:02d}-{e['slug']}.{ext}"
            assert e["file"] == expected, f"ref {e['id']}: {e['file']} != {expected}"
        else:
            assert e["duplicate_of"] in EXPECTED_IDS
            assert "file" not in e


def test_slugs_are_kebab_case_and_unique():
    entries = [e for e in load() if e.get("duplicate_of") is None]
    slugs = [e["slug"] for e in entries]
    assert len(slugs) == len(set(slugs))
    for s in slugs:
        assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", s), s
```

- [ ] **Step 3: Run test to verify it fails**

Run: `.venv\Scripts\python.exe -m pytest tests/test_manifest.py -v`
Expected: FAIL (manifest.json does not exist)

- [ ] **Step 4: Create `references/manifest.json`**

Exactly this content (curated from `wiki/BIBLIOGRAPHY.md`; URLs resolved: printed ePrint IDs → `eprint.iacr.org/YYYY/NNN.pdf`, printed arXiv IDs → `arxiv.org/pdf/<id>`, classics resolved to known open-access mirrors; `status` starts `"pending"` everywhere — add `"status": "pending"` to every entry below):

```json
[
  {"id": 1, "slug": "clarke-profiles-of-the-future", "citation": "Clarke, Arthur C. Profiles of the Future. Harper & Row, 1962.", "chapters": [1], "type": "stub", "file": "references/ch01/ref-01-clarke-profiles-of-the-future.md"},
  {"id": 2, "slug": "gmr-knowledge-complexity", "citation": "Goldwasser, Micali, Rackoff. The Knowledge Complexity of Interactive Proof Systems. SIAM J. Computing 18(1), 1989.", "chapters": [1], "type": "paper", "url": "https://people.csail.mit.edu/silvio/Selected%20Scientific%20Papers/Proof%20Systems/The_Knowledge_Complexity_Of_Interactive_Proof_Systems.pdf", "file": "references/ch01/ref-02-gmr-knowledge-complexity.pdf"},
  {"id": 3, "slug": "sok-snark-vulnerabilities", "citation": "Chaliasos et al. SoK: What Don't We Know? Understanding Security Vulnerabilities in SNARKs. USENIX Security 2024.", "chapters": [1], "type": "paper", "url": "https://arxiv.org/pdf/2402.15293", "file": "references/ch01/ref-03-sok-snark-vulnerabilities.pdf"},
  {"id": 4, "slug": "kzg-commitments", "citation": "Kate, Zaverucha, Goldberg. Constant-Size Commitments to Polynomials and Their Applications. ASIACRYPT 2010.", "chapters": [2], "type": "paper", "url": "https://cacr.uwaterloo.ca/techreports/2010/cacr2010-10.pdf", "file": "references/ch02/ref-04-kzg-commitments.pdf"},
  {"id": 5, "slug": "mpc-random-beacon", "citation": "Bowe, Gabizon, Miers. Scalable Multi-party Computation for zk-SNARK Parameters in the Random Beacon Model. ePrint 2017/1050.", "chapters": [2], "type": "paper", "url": "https://eprint.iacr.org/2017/1050.pdf", "file": "references/ch02/ref-05-mpc-random-beacon.pdf"},
  {"id": 6, "slug": "groth16", "citation": "Groth, Jens. On the Size of Pairing-Based Non-interactive Arguments. EUROCRYPT 2016. ePrint 2016/260.", "chapters": [2], "type": "paper", "url": "https://eprint.iacr.org/2016/260.pdf", "file": "references/ch02/ref-06-groth16.pdf"},
  {"id": 7, "slug": "plonk", "citation": "Gabizon, Williamson, Ciobotaru. PLONK. ePrint 2019/953.", "chapters": [2], "type": "paper", "url": "https://eprint.iacr.org/2019/953.pdf", "file": "references/ch02/ref-07-plonk.pdf"},
  {"id": 8, "slug": "stark", "citation": "Ben-Sasson et al. Scalable, Transparent, and Post-Quantum Secure Computational Integrity. ePrint 2018/046.", "chapters": [2], "type": "paper", "url": "https://eprint.iacr.org/2018/046.pdf", "file": "references/ch02/ref-08-stark.pdf"},
  {"id": 9, "slug": "bulletproofs", "citation": "Bunz et al. Bulletproofs: Short Proofs for Confidential Transactions and More. IEEE S&P 2018. ePrint 2017/1066.", "chapters": [2], "type": "paper", "url": "https://eprint.iacr.org/2017/1066.pdf", "file": "references/ch02/ref-09-bulletproofs.pdf"},
  {"id": 10, "slug": "sok-powers-of-tau", "citation": "Wang, Cohney, Bonneau. SoK: Trusted Setups for Powers-of-Tau Strings. FC 2025. ePrint 2025/064.", "chapters": [2], "type": "paper", "url": "https://eprint.iacr.org/2025/064.pdf", "file": "references/ch02/ref-10-sok-powers-of-tau.pdf"},
  {"id": 11, "slug": "latticefold-plus", "citation": "Boneh, Chen. LatticeFold+. CRYPTO 2025. ePrint 2025/247.", "chapters": [2], "type": "paper", "url": "https://eprint.iacr.org/2025/247.pdf", "file": "references/ch02/ref-11-latticefold-plus.pdf"},
  {"id": 12, "slug": "underconstrained-circuits", "citation": "Pailoor et al. Automated Detection of Under-Constrained Circuits in Zero-Knowledge Proofs. PLDI 2023. ePrint 2023/512.", "chapters": [3, 4, 5], "type": "paper", "url": "https://eprint.iacr.org/2023/512.pdf", "file": "references/ch03/ref-12-underconstrained-circuits.pdf"},
  {"id": 13, "slug": "practical-security-zk-circuits", "citation": "Wen et al. Practical Security Analysis of Zero-Knowledge Proof Circuits. USENIX Security 2024. ePrint 2023/190.", "chapters": [3, 4, 5], "type": "paper", "url": "https://eprint.iacr.org/2023/190.pdf", "file": "references/ch03/ref-13-practical-security-zk-circuits.pdf"},
  {"id": 14, "slug": "ccs-customizable-constraints", "citation": "Setty, Thaler, Wahby. Customizable Constraint Systems for Succinct Arguments. ePrint 2023/552.", "chapters": [3, 4, 5], "type": "paper", "url": "https://eprint.iacr.org/2023/552.pdf", "file": "references/ch03/ref-14-ccs-customizable-constraints.pdf"},
  {"id": 15, "slug": "lasso", "citation": "Setty, Thaler, Wahby. Unlocking the Lookup Singularity with Lasso. ePrint 2023/1216.", "chapters": [3, 4, 5], "type": "paper", "url": "https://eprint.iacr.org/2023/1216.pdf", "file": "references/ch03/ref-15-lasso.pdf"},
  {"id": 16, "slug": "jolt", "citation": "Arun, Setty, Thaler. Jolt: SNARKs for Virtual Machines via Lookups. ePrint 2023/1217.", "chapters": [3, 4, 5], "type": "paper", "url": "https://eprint.iacr.org/2023/1217.pdf", "file": "references/ch03/ref-16-jolt.pdf"},
  {"id": 17, "slug": "nova", "citation": "Kothapalli, Setty, Tzialla. Nova: Recursive Zero-Knowledge Arguments from Folding Schemes. CRYPTO 2022. ePrint 2021/370.", "chapters": [6], "type": "paper", "url": "https://eprint.iacr.org/2021/370.pdf", "file": "references/ch06/ref-17-nova.pdf"},
  {"id": 18, "slug": "hypernova", "citation": "Kothapalli, Setty. HyperNova. CRYPTO 2024. ePrint 2023/573.", "chapters": [6], "type": "paper", "url": "https://eprint.iacr.org/2023/573.pdf", "file": "references/ch06/ref-18-hypernova.pdf"},
  {"id": 19, "slug": "protostar", "citation": "Bunz, Chen. ProtoStar. ASIACRYPT 2023. ePrint 2023/620.", "chapters": [6], "type": "paper", "url": "https://eprint.iacr.org/2023/620.pdf", "file": "references/ch06/ref-19-protostar.pdf"},
  {"id": 20, "slug": "latticefold", "citation": "Boneh, Chen. LatticeFold. ASIACRYPT 2025. ePrint 2024/257.", "chapters": [6], "type": "paper", "url": "https://eprint.iacr.org/2024/257.pdf", "file": "references/ch06/ref-20-latticefold.pdf"},
  {"id": 21, "slug": "neo", "citation": "Nguyen, Setty. Neo: Lattice-based Folding Scheme for CCS over Small Fields. ePrint 2025/294.", "chapters": [6], "type": "paper", "url": "https://eprint.iacr.org/2025/294.pdf", "file": "references/ch06/ref-21-neo.pdf"},
  {"id": 22, "slug": "frozen-heart", "citation": "Trail of Bits. Frozen Heart: Forgery of Zero Knowledge Proofs. Blog, April 2022.", "chapters": [6], "type": "web", "url": "https://blog.trailofbits.com/2022/04/13/part-1-coordinated-disclosure-of-vulnerabilities-affecting-girault-bulletproofs-and-plonk/", "file": "references/ch06/ref-22-frozen-heart.md"},
  {"id": 23, "slug": "circle-starks", "citation": "Haboeck, Levit, Papini. Circle STARKs. ePrint 2024/278.", "chapters": [6], "type": "paper", "url": "https://eprint.iacr.org/2024/278.pdf", "file": "references/ch06/ref-23-circle-starks.pdf"},
  {"id": 24, "slug": "shor", "citation": "Shor, Peter W. Algorithms for Quantum Computation. FOCS 1994. arXiv quant-ph/9508027.", "chapters": [7], "type": "paper", "url": "https://arxiv.org/pdf/quant-ph/9508027", "file": "references/ch07/ref-24-shor.pdf"},
  {"id": 25, "slug": "nist-fips-203-204-205", "citation": "NIST. FIPS 203, 204, 205. August 2024. (FIPS 203 PDF downloaded; 204 see ref 64; 205 at nvlpubs.nist.gov.)", "chapters": [7], "type": "paper", "url": "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf", "file": "references/ch07/ref-25-nist-fips-203-204-205.pdf"},
  {"id": 26, "slug": "nist-ir-8547", "citation": "NIST. Transition to Post-Quantum Cryptography Standards (IR 8547). November 2024.", "chapters": [7], "type": "paper", "url": "https://nvlpubs.nist.gov/nistpubs/ir/2024/NIST.IR.8547.ipd.pdf", "file": "references/ch07/ref-26-nist-ir-8547.pdf"},
  {"id": 27, "slug": "l2beat-stages", "citation": "L2Beat. Stages Framework for L2 Maturity. Accessed March 2026.", "chapters": [8], "type": "web", "url": "https://l2beat.com/stages", "file": "references/ch08/ref-27-l2beat-stages.md"},
  {"id": 28, "slug": "rollup-pricing-attacks", "citation": "Chaliasos et al. Unaligned Incentives: Pricing Attacks Against Blockchain Rollups. arXiv 2509.17126, 2025.", "chapters": [8], "type": "paper", "url": "https://arxiv.org/pdf/2509.17126", "file": "references/ch08/ref-28-rollup-pricing-attacks.pdf"},
  {"id": 29, "slug": "gentry-fhe", "citation": "Gentry, Craig. Fully Homomorphic Encryption Using Ideal Lattices. STOC 2009.", "chapters": [9], "type": "paper", "url": "https://www.cs.cmu.edu/~odonnell/hits09/gentry-homomorphic-encryption.pdf", "file": "references/ch09/ref-29-gentry-fhe.pdf"},
  {"id": 30, "slug": "kachina", "citation": "Kerber, Kiayias, Kohlweiss. Kachina -- Foundations of Private Smart Contracts. IEEE CSF 2021. ePrint 2020/543.", "chapters": [9], "type": "paper", "url": "https://eprint.iacr.org/2020/543.pdf", "file": "references/ch09/ref-30-kachina.pdf"},
  {"id": 31, "slug": "blockchain-privacy-compliance", "citation": "Buterin et al. Blockchain Privacy and Regulatory Compliance. Blockchain: Research and Applications, 2023. SSRN 4563364.", "chapters": [9], "type": "web", "url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4563364", "file": "references/ch09/ref-31-blockchain-privacy-compliance.md"},
  {"id": 32, "slug": "zkvm-compiler-optimization", "citation": "Gassmann et al. Evaluating Compiler Optimization Impacts on zkVM Performance. arXiv 2508.17518, 2026.", "chapters": [10, 11], "type": "paper", "url": "https://arxiv.org/pdf/2508.17518", "file": "references/ch10/ref-32-zkvm-compiler-optimization.pdf"},
  {"id": 33, "slug": "circ", "citation": "Ozdemir, Brown, Wahby. CirC: Compiler Infrastructure for Proof Systems. IEEE S&P 2022. ePrint 2020/1586.", "chapters": [10, 11], "type": "paper", "url": "https://eprint.iacr.org/2020/1586.pdf", "file": "references/ch10/ref-33-circ.pdf"},
  {"id": 35, "slug": "coda", "citation": "Liu et al. Certifying Zero-Knowledge Circuits with Refinement Types (Coda). IEEE S&P 2024. ePrint 2023/547.", "chapters": [10, 11], "type": "paper", "url": "https://eprint.iacr.org/2023/547.pdf", "file": "references/ch10/ref-35-coda.pdf"},
  {"id": 36, "slug": "sonic", "citation": "Maller, Bowe, Kohlweiss, Meiklejohn. Sonic. CCS 2019. ePrint 2019/099.", "chapters": [10, 11], "type": "paper", "url": "https://eprint.iacr.org/2019/099.pdf", "file": "references/ch10/ref-36-sonic.pdf"},
  {"id": 37, "slug": "updatable-universal-crs", "citation": "Groth, Kohlweiss, Maller, Meiklejohn, Miers. Updatable and Universal Common Reference Strings. CRYPTO 2018. ePrint 2018/280.", "chapters": [10, 11], "type": "paper", "url": "https://eprint.iacr.org/2018/280.pdf", "file": "references/ch10/ref-37-updatable-universal-crs.pdf"},
  {"id": 38, "slug": "snarky-ceremonies", "citation": "Kohlweiss, Maller, Siim, Volkhov. Snarky Ceremonies. ASIACRYPT 2021. ePrint 2021/219.", "chapters": [10, 11], "type": "paper", "url": "https://eprint.iacr.org/2021/219.pdf", "file": "references/ch10/ref-38-snarky-ceremonies.pdf"},
  {"id": 39, "slug": "compact-language-reference", "citation": "Midnight Network. Compact Language Reference. 2025.", "chapters": [12], "type": "web", "url": "https://docs.midnight.network/develop/reference/", "file": "references/ch12/ref-39-compact-language-reference.md"},
  {"id": 40, "slug": "zkir-reference", "citation": "Midnight Network. ZKIR Intermediate Representation Reference. 2025.", "chapters": [12], "type": "web", "url": "https://docs.midnight.network/develop/reference/", "file": "references/ch12/ref-40-zkir-reference.md"},
  {"id": 41, "slug": "midnight-developer-guide", "citation": "Midnight Network. Developer Guide. 2025.", "chapters": [12], "type": "web", "url": "https://docs.midnight.network/", "file": "references/ch12/ref-41-midnight-developer-guide.md"},
  {"id": 42, "slug": "gvr-zkp-market-report", "citation": "Grand View Research. Zero-Knowledge Proof Market Size, Share & Trends Analysis Report. GVR-4-68040-808-5, 2025.", "chapters": [13], "type": "web", "url": "https://www.grandviewresearch.com/industry-analysis/zero-knowledge-proof-market-report", "file": "references/ch13/ref-42-gvr-zkp-market-report.md"},
  {"id": 43, "slug": "castlelabs-zk-privacy", "citation": "CastleLabs. ZK Proofs: Is Privacy Cheap Enough to Be Mainstream? 2025.", "chapters": [13], "type": "web", "url": "https://research.castlelabs.io", "file": "references/ch13/ref-43-castlelabs-zk-privacy.md"},
  {"id": 44, "slug": "ethproofs", "citation": "Ethproofs. ZK Proving Cost Tracker. Ethereum Foundation, 2025.", "chapters": [13], "type": "web", "url": "https://ethproofs.org", "file": "references/ch13/ref-44-ethproofs.md"},
  {"id": 45, "slug": "small-space-cpu-proofs", "citation": "Nair, Thaler, Zhu. Proving CPU Executions in Small Space. ePrint 2025/611.", "chapters": [14], "type": "paper", "url": "https://eprint.iacr.org/2025/611.pdf", "file": "references/ch14/ref-45-small-space-cpu-proofs.pdf"},
  {"id": 46, "slug": "zk-memory-algebraic-proofs", "citation": "Ozdemir, Laufer, Boneh. Volatile and Persistent Memory for zkSNARKs via Algebraic Interactive Proofs. IEEE S&P 2025. ePrint 2024/979.", "chapters": [14], "type": "paper", "url": "https://eprint.iacr.org/2024/979.pdf", "file": "references/ch14/ref-46-zk-memory-algebraic-proofs.pdf"},
  {"id": 47, "slug": "underconstrained-circuits-ch14", "citation": "Pailoor et al. Automated Detection of Under-Constrained Circuits. PLDI 2023. ePrint 2023/512. (Same paper as ref 12.)", "chapters": [14], "type": "paper", "duplicate_of": 12},
  {"id": 48, "slug": "practical-security-zk-circuits-ch14", "citation": "Wen et al. Practical Security Analysis of Zero-Knowledge Proof Circuits. USENIX Security 2024. ePrint 2023/190. (Same paper as ref 13.)", "chapters": [14], "type": "paper", "duplicate_of": 13},
  {"id": 49, "slug": "nightstream", "citation": "LFDT-Nightstream. Nightstream: Lattice-Based Folding Implementation. GitHub, 2025.", "chapters": [6], "type": "web", "url": "https://github.com/LFDT-Nightstream/Nightstream", "file": "references/ch06/ref-49-nightstream.md"},
  {"id": 50, "slug": "extended-tower-nfs", "citation": "Kim, Barbulescu. Extended Tower Number Field Sieve. CRYPTO 2016. ePrint 2015/1027.", "chapters": [10, 11], "type": "paper", "url": "https://eprint.iacr.org/2015/1027.pdf", "file": "references/ch10/ref-50-extended-tower-nfs.pdf"},
  {"id": 51, "slug": "pairing-efficiency-curves", "citation": "Guillevic, Aurore. Comparing the Pairing Efficiency over Composite-Order and Prime-Order Elliptic Curves. ACNS 2013. ePrint 2013/218.", "chapters": [10, 11], "type": "paper", "url": "https://eprint.iacr.org/2013/218.pdf", "file": "references/ch10/ref-51-pairing-efficiency-curves.pdf"},
  {"id": 52, "slug": "sp1-hypercube", "citation": "Succinct Labs. SP1 Hypercube: Proving Ethereum in Real-Time. Blog, May 2025.", "chapters": [10, 11], "type": "web", "url": "https://blog.succinct.xyz/sp1-hypercube/", "file": "references/ch10/ref-52-sp1-hypercube.md"},
  {"id": 53, "slug": "airbender", "citation": "ZKsync. Airbender: GPU-Accelerated RISC-V Proving. June 2025.", "chapters": [10, 11], "type": "web", "url": "https://www.zksync.io/airbender", "file": "references/ch10/ref-53-airbender.md"},
  {"id": 55, "slug": "zkevm-security-foundations", "citation": "Kadianakis, George. Shipping an L1 zkEVM #2: The Security Foundations. Ethereum Foundation Blog, December 2025.", "chapters": [10, 11], "type": "web", "url": "https://blog.ethereum.org/2025/12/18/zkevm-security-foundations", "file": "references/ch10/ref-55-zkevm-security-foundations.md"},
  {"id": 56, "slug": "symphony", "citation": "Chen, Binyi. Symphony: Scalable SNARKs in the Random Oracle Model from Lattice-Based High-Arity Folding. ePrint 2025/1905.", "chapters": [10, 11], "type": "paper", "url": "https://eprint.iacr.org/2025/1905.pdf", "file": "references/ch10/ref-56-symphony.pdf"},
  {"id": 57, "slug": "chorus-one-zk-economics", "citation": "Klich, Rafal (Chorus One). The Economics of ZK-Proving: Market Size and Future Projections. Research report, March 2025. (No public URL.)", "chapters": [13], "type": "stub", "file": "references/ch13/ref-57-chorus-one-zk-economics.md"},
  {"id": 58, "slug": "dtcc-canton-tokenization", "citation": "DTCC. DTCC and Digital Asset Tokenize US Treasuries on Canton Network. Press release, December 2025.", "chapters": [13], "type": "web", "url": "https://www.dtcc.com/digital-assets/tokenization", "file": "references/ch13/ref-58-dtcc-canton-tokenization.md"},
  {"id": 59, "slug": "world-whitepaper", "citation": "Tools for Humanity (World). World Whitepaper. 2024.", "chapters": [13], "type": "web", "url": "https://whitepaper.world.org/", "file": "references/ch13/ref-59-world-whitepaper.md"},
  {"id": 60, "slug": "eidas-2-regulation", "citation": "European Union. Regulation (EU) 2024/1183 -- European Digital Identity Framework (eIDAS 2.0). OJEU, 2024.", "chapters": [13], "type": "paper", "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202401183", "file": "references/ch13/ref-60-eidas-2-regulation.pdf"},
  {"id": 61, "slug": "arguzz", "citation": "Hochrainer, Wustholz, Christakis. Arguzz: Testing zkVMs for Soundness and Completeness Bugs. arXiv 2509.10819, 2025.", "chapters": [14], "type": "paper", "url": "https://arxiv.org/pdf/2509.10819", "file": "references/ch14/ref-61-arguzz.pdf"},
  {"id": 62, "slug": "lattice-functional-commitments", "citation": "Wee, Wu. Lattice-Based Functional Commitments. ASIACRYPT 2023. ePrint 2024/028.", "chapters": [14], "type": "paper", "url": "https://eprint.iacr.org/2024/028.pdf", "file": "references/ch14/ref-62-lattice-functional-commitments.pdf"},
  {"id": 63, "slug": "harvest-now-decrypt-later", "citation": "Mascelli, Rodden. Harvest Now Decrypt Later. FEDS 2025-093, Federal Reserve Board, 2025.", "chapters": [14], "type": "paper", "url": "https://www.federalreserve.gov/econres/feds/files/2025093pap.pdf", "file": "references/ch14/ref-63-harvest-now-decrypt-later.pdf"},
  {"id": 64, "slug": "fips-204", "citation": "NIST. Module-Lattice-Based Digital Signature Standard (FIPS 204). August 2024.", "chapters": [14], "type": "paper", "url": "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf", "file": "references/ch14/ref-64-fips-204.pdf"},
  {"id": 65, "slug": "greyhound", "citation": "Nguyen, Seiler. Greyhound: Fast Polynomial Commitments from Lattices. CRYPTO 2024. ePrint 2024/1293.", "chapters": [14], "type": "paper", "url": "https://eprint.iacr.org/2024/1293.pdf", "file": "references/ch14/ref-65-greyhound.pdf"}
]
```

(Reminder: insert `"status": "pending"` into every object before saving — the test does not check it but the fetch script requires it.)

- [ ] **Step 5: Run test to verify it passes**

Run: `.venv\Scripts\python.exe -m pytest tests/test_manifest.py -v`
Expected: 3 passed

- [ ] **Step 6: Cross-check against the bibliography by eye**

Open `wiki/BIBLIOGRAPHY.md` next to the manifest and confirm: 63 entries, every printed ePrint/arXiv/URL matches, chapter grouping matches the section headers. Fix discrepancies, re-run the test.

- [ ] **Step 7: Commit**

```bash
git add references/manifest.json tests/test_manifest.py
git commit -m "Add curated reference manifest for all 63 bibliography entries"
```

---

### Task 2: Fetch script — pure helpers (TDD)

**Files:**
- Create: `scripts/fetch_references.py`
- Create: `tests/test_fetch_references.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_fetch_references.py`:

```python
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from fetch_references import is_pdf, stub_markdown, web_markdown

ENTRY = {
    "id": 57,
    "slug": "chorus-one-zk-economics",
    "citation": "Klich, Rafal (Chorus One). The Economics of ZK-Proving. March 2025.",
    "chapters": [13],
    "type": "stub",
    "file": "references/ch13/ref-57-chorus-one-zk-economics.md",
    "status": "pending",
}

WEB_ENTRY = {
    "id": 27,
    "slug": "l2beat-stages",
    "citation": "L2Beat. Stages Framework for L2 Maturity.",
    "chapters": [8],
    "type": "web",
    "url": "https://l2beat.com/stages",
    "file": "references/ch08/ref-27-l2beat-stages.md",
    "status": "pending",
}


def test_is_pdf():
    assert is_pdf(b"%PDF-1.7 rest of file")
    assert not is_pdf(b"<!DOCTYPE html>")
    assert not is_pdf(b"")


def test_stub_markdown_carries_citation_and_id():
    md = stub_markdown(ENTRY)
    assert "ref_id: 57" in md
    assert "Klich" in md
    assert "print-only or paywalled" in md


def test_web_markdown_frontmatter():
    md = web_markdown(WEB_ENTRY, "Extracted page text.", "fetcher", "2026-06-12")
    head, body = md.split("---\n", 2)[1:]
    assert "ref_id: 27" in head
    assert "source_url: https://l2beat.com/stages" in head
    assert "fetched: 2026-06-12" in head
    assert "fetched_with: fetcher" in head
    assert "Extracted page text." in body
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv\Scripts\python.exe -m pytest tests/test_fetch_references.py -v`
Expected: FAIL (`ModuleNotFoundError: fetch_references`)

- [ ] **Step 3: Write the helpers**

Create `scripts/fetch_references.py`:

```python
"""Download the book's references per chapter, driven by references/manifest.json.

Usage (from repo root, venv active):
    python scripts/fetch_references.py [--dry-run] [--force] [--only 6,17,42]
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO / "references" / "manifest.json"


def load_manifest() -> list[dict]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def save_manifest(entries: list[dict]) -> None:
    MANIFEST_PATH.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def is_pdf(data: bytes) -> bool:
    return data[:5] == b"%PDF-"


def stub_markdown(entry: dict) -> str:
    chapters = ", ".join(str(c) for c in entry["chapters"])
    return (
        "---\n"
        f"ref_id: {entry['id']}\n"
        f"chapters: [{chapters}]\n"
        "type: stub\n"
        "---\n\n"
        f"# Reference {entry['id']}: {entry['slug']}\n\n"
        f"{entry['citation']}\n\n"
        "This source is print-only or paywalled; no electronic copy is stored. "
        "This stub exists so the reference appears as a node in the knowledge graph.\n"
    )


def web_markdown(entry: dict, text: str, fetched_with: str, date: str) -> str:
    chapters = ", ".join(str(c) for c in entry["chapters"])
    return (
        "---\n"
        f"ref_id: {entry['id']}\n"
        f"chapters: [{chapters}]\n"
        "type: web\n"
        f"source_url: {entry['url']}\n"
        f"fetched: {date}\n"
        f"fetched_with: {fetched_with}\n"
        f"citation: '{entry['citation'].replace(chr(39), chr(39) * 2)}'\n"
        "---\n\n"
        f"# {entry['citation']}\n\n"
        f"{text}\n"
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv\Scripts\python.exe -m pytest tests/test_fetch_references.py -v`
Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/fetch_references.py tests/test_fetch_references.py
git commit -m "Add fetch_references pure helpers with tests"
```

---

### Task 3: Fetch script — network tier + CLI

**Files:**
- Modify: `scripts/fetch_references.py` (append)

- [ ] **Step 1: Verify the Scrapling 0.4.9 API surface before coding**

Run each and read the output (adjust the code in Step 2 if names differ):

```bash
.venv\Scripts\python.exe -c "from scrapling.fetchers import Fetcher; import inspect; print(inspect.signature(Fetcher.get))"
.venv\Scripts\python.exe -c "from scrapling.fetchers import StealthyFetcher; import inspect; print(inspect.signature(StealthyFetcher.fetch))"
.venv\Scripts\python.exe -c "from scrapling.engines.toolbelt.custom import Response; print([a for a in dir(Response) if not a.startswith('_')])"
```

Confirm: `Fetcher.get(url, ...)` exists, responses expose `.status` and raw bytes (`.body` or equivalent), and selector text extraction (`.get_all_text()`) exists. If an attribute is named differently, use the actual name consistently below.

- [ ] **Step 2: Append the network functions and CLI to `scripts/fetch_references.py`**

```python
def fetch_paper(url: str) -> tuple[bytes | None, str]:
    """Two attempts with curl_cffi impersonation. Returns (pdf_bytes, fetcher_name)."""
    from scrapling.fetchers import Fetcher

    for impersonate in ("chrome", "firefox"):
        try:
            page = Fetcher.get(url, impersonate=impersonate, timeout=90)
        except Exception as exc:  # noqa: BLE001 - report and try next tier
            print(f"    {impersonate}: {exc}")
            continue
        if page.status == 200 and is_pdf(page.body):
            return page.body, f"fetcher-{impersonate}"
        print(f"    {impersonate}: status={page.status}, pdf={is_pdf(page.body)}")
    return None, ""


def fetch_web_text(url: str) -> tuple[str | None, str]:
    """Fetcher first; StealthyFetcher (Camoufox) for bot-blocked/JS pages."""
    from scrapling.fetchers import Fetcher, StealthyFetcher

    try:
        page = Fetcher.get(url, impersonate="chrome", timeout=90)
        if page.status == 200:
            text = page.get_all_text(ignore_tags=("script", "style")).strip()
            if len(text) > 200:  # tiny bodies = JS shell or block page
                return text, "fetcher"
    except Exception as exc:  # noqa: BLE001
        print(f"    fetcher: {exc}")
    try:
        page = StealthyFetcher.fetch(url, headless=True, network_idle=True, timeout=120000)
        if page.status == 200:
            return page.get_all_text(ignore_tags=("script", "style")).strip(), "stealthy"
    except Exception as exc:  # noqa: BLE001
        print(f"    stealthy: {exc}")
    return None, ""


def process(entry: dict, force: bool, dry_run: bool) -> str:
    """Returns the new status for the entry."""
    if entry.get("duplicate_of") is not None:
        target = next(e for e in load_manifest() if e["id"] == entry["duplicate_of"])
        return "ok" if (REPO / target["file"]).exists() else "pending"

    out = REPO / entry["file"]
    if out.exists() and not force:
        return entry["status"] if entry["status"] not in ("pending", "failed") else "ok"
    if dry_run:
        print(f"  would fetch [{entry['type']}] {entry.get('url', '(stub)')} -> {entry['file']}")
        return entry["status"]

    out.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()

    if entry["type"] == "stub":
        out.write_text(stub_markdown(entry), encoding="utf-8")
        return "stub"
    if entry["type"] == "paper":
        data, how = fetch_paper(entry["url"])
        if data is None:
            return "failed"
        out.write_bytes(data)
        return "ok" if how == "fetcher-chrome" else "ok-stealth"
    # web
    text, how = fetch_web_text(entry["url"])
    if text is None:
        return "failed"
    out.write_text(web_markdown(entry, text, how, today), encoding="utf-8")
    return "ok" if how == "fetcher" else "ok-stealth"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true", help="re-download existing files")
    ap.add_argument("--only", help="comma-separated ref ids")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    entries = load_manifest()
    only = {int(x) for x in args.only.split(",")} if args.only else None
    for entry in entries:
        if only and entry["id"] not in only:
            continue
        print(f"[{entry['id']:02d}] {entry['slug']} ({entry['type']})")
        entry["status"] = process(entry, args.force, args.dry_run)
        print(f"  -> {entry['status']}")
        if not args.dry_run:
            save_manifest(entries)

    bad = [e["id"] for e in entries if e["status"] in ("pending", "failed")]
    print(f"\n{len(entries) - len(bad)}/{len(entries)} resolved; unresolved: {bad or 'none'}")
    return 1 if (bad and not args.dry_run and not only) else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Verify with dry run**

Run: `.venv\Scripts\python.exe scripts/fetch_references.py --dry-run`
Expected: 63 lines of `would fetch ...` / duplicate handling, exit 0, no files created, manifest unchanged (`git diff --stat references/manifest.json` empty).

- [ ] **Step 4: Run existing tests still pass**

Run: `.venv\Scripts\python.exe -m pytest tests/ -v`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
git add scripts/fetch_references.py
git commit -m "Add two-tier Scrapling fetch pipeline and CLI"
```

---

### Task 4: Download the corpus

**Files:**
- Create (downloads): `references/ch01/..ch14/*` (~63 files)
- Modify: `references/manifest.json` (statuses)

- [ ] **Step 1: Smoke-test one easy paper and one web page**

Run: `.venv\Scripts\python.exe scripts/fetch_references.py --only 6,49`
Expected: `references/ch02/ref-06-groth16.pdf` exists and starts with `%PDF`; `references/ch06/ref-49-nightstream.md` exists with front-matter. If the Scrapling API misbehaves here, fix `fetch_paper`/`fetch_web_text` now (this is the integration checkpoint).

- [ ] **Step 2: Full run**

Run: `.venv\Scripts\python.exe scripts/fetch_references.py`
Expected: several minutes (Camoufox launches for JS-heavy pages: l2beat, ethproofs, zksync, SSRN, Grand View Research). Final line reports resolved count and lists failures.

- [ ] **Step 3: Triage failures**

For each `failed` entry:
- Wrong/dead URL (likely candidates: ref 2 MIT-hosted GMR PDF, ref 60 eur-lex PDF format, ref 43 castlelabs): find the correct open-access URL, update `url` in the manifest, rerun `--only <id> --force`.
- Hard bot-wall after both tiers (likely candidate: ref 31 SSRN, ref 42 Grand View Research): change `"type"` to `"stub"`, change `file` extension to `.md`, keep the original URL in the citation text, rerun `--only <id>`.

Repeat until the script exits 0.

- [ ] **Step 4: Verify completeness, integrity, idempotency**

Run from bash (note forward slashes — this is a heredoc):

```bash
.venv/Scripts/python.exe - <<'EOF'
import json, pathlib
repo = pathlib.Path(".")
entries = json.loads((repo / "references/manifest.json").read_text(encoding="utf-8"))
assert all(e["status"] in ("ok", "ok-stealth", "stub") for e in entries), [e["id"] for e in entries if e["status"] not in ("ok", "ok-stealth", "stub")]
for e in entries:
    if e.get("duplicate_of") is None:
        p = repo / e["file"]
        assert p.exists(), e["file"]
        if e["type"] == "paper":
            assert p.read_bytes()[:5] == b"%PDF-", e["file"]
print("corpus complete:", len(entries), "refs")
EOF
```

Then rerun `.venv\Scripts\python.exe scripts/fetch_references.py` — Expected: every entry skipped, exit 0 (idempotent).

- [ ] **Step 5: Run the full test suite**

Run: `.venv\Scripts\python.exe -m pytest tests/ -v`
Expected: all pass (manifest test still valid after triage edits — if a type changed to stub, the `file` extension test enforces `.md`).

- [ ] **Step 6: Commit the corpus**

```bash
git add references/
git commit -m "Download reference corpus: papers, web captures, and stubs for all chapters"
```

---

### Task 5: Build the knowledge graph

**Files:**
- Create: `graphify-out/` (graph.json, HTML, GRAPH_REPORT.md)
- Possibly create: `scripts/stage_corpus.py` (fallback only)

- [ ] **Step 1: Check Graphify's exclude support**

Run: `.venv\Scripts\graphify.exe --help` and `.venv\Scripts\graphify.exe build --help` (or the equivalent top-level command shown by `--help`).
Look for an ignore/exclude flag or config (e.g. `--exclude`, `.graphifyignore`).

- [ ] **Step 2a (preferred — exclude support exists): build on repo root**

Exclude everything that is not corpus: `assets/`, `src/`, `docs/`, `.venv/`, `.claude/`, `*.tex`, `*.lua`, `*.css`, `*.py`, `*.toml`, `*.xml`, `proving-nothing.pdf`, `proving-nothing.epub`, `coverpage.tex`, `wiki/tools/`, `wiki/_meta/` (keep `proving-nothing.md`, `references/`, `wiki/` markdown). Run the full pipeline per the flag syntax `--help` showed, from the repo root with the venv activated (`.venv\Scripts\activate`).

- [ ] **Step 2b (fallback — no exclude support): stage a corpus directory**

Create `scripts/stage_corpus.py`:

```python
"""Assemble corpus/ for graphify: manuscript + references + wiki markdown."""
from __future__ import annotations

import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CORPUS = REPO / "corpus"


def main() -> None:
    if CORPUS.exists():
        shutil.rmtree(CORPUS)
    CORPUS.mkdir()
    shutil.copy2(REPO / "proving-nothing.md", CORPUS / "proving-nothing.md")
    shutil.copytree(REPO / "references", CORPUS / "references",
                    ignore=shutil.ignore_patterns("manifest.json"))
    shutil.copytree(REPO / "wiki", CORPUS / "wiki",
                    ignore=shutil.ignore_patterns("tools", "_meta", ".gitkeep"))
    n = sum(1 for p in CORPUS.rglob("*") if p.is_file())
    print(f"staged {n} files in {CORPUS}")


if __name__ == "__main__":
    main()
```

Run it, add `corpus/` to `.gitignore` (it is a derived artifact), then run the Graphify pipeline on `corpus/` per the `/graphify` skill in `.claude/skills/graphify/SKILL.md` (the skill's detect/extract/cluster steps), with the venv activated so its `pip`/`python` calls hit `.venv`.

- [ ] **Step 3: Inspect the audit report for corpus pollution**

Open `graphify-out/GRAPH_REPORT.md`. Confirm: no nodes from fonts/LaTeX/build scripts; chapter, reference, and wiki-concept nodes present; EXTRACTED edges dominate (INFERRED should not be the majority).
If polluted: switch to the staged-corpus path (Step 2b) and rebuild.

- [ ] **Step 4: Commit graph outputs**

```bash
git add graphify-out/ .gitignore scripts/stage_corpus.py
git commit -m "Build Graphify knowledge graph over manuscript, references, and wiki"
```

(Omit `scripts/stage_corpus.py` from the commit if Step 2a was used.)

---

### Task 6: Verification and wrap-up

**Files:**
- None new (possibly small fixes)

- [ ] **Step 1: Graph sanity queries**

Run (syntax per the `/graphify` skill / CLI help):

```bash
.venv\Scripts\graphify.exe query "Which chapters and references discuss KZG polynomial commitments?"
.venv\Scripts\graphify.exe query "What does the book say about under-constrained circuits?"
.venv\Scripts\graphify.exe path "Nova" "LatticeFold"
```

Expected: KZG answer touches chapters 2/6, ref 4, and `wiki/concepts/kzg.md`; under-constrained answer touches chapters 3-5/14 and refs 12/13; the path query returns a folding-scheme chain. If a query returns nothing, the corpus staging missed files — fix and rebuild before proceeding.

- [ ] **Step 2: Full test suite + fetch idempotency one last time**

```bash
.venv\Scripts\python.exe -m pytest tests/ -v
.venv\Scripts\python.exe scripts/fetch_references.py
```

Expected: tests pass; fetch run downloads nothing, exit 0.

- [ ] **Step 3: Final commit if anything changed**

```bash
git status --short
git add -A && git commit -m "Verify knowledge graph and reference corpus pipeline"
```

(Skip the commit if the tree is clean.)
