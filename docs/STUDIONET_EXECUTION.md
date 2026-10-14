# StudioNet 61999 execution and evidence checklist

The final deployment and lifecycle evidence are recorded in [DEPLOYMENT.md](../DEPLOYMENT.md). This project is restricted to stable `studionet`, chain `61999`, RPC `https://studio.genlayer.com/api`, and repository-local `genlayer@0.39.1`. Never use the global RC CLI, `studio-dev`, `studio-next` or chain `61997`.

## Reproduction gates

1. Install the pinned dependencies with `npm install` and `python -m pip install -r requirements-direct.txt` under Python 3.12.
2. Verify `./node_modules/.bin/genlayer --version` reports `0.39.1`.
3. Run `./node_modules/.bin/genlayer network set studionet`, `node scripts/network-guard.cjs` and `python scripts/rpc-guard.py`; stop on any mismatch.
4. Run the offline suite, official Direct Mode suite, mutation suite, both contract lint/validation commands and `python scripts/preflight.py`.
5. Deploy only from a clean source commit. Wait for `FINALIZED`; an `ACCEPTED` transaction is not finality and a finalized execution error is not a successful proof.
6. Retrieve deployed source with `gen_getContractCode` (the RPC returns base64), decode it, and compare byte count and SHA-256 against the exact committed file.

## Final addresses

- ParetoRail: `0x7a785f8790c44A470898D24772773E1A2713b15D`
- ParetoRail deployment: `0x6c713238330a8252bd2858cc2c28863ef66c983e617abe81b5279c77f6c75a26`
- AmendedActionGate: `0x522984057CA9181417f8E97023EA6a02f9AA5121`
- Consumer deployment: `0x4e3d1ee0164f2419a17838ee615191575c7807f07a73203bd706d0446d4a2a01`
- Consumer binding: proposal `5`, head `970ff648c7f9096b8acb5fb8ae3f900b85536768ab6de4899c9fede4b557ee46`

## Final lifecycle

The run used three distinct public wallets: Buyer/creator `0x951e6B75530774fF82321a5ae54e14F778F0C855`, Supplier `0xB845a69860ba4CDf19CfDC5AfbAF2e20b6bE86b0`, and Referrer `0xac3AC69dC0Bde389256dD6748C75817ead9286D9`.

- Create agreement `1`, add the two parties, attest from all three wallets, and seal. Final readback: sealed, version `1`, genesis `0eb4e805cfe0f17987d26f32fe4dbe2f80d4fff784088244927ef5c2e1ecce34`, head `2b1c4fb351be47091ee8975cb185129a9160e95c1ef4e67a5463d97a0de6dec3`, quorum `2`.
- Demonstrate terminal cancellation recovery: Buyer’s proposal `1` and Supplier’s proposal `2` were each cancelled, then Buyer and Supplier submitted proposals `3` and `4` under the unchanged head. The append-only history readback retained `[1,2,3,4]`.
- Approve and finalize proposal `4`, then show an approval against old-head proposal `3` fails `STALE_PROPOSAL`.
- Submit proposal `5` reducing the Referrer share. The live vector was `NNW`; Buyer + Supplier produced `approvals_mask=3` while `can_finalize=false`. Referrer approval changed the mask to `7`; finalization advanced to version `3` and head `970ff648…`.
- Submit a vague candidate; the live model returned `WWW`, so it was cancelled without a head change. The official Direct Mode suite separately covers blocked `U` recovery.
- Execute the Consumer bound to proposal `5` and the final head once; the replay finalized with `ALREADY_PERFORMED` and did not change state.

See [DEPLOYMENT.md](../DEPLOYMENT.md) for every transaction hash, receipt classification and state readback. A rejected consensus transaction or finalized execution error is evidence of a safe non-transition, not successful adoption.
