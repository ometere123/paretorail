# ParetoRail submission evidence

ParetoRail is a contract-only GenLayer primitive for consent-safe amendments to multi-party natural-language agreements. It uses consensus for a bounded per-party semantic impact vector and deterministic contract logic for quorum, harmed-party consent, exact proposal binding, stale-head rejection and hash-linked history. Ordinary deterministic code cannot itself classify the material effect of a free-form amendment on each party; consensus is used only for that bounded semantic relation, not for votes, thresholds, hashes, identity or adoption.

## Verified target

- Network: stable StudioNet `studionet`, chain `61999` (`0xF22F`)
- RPC: `https://studio.genlayer.com/api`
- Repository-local CLI: `genlayer@0.39.1`
- ParetoRail: `0x3cF4773bAC377CeaA3f90b5AE3bC1E317F315411`
- Deployment transaction: `0xf054cc46ea3677d9aa5aa5012f1393fc644bc871beb96252ccd72a4472db13cd`
- Deployment outcome: `FINALIZED / MAJORITY_AGREE / SUCCESS`
- ParetoRail source SHA-256: `f19d28c009259ddf22c289936beb43b7d7c064dcaa83f69e7049ff314580215d`
- Deployed-source parity: exact byte count and SHA-256 match (`23,686` bytes)

The optional `AmendedActionGate` consumer is deployed at `0xd3b91F93ECE55c188D2E8938A37cF35ded583f39`, bound to the ParetoRail address above, proposal `4`, and adopted head `cda68fa595c6064411be0eed3b0a888a5872551c8ac4d9f1418807061e402cdd`. Its source SHA-256 is `2044110f4e6c20ade3335eabaf1765be71738440713ac6f81b6773fe4dc55c7c`; deployed bytes match.

## Tests and tooling

- Offline mock-runtime suite: `33 passed` (`python -m pytest tests/test_offline.py -q`). These are explicitly not Direct Mode or live evidence.
- Official Direct Mode suite: `11 passed` (`py -3.12 -m pytest tests/direct/ -v`).
- GenVM lint: `3/3` checks passed for `contracts/paretorail.py`; `3/3` checks passed for `contracts/consumer_example.py`; `genvm-lint download --version v0.2.12` completed.
- Structural preflight: passed.
- Stable network guard: passed for local CLI `0.39.1`, studionet and RPC; RPC `eth_chainId` returned `0xf22f`.
- Python 3.12 was used for the pinned GenLayer test/lint toolchain. `npm install --no-audit --no-fund` generated the committed lockfile.

## Live lifecycle summary

The final deployment has a finalized three-party agreement with unanimous baseline attestations, a `BWN` amendment that could not finalize at quorum until the harmed Supplier consented, and a subsequent finalized adoption. A semantically equivalent reordered amendment was certified `NNN` and adopted. Old-head finalization returned `STALE_PROPOSAL`. A hidden referral carve-out and an ambiguous/non-convergent attempt finalized without state change (`MAJORITY_DISAGREE`). The bound consumer performed exactly once and rejected replay with `ALREADY_PERFORMED`.

Detailed hashes and state readbacks are in [DEPLOYMENT.md](DEPLOYMENT.md) and the machine-readable [artifacts/studionet_proof.json](artifacts/studionet_proof.json).

## Scope and limitations

ParetoRail does not prove legal fairness, domain ownership, complete discovery of external obligations, or commercial-market adoption. A party wallet is the contract’s identity boundary. Leader explanations are stored as `LEADER_REPORTED_NOT_CERTIFIED`; only the normalized impact vector is consensus-bound. The example consumer gates a one-shot action and does not custody or transfer GEN.
