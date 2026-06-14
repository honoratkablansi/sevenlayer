---
source_file: "references/recursion/ch3/ref-69-kang-trustless-dnn-inference.pdf"
type: "paper"
community: "Community 76"
location: "title/Abstract"
tags:
  - graphify/paper
  - graphify/EXTRACTED
  - community/Community_76
---

# Scaling up Trustless DNN Inference with Zero-Knowledge Proofs (Kang, Hashimoto, Stoica, Sun, 2022)

## Connections
- [[Evaluation claim ImageNet-scale MobileNet v2 SNARKs up to 79.2% top-5 accuracy; 10x-1000x lower proving time than prior work (Zen, vCNN, pvCNN, zkCNN)]] - `proves` [EXTRACTED]
- [[Groth16  R1CS arithmetization (Groth 2016; Gennaro et al. 2013) older pairing-based SNARK + R1CS used by prior DNN-SNARK work (e.g. Zen)]] - `cites` [EXTRACTED]
- [[Halo 2  UltraPlonk]] - `cites` [EXTRACTED]
- [[MobileNet v2 (Sandler et al. 2018) inverted-residual CNN architecture used as the proved model]] - `cites` [EXTRACTED]
- [[Neural-network arithmetization translating CNN layers (convolution, batchnorm, ReLU, residual, fully-connected) into ZK-SNARK arithmetic-circuit constraints]] - `introduces` [EXTRACTED]
- [[Proof of model provenance committing to hidden weights via a SNARK-friendly hash so a provider can prove it ran a specific committed model]] - `introduces` [INFERRED]
- [[Proof-of-inference first ImageNet-scale ZK-SNARK proof of valid DNN inference (MobileNet v2), 79% top-5 accuracy, verifiable in ~10s]] - `introduces` [EXTRACTED]
- [[Protocol for verifying MLaaS model accuracy with hidden weights, using ZK-SNARKs plus stakingescrow economic incentives]] - `introduces` [EXTRACTED]
- [[Protocol for verifying MLaaS predictions in rounds, with random-contest sampling so a ZK-SNARK is not needed for every prediction]] - `introduces` [EXTRACTED]
- [[Secure ML via MPC  homomorphic encryption  interactive proofs (Ghodsi SafetyNets 2017, Mohassel SecureML 2017, Knott CrypTen 2021, GAZELLE, Delphi) impractical against malicious adversaries o_cb9fbadd]] - `cites` [EXTRACTED]
- [[Sumcheck-based DNN proof systems (zkCNNLiu 2021, vCNNLee 2020, pvCNNWeng 2022, Thaler 2013) custom IPSNARK protocols tailored to convolutions, limited to MNISTCIFAR-10]] - `cites` [EXTRACTED]
- [[Trustless retrieval ZK-SNARK protocol for returning documents matching an ML-encoded predicate (FOIA  legal-discovery use cases)]] - `introduces` [EXTRACTED]
- [[Use of the SNARK-friendly Poseidon hash to commit to hidden inputs andor weights inside the circuit]] - `cites` [EXTRACTED]
- [[Verifiable  trustless DNN inference model consumer verifies that the model provider served correct predictions in an untrusted (MLaaS) setting]] - `introduces` [EXTRACTED]
- [[ZKML (Zero-Knowledge Machine Learning)]] - `conceptually_related_to` [EXTRACTED]
- [[zk-SNARK]] - `assumes` [EXTRACTED]

#graphify/paper #graphify/EXTRACTED #community/Community_76