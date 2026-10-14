# StudioNet 61999 execution and evidence checklist

The current corrected deployment and lifecycle evidence are recorded in [DEPLOYMENT.md](../DEPLOYMENT.md). This project is restricted to stable `studionet`, chain `61999`, RPC `https://studio.genlayer.com/api`, and the repository-local `genlayer@0.39.1` CLI. Never use the global RC CLI, `studio-dev`, `studio-next` or chain `61997`.

## Reproduction gates

1. Install the pinned dependencies with `npm install` and `python -m pip install -r requirements-direct.txt` under Python 3.12.
2. Verify `./node_modules/.bin/genlayer --version` reports `0.39.1`.
3. Run `./node_modules/.bin/genlayer network set studionet`, `node scripts/network-guard.cjs` and `python scripts/rpc-guard.py`; stop on any mismatch.
4. Run the offline suite, official Direct Mode suite, mutation suite, both contract lint/validation commands and `python scripts/preflight.py`.
5. Deploy only from a clean source commit. Wait for `FINALIZED`; an `ACCEPTED` transaction is not finality and a finalized execution error is not a successful proof.
6. Retrieve deployed source with `gen_getContractCode` (the RPC returns base64), decode it, and compare byte count and SHA-256 against the exact committed file.

## Current corrected addresses

- ParetoRail: `0x45df5A40bf702306bd9A30Ae5Bec1847C2e6efE1`
- ParetoRail deployment: `0xec1809fb315effc9b7a37212fe508a2f005a0a16479e42bcfd6efb455f9f270d`
- AmendedActionGate: `0xAA543bF4395A87A744fc4b5813BA6cc8960C18AE`
- Consumer deployment: `0x3a0948c43ff77efe22d3c57af30254f6b48604b76f28346a49f04fdb12e99a24`
- Consumer binding: proposal `2`, head `416b1751429f20d20e5c3c3edb6c884dd5fd36e5ff287fd51e4f6a643d5c8138`

## Corrected live sequence

The reproducible run used three distinct public wallets: Buyer/creator `0x951e6B75530774fF82321a5ae54e14F778F0C855`, Supplier `0xB845a69860ba4CDf19CfDC5AfbAF2e20b6bE86b0`, and Referrer `0xac3AC69dC0Bde389256dD6748C75817ead9286D9`.

- Create agreement `1`, add Supplier and Referrer, attest from all three wallets, and seal. The sealed readback is version `1`, genesis `696cf2dfc942eab28678d6a961e0c0b881174d8e72ccf9978333ff3c5849e5b0`, head `b820521e28def101514965baf518da6f22d938ea64f272070f10d6b73b052293`.
- Submit adverse candidates and record the actual consensus result. The price increase and shortened supplier deadline finalized `MAJORITY_DISAGREE` and did not persist.
- Submit neutral proposal `1`, collect approvals, finalize, and read head `c45f36a5bf2509c699810517caace828e8003e7c3529ff19e78d76b546f5cf8c`.
- Submit neutral cosmetic proposal `2`, approve, finalize, and read final version `3` with head `416b1751429f20d20e5c3c3edb6c884dd5fd36e5ff287fd51e4f6a643d5c8138`.
- Attempt a second proposal from the same party on the same head: `PROPOSAL_QUOTA`; a different party can still create its own proposal. After adoption, old-head candidates fail as `STALE_PROPOSAL`.
- Execute the head-pinned Consumer once and read `was_performed() == true`; the second call finalizes with `ALREADY_PERFORMED` rollback and does not undo the first action.

This live run demonstrates the corrected per-party/per-head submission capacity and one-shot consumer gate. It does not claim that every possible natural-language amendment will converge to a particular vector; disagreement or uncertainty is a safe non-transition.
