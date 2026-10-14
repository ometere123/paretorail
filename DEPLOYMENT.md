# ParetoRail StudioNet deployment evidence

This is the final corrected deployment record for the contract-only ParetoRail repository. Earlier deployments remain historical in [docs/HISTORY.md](docs/HISTORY.md) and `artifacts/studionet_proof_historical_06ed.json`; they are not evidence for the final source below.

## Environment and source

- Network: stable `studionet`
- Chain ID: `61999` / `0xF22F`
- RPC: `https://studio.genlayer.com/api`
- Explorer: `https://explorer-studio.genlayer.com`
- Repository-local CLI: `genlayer@0.39.1`
- GenVM target: `v0.2.12`
- Final deployed contract source commit: `296eb2d77f2489379aa1f5cdc8c208b6b0f6f539`
- ParetoRail source: `26,993` bytes, SHA-256 `fcda440704141cfca09fdf7db0bb0d29d538dc5aff9081ae0242adf20172247e`
- Consumer source: `1,210` bytes, SHA-256 `2044110f4e6c20ade3335eabaf1765be71738440713ac6f81b6773fe4dc55c7c`
- The stable network guard and RPC chain-ID guard returned `61999` before deployment. No preview RPC or chain `61997` was used.

## Final ParetoRail

| item | value |
|---|---|
| address | `0x7a785f8790c44A470898D24772773E1A2713b15D` |
| deployment transaction | `0x6c713238330a8252bd2858cc2c28863ef66c983e617abe81b5279c77f6c75a26` |
| receipt | `FINALIZED / MAJORITY_AGREE / SUCCESS` |
| deployed source commit | `296eb2d77f2489379aa1f5cdc8c208b6b0f6f539` |
| source bytes | `26,993` |
| source SHA-256 | `fcda440704141cfca09fdf7db0bb0d29d538dc5aff9081ae0242adf20172247e` |
| source parity | `gen_getContractCode` returned exactly 26,993 bytes with the same SHA-256 |

## Final AmendedActionGate

| item | value |
|---|---|
| address | `0x522984057CA9181417f8E97023EA6a02f9AA5121` |
| deployment transaction | `0x4e3d1ee0164f2419a17838ee615191575c7807f07a73203bd706d0446d4a2a01` |
| receipt | `FINALIZED / MAJORITY_AGREE / SUCCESS` |
| deployed source commit | `296eb2d77f2489379aa1f5cdc8c208b6b0f6f539` |
| source bytes | `1,210` |
| source SHA-256 | `2044110f4e6c20ade3335eabaf1765be71738440713ac6f81b6773fe4dc55c7c` |
| source parity | `gen_getContractCode` returned exactly 1,210 bytes with the same SHA-256 |
| bound ParetoRail | `0x7a785f8790c44A470898D24772773E1A2713b15D` |
| bound proposal | `5` |
| bound adopted head | `970ff648c7f9096b8acb5fb8ae3f900b85536768ab6de4899c9fede4b557ee46` |

The finalized Consumer deployment was submitted with the final ParetoRail address, proposal `5`, and the adopted head above as constructor arguments. The retrieved Consumer bytes match the committed `contracts/consumer_example.py` exactly. The Consumer is a one-shot authorization example and does not hold funds.

## Final live lifecycle

All writes below were performed on the final ParetoRail unless marked Consumer. Each cited transaction was checked at `FINALIZED`; successful writes also had `MAJORITY_AGREE` and leader execution `SUCCESS`. Rejected/blocked operations are explicitly labelled and are not counted as successful state transitions.

### Agreement creation and sealing

Public wallets used:

- Buyer/creator: `0x951e6B75530774fF82321a5ae54e14F778F0C855`
- Supplier: `0xB845a69860ba4CDf19CfDC5AfbAF2e20b6bE86b0`
- Referrer: `0xac3AC69dC0Bde389256dD6748C75817ead9286D9`

- `create_agreement` finalized in `0x817580c64f9c7e0e1414c6de705eb9e014615c461c9116e4d16584901beed252`.
- Unauthorized `add_party` by the Referrer finalized with leader execution `ERROR` in `0x76ac9ef14ff1e979e7aee907395f9328616aa7a512e436d4d6a6059256fa8452`; the roster did not change.
- Creator added Supplier in `0xb970c405e8ee231318f874411c52ec0efaa0deaad627e62e61333335345c33bd` and Referrer in `0xc905565eb3fb7c284843251e7f70b7264dab8419cfd72d9d0dc95a3eedddd603`.
- Buyer, Supplier and Referrer attestations finalized in `0x2978dbd2c7f20e408e71a5050fd2bde966e7051806ab05c1dc9072abdad65411`, `0x0a08ee9858236f8af3caed8f145fd9d1a722f50f421c5c80c168aff82a7d427d`, and `0x66d620347fa4761df78d84c9e980f7622218def723443e68c84b2cfc35eaae93`.
- `seal_agreement` finalized in `0x7855820f2cc2165c5c790ad5aa94808b6da9daef26e566ff12a9042fcf70e61d`.
- Sealed readback: genesis `0eb4e805cfe0f17987d26f32fe4dbe2f80d4fff784088244927ef5c2e1ecce34`, version `1`, head `2b1c4fb351be47091ee8975cb185129a9160e95c1ef4e67a5463d97a0de6dec3`, quorum `2`, roster size `3`, and all parties attested.

### Terminal-proposal recovery under one unchanged head

The former design could permanently lock a two-party agreement after both parties spent their one lifetime-per-head slot on cancelled proposals. The final design stores one active pending proposal ID per party. Cancellation clears only the proposer’s exact active ID; a `U` proposal is terminal and never occupies a slot; adoption clears active IDs for the new head. No write scans proposal history.

- A neutral candidate was rejected by validator disagreement in `0x15ec2b4d7b5a05546492e5ef65d4699abbc0a08c28f974f89cd3972f19a8d4d7`; no proposal was persisted.
- Buyer created proposal `1` (`NNN`) in `0x5a750883e04ffcf5e01e527dcfa772b6491bd3b7d7033a4ceb46f39df046ddc1`, then cancelled it in `0x8549b99249ccbea88fb6c36d99cf1aeafbbde9a8423a496a9f046b7eac85f876`.
- Supplier created proposal `2` (`NNN`) in `0x6c42e6709dc2ba00b385048c7e56885d4d09e650856a256e01aa011b0389170b`, then cancelled it in `0x08aff0e95b116b6fb37a441341df93b01fbd494974665f454c669c507dc7a22c`.
- Without any head change, Buyer then created proposal `3` in `0x16d5cb9735e46543e2b5f08cd4c00c744d618c014f96922ec19436039f27c950` and Supplier created proposal `4` in `0x556b2f45d63a7b99e6ab6b9ace650dd7e6cbf9f29326797487b0c91c09d0c335`. Readback showed proposal IDs `[1,2,3,4]` and the original version/head unchanged. This is the required live recovery proof.
- Proposal `4` approvals finalized in `0xf5564dae2d268bd4664b1a1d6b4059511fa0b069b19e44c237bc82c17a8c5fe7` and `0xd89378eb8c99c5169b91f379ab502aa5f7b1e686d34f4258af7df1ec028ae00d`; finalization succeeded in `0x79151362ebf0bf4c81da90f42bf4993b485514d0d91bb6d7891e0e7fb17eccb2`, advancing to version `2`, head `13bf4307ea5512427e5770b72284f757763e9fe59fb5ef2ba5375b797e02be53`.
- Approval of old-head proposal `3` in `0xbfebc1a55adee5fd5436d2f8f04261586bfa714dbfcf49da0b330e1ee5b0a7a1` finalized with leader execution `ERROR / STALE_PROPOSAL`; approvals and head remained unchanged.

### Harmed-party consent and adoption

- Buyer proposed a referral reduction (10% to 5%) in `0x562f171674faf0ef062ae6d67321c01c1dc38e370e23d8378957f5f382170fad`. Readback was vector `NNW`, `impacted_mask=4`, proposal `5`, base version `2`, and base head `13bf4307ea5512427e5770b72284f757763e9fe59fb5ef2ba5375b797e02be53`.
- Buyer and Supplier approvals finalized in `0xdbe4039e4e5afae0a59b2162164d4c082e0f216de7707d9545cae330ac27c` and `0xc2ebcd296afeec32a447a0365cc4dfaebf6a6674bbb6738915b529cc5cff2dd7`. Readback was `approvals_mask=3`, `impacted_mask=4`, `can_finalize=false`.
- Referrer approval finalized in `0xc242df147129542d4b0bf8b0da17b23c66bfd47c16566b0fe5a72d89cafb22be`. Readback became `approvals_mask=7` and `can_finalize=true`.
- Finalization succeeded in `0x09086816f798cc4e462169710e7f850da5f7aa1b3dca35327edcb86c435ce7a0`. Readback: version `3`, current terms `Buyer pays 50 GEN. Supplier delivers within five days. Referrer receives five percent.`, and head `970ff648c7f9096b8acb5fb8ae3f900b85536768ab6de4899c9fede4b557ee46`.
- A vague candidate (`The parties will adjust compensation reasonably when appropriate.`) returned live vector `WWW` and was cancelled in `0xa28b9f9c95461c5fff8dccfd5a10b77be021be8f0489c132feea268f006f71b6`. The official Direct Mode suite separately proves a blocked `U` proposal is terminal and recoverable; the live model result is recorded as observed, not forced.

### Bound Consumer one-shot proof

- `was_performed()` on `0x522984057CA9181417f8E97023EA6a02f9AA5121` initially read `false`.
- `perform()` finalized successfully in `0x66315c086eb4126785412ace1d91ec7a9cfab2e3b342ee3ea443bfe67045e93e`; readback was `true`.
- A second `perform()` finalized in `0xe7c1072219051b0e3bb36901e37dbe725210817d2471c1e046dcc7485108e638` with `MAJORITY_AGREE` and execution `ERROR / ALREADY_PERFORMED`; readback remained `true`.

## Limits

The active-slot change eliminates permanent terminal-proposal lockout without granting an administrator or changing the consent rule. It intentionally permits a proposer to cancel and later submit again, so repeated cancellations can grow append-only history and consume transactions. History is bounded per read (`get_proposal_ids_page` limit at most 25), and no state-changing path scans arbitrary proposal history. A blocked or ambiguous proposal is not adoptable; because it does not occupy the active slot, a participant can submit a replacement against the same head. The semantic vector is consensus-backed but remains model-mediated, not formal legal proof. Wallet attestation is not legal identity. The Consumer is noncustodial and only gates one exact adopted head.
