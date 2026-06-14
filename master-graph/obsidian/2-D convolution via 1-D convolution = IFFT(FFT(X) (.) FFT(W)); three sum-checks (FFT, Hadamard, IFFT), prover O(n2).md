---
source_file: "references/recursion/ch3/ref-70-zkcnn.pdf"
type: "paper"
community: "Community 114"
location: "§3.2 (Eq 11-12)"
tags:
  - graphify/paper
  - graphify/EXTRACTED
  - community/Community_114
---

# 2-D convolution via 1-D convolution = IFFT(FFT(X) (.) FFT(W)); three sum-checks (FFT, Hadamard, IFFT), prover O(n^2)

## Connections
- [[Conv-layer with ch_in channels IFFT linearity reduces IFFTs to ch_out, sum of Hadamard products via single sum-check]] - `conceptually_related_to` [EXTRACTED]
- [[New sum-check protocol for FFT with O(N) linear prover time (faster than computing the FFT)]] - `assumes` [EXTRACTED]
- [[Zero-knowledge proof of 2-D convolution correctness]] - `defines` [EXTRACTED]

#graphify/paper #graphify/EXTRACTED #community/Community_114