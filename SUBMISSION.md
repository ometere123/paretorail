# ParetoRail submission evidence

ParetoRail is a contract-only GenLayer primitive for consent-safe amendments to multi-party natural-language agreements. Consensus is used only for a bounded per-party semantic impact vector; deterministic contract logic enforces exact text/head binding, quorum, harmed-party consent, replay protection, stale-head rejection and hash-linked history. Ordinary deterministic code cannot reliably classify the material effect of a free-form amendment on each party, while consensus alone must not decide votes, thresholds, identity or adoption.

## Current verified target

- Network: stable StudioNet `studionet`, chain `61999` (`0xF22F`)
- RPC: `https://studio.genlayer.com/api`
- Repository-local CLI: `genlayer@0.39.1`
- Corrected ParetoRail: `0x45df5A40bf702306bd9A30Ae5Bec1847C2e6efE1`
- ParetoRail deployment transaction: `0xec1809fb315effc9b7a37212fe508a2f005a0a16479e42bcfd6efb455f9f270d`
- ParetoRail deployment outcome: `FINALIZED / MAJORITY_AGREE / SUCCESS`
- Deployed ParetoRail source commit: `83a2dbb53e247e54aa73f3224c174dcf6b1625f5`
- ParetoRail source: `26,200` bytes, SHA-256 `f96cd5dc10d5ddbdfad3d573b50eb2533cda8d82c88695a47d6480b2199f0a32`
- ParetoRail source parity: exact `gen_getContractCode` byte and SHA-256 match
- Corrected Consumer: `0xAA543bF4395A87A744fc4b5813BA6cc8960C18AE`
- Consumer deployment transaction: `0x3a0948c43ff77efe22d3c57af30254f6b48604b76f28346a49f04fdb12e99a24`
- Consumer deployment outcome: `FINALIZED / MAJORITY_AGREE / SUCCESS`
- Consumer binding: ParetoRail above, proposal `2`, adopted head `416b1751429f20d20e5c3c3edb6c884dd5fd36e5ff287fd51e4f6a643d5c8138`
- Consumer source: `1,210` bytes, SHA-256 `2044110f4e6c20ade3335eabaf1765be71738440713ac6f81b6773fe4dc55c7c`, exact deployed parity
- Source-code CI: [38605324552](https://github.com/ometere123/paretorail/actions/runs/38605324552), green for the deployed source commit

The superseded deployment is historical only and is preserved in [docs/HISTORY.md](docs/HISTORY.md) and `artifacts/studionet_proof_historical_690b6e.json`.

## Test and tool evidence

- Offline mock-runtime tests: **36/36 passed**. These are not Direct Mode or live consensus evidence.
- Official GenLayer Direct Mode tests: **14/14 passed** with pinned GenVM `v0.2.12`.
- Behavioral security mutation suite: **10/10 mutants killed**.
- GenVM lint: **3/3** checks passed for each deployable contract.
- GenVM semantic validation: passed for both deployable contracts.
- Python 3.12 syntax and structural preflight: passed.
- Stable network guard: passed; RPC `eth_chainId` returned `0xf22f`.

## Live state and lifecycle evidence

The corrected deployment has a finalized three-party agreement `1`, with Buyer `0x951e6B75530774fF82321a5ae54e14F778F0C855`, Supplier `0xB845a69860ba4CDf19CfDC5AfbAF2e20b6bE86b0`, and Referrer `0xac3AC69dC0Bde389256dD6748C75817ead9286D9`. All three individually attested the final roster; sealing finalized with genesis `696cf2dfc942eab28678d6a961e0c0b881174d8e72ccf9978333ff3c5849e5b0`.

The live run also proves:

- consensus rejected a buyer-price increase (`0xfaf7657bc4a6a59f9ec154804a2efbd4abab3710f1a4c79ec01bf6277c529904`) and a deadline weakening (`0xa05a222d1370b7db925b6a726b522287cdf01b71976900a8972af9534855b2d7`) without persisting proposals;
- a neutral candidate was accepted as proposal `1`, approved by the relevant parties, and adopted at head `c45f36a5bf2509c699810517caace828e8003e7c3529ff19e78d76b546f5cf8c`;
- a second neutral cosmetic candidate was adopted as proposal `2`, producing final version `3` and head `416b1751429f20d20e5c3c3edb6c884dd5fd36e5ff287fd51e4f6a643d5c8138`;
- a same-party second submission was rejected with `PROPOSAL_QUOTA` (`0x77700b82fecaae07032752511ebd87e5f0c76f977eb6e40922487160943bc16d`), while another party still submitted proposal `3` (`0xc29237a673e44c0fd88437a579fb9cf80b2edd346f26ec06378a596d4911d99`);
- the competing proposal was stale after the head advanced; the finalized approval attempt `0x87cb079aabf866b835843727635baa94dae8211e2b5f0ed396639648398b5bf0` returned `STALE_PROPOSAL` without state mutation;
- the corrected Consumer performed once in `0x6642b5173651e0a019e5705fa292d6b7ae1a24b553bc762c7896a4eb5ee0826c`, read back `true`, and rejected replay in `0xe9b0b4b7c88934e881d3a7e3655694aa1254e67e608d2879030700cb0c3de3d4` with `ALREADY_PERFORMED`.

Full transaction/state detail is in [DEPLOYMENT.md](DEPLOYMENT.md), and machine-readable evidence is in [artifacts/studionet_proof.json](artifacts/studionet_proof.json).

## Trust boundaries and limitations

The impact vector is the consensus-bound decision-bearing output. Leader explanation and witness text are stored with `LEADER_REPORTED_NOT_CERTIFIED` provenance and are not presented as independently agreed facts. The model-mediated comparison is not a formal legal or mathematical proof. Party-wallet attestation is not legal identity verification. The controlled live fixture demonstrates the contract mechanics, not independent market discovery or commercial enforcement. The example consumer authorizes one head-pinned, one-shot action and holds no funds.
