# ParetoRail submission evidence

ParetoRail is a contract-only GenLayer primitive for consent-safe amendments to multi-party natural-language agreements. Consensus is used only for a bounded per-party semantic impact vector; deterministic contract logic enforces exact text/head binding, quorum, harmed-party consent, replay protection, stale-head rejection and hash-linked history. Ordinary deterministic code cannot reliably classify the material effect of a free-form amendment on each party, while consensus alone must not decide votes, thresholds, identity or adoption.

## Current verified target

- Network: stable StudioNet `studionet`, chain `61999` (`0xF22F`)
- RPC: `https://studio.genlayer.com/api`
- Repository-local CLI: `genlayer@0.39.1`
- Final ParetoRail: `0x7a785f8790c44A470898D24772773E1A2713b15D`
- ParetoRail deployment transaction: `0x6c713238330a8252bd2858cc2c28863ef66c983e617abe81b5279c77f6c75a26`
- ParetoRail deployment outcome: `FINALIZED / MAJORITY_AGREE / SUCCESS`
- Deployed ParetoRail source commit: `296eb2d77f2489379aa1f5cdc8c208b6b0f6f539`
- ParetoRail source: `26,993` bytes, SHA-256 `fcda440704141cfca09fdf7db0bb0d29d538dc5aff9081ae0242adf20172247e`
- ParetoRail source parity: exact `gen_getContractCode` byte and SHA-256 match
- Final Consumer: `0x522984057CA9181417f8E97023EA6a02f9AA5121`
- Consumer deployment transaction: `0x4e3d1ee0164f2419a17838ee615191575c7807f07a73203bd706d0446d4a2a01`
- Consumer deployment outcome: `FINALIZED / MAJORITY_AGREE / SUCCESS`
- Consumer binding: ParetoRail above, proposal `5`, adopted head `970ff648c7f9096b8acb5fb8ae3f900b85536768ab6de4899c9fede4b557ee46`
- Consumer source: `1,210` bytes, SHA-256 `2044110f4e6c20ade3335eabaf1765be71738440713ac6f81b6773fe4dc55c7c`, exact deployed parity
- Source verification CI: [run 38626366755](https://github.com/ometere123/paretorail/actions/runs/38626366755), green for source commit `27cfc78359185790d572abac860b7ad2bce6081c`

The prior corrected deployment (`0x45df5A40bf702306bd9A30Ae5Bec1847C2e6efE1`) is historical only and is preserved in [docs/HISTORY.md](docs/HISTORY.md) and [artifacts/studionet_proof_historical_06ed.json](artifacts/studionet_proof_historical_06ed.json).

## Test and tool evidence

- Offline mock-runtime tests: **40/40 passed**. These are not Direct Mode or live consensus evidence.
- Official GenLayer Direct Mode tests: **16/16 passed** with pinned GenVM `v0.2.12`.
- Behavioral security mutation suite: **13/13 mutants killed**.
- GenVM lint: **3/3** checks passed for each deployable contract.
- GenVM semantic validation: passed for both deployable contracts.
- Python 3.12 syntax and structural preflight: passed.
- Stable network guard: passed; RPC `eth_chainId` returned `0xf22f`.

## Live state and lifecycle evidence

The final deployment has a finalized three-party agreement `1`, with Buyer `0x951e6B75530774fF82321a5ae54e14F778F0C855`, Supplier `0xB845a69860ba4CDf19CfDC5AfbAF2e20b6bE86b0`, and Referrer `0xac3AC69dC0Bde389256dD6748C75817ead9286D9`. All three individually attested the final roster. The final readback is sealed, version `3`, with genesis `0eb4e805cfe0f17987d26f32fe4dbe2f80d4fff784088244927ef5c2e1ecce34` and head `970ff648c7f9096b8acb5fb8ae3f900b85536768ab6de4899c9fede4b557ee46`.

The final run proves:

- unauthorized roster mutation was finalized with leader execution `ERROR` in `0x76ac9ef14ff1e979e7aee907395f9328616aa7a512e436d4d6a6059256fa8452`; the roster remained unchanged;
- proposals `1` and `2` were cancelled by their own proposers, then both parties independently submitted proposals `3` and `4` against the unchanged original head (`0x16d5cb9735e46543e2b5f08cd4c00c744d618c014f96922ec19436039f27c950` and `0x556b2f45d63a7b99e6ab6b9ace650dd7e6cbf9f29326797487b0c91c09d0c335`). This is the live recovery of the former all-participants-exhausted deadlock;
- proposal `4` was approved by Supplier and Buyer (`0xf5564dae2d268bd4664b1a1d6b4059511fa0b069b19e44c237bc82c17a8c5fe7`, `0xd89378eb8c99c5169b91f379ab502aa5f7b1e686d34f4258af7df1ec028ae00d`) and adopted in `0x79151362ebf0bf4c81da90f42bf4993b485514d0d91bb6d7891e0e7fb17eccb2`, advancing to version `2` and head `13bf4307ea5512427e5770b72284f757763e9fe59fb5ef2ba5375b797e02be53`;
- an approval against stale proposal `3` finalized with leader execution `ERROR` in `0xbfebc1a55adee5fd5436d2f8f04261586bfa714dbfcf49da0b330e1ee5b0a7a1` and did not mutate state;
- proposal `5` produced the actual live adverse vector `NNW` with `impacted_mask=4`. Buyer and Supplier approvals alone yielded `approvals_mask=3` and `can_finalize=false` (`0xdbe4039e4e5afae0a59b2162164d4c082e0f216de7707d9545cae330ac27c`, `0xc2ebcd296afeec32a447a0365cc4dfaebf6a6674bbb6738915b529cc5cff2dd7`); Referrer then approved in `0xc242df147129542d4b0bf8b0da17b23c66bfd47c16566b0fe5a72d89cafb22be`, giving mask `7` and `can_finalize=true`;
- proposal `5` finalized in `0x09086816f798cc4e462169710e7f850da5f7aa1b3dca35327edcb86c435ce7a0`, adopting the exact reduced-referral text and head above;
- an intentionally vague candidate returned a conservative `WWW` vector and was cancelled in `0xa28b9f9c95461c5fff8dccfd5a10b77be021be8f0489c132feea268f006f71b6`; the official Direct Mode suite separately proves `U` proposals are terminal and recoverable;
- the final Consumer was bound to proposal `5` and the final adopted head. Its one-shot `perform()` finalized successfully in `0x66315c086eb4126785412ace1d91ec7a9cfab2e3b342ee3ea443bfe67045e93e`; `was_performed()` read back `true`. Replay finalized in `0xe7c1072219051b0e3bb36901e37dbe725210817d2471c1e046dcc7485108e638` with execution `ERROR` and `ALREADY_PERFORMED`; state remained `true`.

Full transaction/state detail is in [DEPLOYMENT.md](DEPLOYMENT.md), and machine-readable evidence is in [artifacts/studionet_proof.json](artifacts/studionet_proof.json). All cited live writes were checked for `FINALIZED`; successful transitions additionally require `MAJORITY_AGREE` and leader execution `SUCCESS`.

## Trust boundaries and limitations

The impact vector is the consensus-bound decision-bearing output. Leader explanation and witness text are stored with `LEADER_REPORTED_NOT_CERTIFIED` provenance and are not presented as independently agreed facts. The model-mediated comparison is not a formal legal or mathematical proof. Party-wallet attestation is not legal identity verification. The controlled live fixture demonstrates the contract mechanics, not independent market discovery or commercial enforcement. The active-slot recovery removes permanent terminal-proposal lockout but repeated cancellation can grow immutable history; enumeration is bounded to pages of at most 25 and writes do not scan history. The example consumer authorizes one head-pinned, one-shot action and holds no funds.
