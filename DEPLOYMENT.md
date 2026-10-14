# ParetoRail StudioNet deployment evidence

This is the current corrected deployment record for the supplied contract-only ParetoRail repository. The superseded deployment and its evidence remain in [docs/HISTORY.md](docs/HISTORY.md) and `artifacts/studionet_proof_historical_690b6e.json`.

## Environment and source

- Network: stable `studionet`
- Chain ID: `61999` / `0xF22F`
- RPC: `https://studio.genlayer.com/api`
- Repository-local CLI: `genlayer@0.39.1`
- GenVM target: `v0.2.12`
- Source commit used for both corrected deployments: `83a2dbb53e247e54aa73f3224c174dcf6b1625f5`
- Source-code CI: [run 38605324552](https://github.com/ometere123/paretorail/actions/runs/38605324552), green for that exact source commit

The stable network guard and RPC chain-ID guard both verified `61999` before deployment. No 61997 or preview RPC was used.

## Corrected ParetoRail

| item | value |
|---|---|
| address | `0x45df5A40bf702306bd9A30Ae5Bec1847C2e6efE1` |
| deployment transaction | `0xec1809fb315effc9b7a37212fe508a2f005a0a16479e42bcfd6efb455f9f270d` |
| receipt | `FINALIZED / MAJORITY_AGREE / SUCCESS` |
| deployed source commit | `83a2dbb53e247e54aa73f3224c174dcf6b1625f5` |
| source bytes | `26,200` |
| source SHA-256 | `f96cd5dc10d5ddbdfad3d573b50eb2533cda8d82c88695a47d6480b2199f0a32` |
| source parity | `gen_getContractCode` returned the exact committed bytes and SHA-256 |

## Corrected AmendedActionGate

| item | value |
|---|---|
| address | `0xAA543bF4395A87A744fc4b5813BA6cc8960C18AE` |
| deployment transaction | `0x3a0948c43ff77efe22d3c57af30254f6b48604b76f28346a49f04fdb12e99a24` |
| receipt | `FINALIZED / MAJORITY_AGREE / SUCCESS` |
| deployed source commit | `83a2dbb53e247e54aa73f3224c174dcf6b1625f5` |
| source bytes | `1,210` |
| source SHA-256 | `2044110f4e6c20ade3335eabaf1765be71738440713ac6f81b6773fe4dc55c7c` |
| source parity | `gen_getContractCode` returned the exact committed bytes and SHA-256 |
| bound ParetoRail | `0x45df5A40bf702306bd9A30Ae5Bec1847C2e6efE1` |
| bound proposal | `2` |
| bound adopted head | `416b1751429f20d20e5c3c3edb6c884dd5fd36e5ff287fd51e4f6a643d5c8138` |

The constructor calldata in the finalized deployment receipt contains the exact ParetoRail address, proposal ID and adopted head above. The Consumer source is unchanged from the original example, but the old Consumer was not reused because its immutable binding pointed at the superseded ParetoRail.

## Corrected live lifecycle

All hashes below are for the corrected ParetoRail unless explicitly identified as Consumer transactions. Each cited write was checked at `FINALIZED`. Successful writes also had `MAJORITY_AGREE` and leader execution `SUCCESS`; rejected writes are identified as rejected and are not counted as successful state transitions.

### Baseline, roster and seal

- Buyer/creator `0x951e6B75530774fF82321a5ae54e14F778F0C855` created agreement `1` in `0xb7dd01221408e3618f61ef349c5f7c199baf74f304234b545a8afaa844eb2b97`.
- Supplier `0xB845a69860ba4CDf19CfDC5AfbAF2e20b6bE86b0` appears in the finalized roster readback. Its CLI transaction hash was not retained in the evidence capture and is intentionally not guessed.
- Referrer `0xac3AC69dC0Bde389256dD6748C75817ead9286D9` was added in `0x388e1f01a09dc0aeccb0fc75a79d85918ec6836381b1a59e1a4b69a5d2299903`.
- Individual attestations finalized in `0x33c1eaeb41fb04e9cd1a7dcf0b6ab25ee274335ada12f22bb83387482dda4a97`, `0x4abf499382717ca945029e04b63ba4639e36eaac077734dddd71e06029daa4c5`, and `0x9597a89be572bc4f8c2b16bdff7f30889550075f0611491e159f481ed393f2da`.
- Sealing finalized in `0xc3ae91645560df207a738c03ae15e544cb5efee1043e544ebf1e51abd03a3a46`.
- Sealed readback: genesis `696cf2dfc942eab28678d6a961e0c0b881174d8e72ccf9978333ff3c5849e5b0`, version `1`, head `b820521e28def101514965baf518da6f22d938ea64f272070f10d6b73b052293`, quorum `2`, and all three parties attested.

### Rejection, adoption and liveness

- Buyer-price increase attempt `0xfaf7657bc4a6a59f9ec154804a2efbd4abab3710f1a4c79ec01bf6277c529904` finalized `MAJORITY_DISAGREE`; the observed vector was `WNB` and no proposal was persisted.
- Supplier-deadline weakening attempt `0xa05a222d1370b7db925b6a726b522287cdf01b71976900a8972af9534855b2d7` finalized `MAJORITY_DISAGREE`; no proposal was persisted.
- Referral reduction/hidden-worsening attempt `0xcad9ab02190bad7f418d22d56944bd7d60eca62bb2eeca60b773b18ac88910a2` finalized `MAJORITY_DISAGREE`; no proposal was persisted.
- A semantically non-convergent candidate `0xa506f0e2d0bf8ffa042712635a58eb4df1d6b279459a1f95291b4ac8abfb4350` also finalized without state change.
- Accepted neutral proposal `1` was submitted in `0x60ca881b3639c9070f2efb0084d3f27fbcab0eeaa63179a04dbab60026a9be4b`; readback was `NNN`. The captured Buyer approval finalized in `0xa1d322667667d7be8c4948192a404e050700351e304f69df7cadc7b2d4350e5c`; the complete approval mask was read back before finalization. Finalization was `0x8919828e33e8908b93be12b90a26e424959a761d59c55b3bfad55cea393fd513`. The resulting head was `c45f36a5bf2509c699810517caace828e8003e7c3529ff19e78d76b546f5cf8c`, version `2`.
- Cosmetic proposal `2` was submitted in `0xef12d4be231fba13d7167704c8681af3b26afdc29229c7cc701d3da3cd3b7caf`, read back `NNN`, and approved in `0xfc4973a4266f00fc3643da1472fbb58c33e96b34d94d50a1dcc8903238402912` and `0xf264271b80481d5825804b253b5e74e08f4abe91910eaf4260976bada2112f55`. Finalization was `0x5bcb84001807d3661f67eafdb0916090aa45be684113a37f6e58d3d1a8d696d7`; the final readback is version `3`, head `416b1751429f20d20e5c3c3edb6c884dd5fd36e5ff287fd51e4f6a643d5c8138`.
- The same proposer’s second current-head attempt `0x77700b82fecaae07032752511ebd87e5f0c76f977eb6e40922487160943bc16d` finalized with execution error `PROPOSAL_QUOTA`; the proposal page remained `[1, 2]`.
- Another party independently submitted proposal `3` in `0xc29237a673e44c0fd88437a579fb9cf80b2edd346f26ec06378a596d4911d99`; it was recorded as pending against the old head. After proposal `2` advanced the head, an approval attempt `0x87cb079aabf866b835843727635baa94dae8211e2b5f0ed396639648398b5bf0` finalized with execution error `STALE_PROPOSAL` and did not mutate state. The final readback exposes proposal IDs `[1, 2, 3]`, and proposal `3` remains directly readable as historical pending/stale data.

### Consumer one-shot proof

- `perform()` on the corrected Consumer finalized in `0x6642b5173651e0a019e5705fa292d6b7ae1a24b553bc762c7896a4eb5ee0826c` with `MAJORITY_AGREE / SUCCESS`; `was_performed()` read back `true`.
- A second `perform()` finalized in `0xe9b0b4b7c88934e881d3a7e3655694aa1254e67e608d2879030700cb0c3de3d4` with a leader rollback payload `ALREADY_PERFORMED`; `was_performed()` remained `true`.

## Verification limits

The consensus boundary certifies the ordered impact vector, not leader prose or witness wording. The live fixture is a controlled demonstration of the contract primitive, not independent commercial-market evidence. Wallet attestation is not legal identity proof. Direct Mode and offline tests are not substitutes for live validator diversity; the finalized receipts above are the live evidence. History is append-only and must be read through bounded pages rather than an unbounded agreement getter.
