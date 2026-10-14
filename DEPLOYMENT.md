# ParetoRail StudioNet deployment evidence

This is the factual deployment record for the supplied contract-only ParetoRail repository. Network identity was checked before deployment with the repository-local CLI and the RPC guard:

- Network: stable `studionet`
- Chain ID: `61999` / `0xF22F`
- RPC: `https://studio.genlayer.com/api`
- Local CLI: `genlayer@0.39.1`
- Explorer base reported by the CLI: `https://genlayer-explorer.vercel.app`

## Source and deployment

The deployed commit is the source commit containing the unchanged ParetoRail contract and the test/tooling corrections in this repository. The contract source is 23,686 bytes and SHA-256:

```text
f19d28c009259ddf22c289936beb43b7d7c064dcaa83f69e7049ff314580215d
```

`gen_getContractCode` returned exactly 23,686 bytes with the same SHA-256. The schema readback reported `ParetoRail` with 15 methods (6 view, 9 write).

| item | value |
|---|---|
| ParetoRail address | `0x3cF4773bAC377CeaA3f90b5AE3bC1E317F315411` |
| deployment transaction | `0xf054cc46ea3677d9aa5aa5012f1393fc644bc871beb96252ccd72a4472db13cd` |
| deployment receipt | `FINALIZED / MAJORITY_AGREE / SUCCESS` |
| contract source parity | exact byte and SHA-256 match |

The optional `AmendedActionGate` source is 1,210 bytes with SHA-256 `2044110f4e6c20ade3335eabaf1765be71738440713ac6f81b6773fe4dc55c7c`. The deployed code returned the same bytes and digest.

| item | value |
|---|---|
| consumer address | `0xd3b91F93ECE55c188D2E8938A37cF35ded583f39` |
| consumer deployment transaction | `0x822d7b52af0b3fae3878e29f1b37f159fa77bbbc62bb4f4eec464e59c5bc8eb3` |
| consumer receipt | `FINALIZED / MAJORITY_AGREE / SUCCESS` |
| bound ParetoRail | `0x3cF4773bAC377CeaA3f90b5AE3bC1E317F315411` |
| consumer binding | proposal `4`, head `cda68fa595c6064411be0eed3b0a888a5872551c8ac4d9f1418807061e402cdd` |

## Finalized live lifecycle

All successful writes below were checked at `FINALIZED` with `MAJORITY_AGREE` and successful leader execution. The readbacks were made against the deployed contract after finality.

### Baseline and roster

- Agreement `2` was created by beneficiary/buyer `0x951e6B75530774fF82321a5ae54e14F778F0C855` in `0x9e744a8c2309656b4038479a0b4109dcb5fe274d0a2107b76e16be6ea8aa2729`.
- The finalized roster readback contains three distinct parties: Buyer `0x951e...`, Supplier `0xB845...`, and Referrer `0xac3A...`. The Supplier add-party hash was not retained by the CLI output and is not claimed as transaction-level evidence here; the final roster and all subsequent state readbacks are authoritative.
- Referrer addition finalized in `0xfb8b877f409a3b44027c4ba53a98de5da5325d8f4515998ac987bd744be3d799`.
- Individual attestations finalized in:
  - Buyer: `0xe4d433455296600a2be8acb78aa69065b1792fc49599e60e08c0fa6c8e006d27`
  - Supplier: `0x66be826f6d579c5f485e702070464df1d1d6e40258047defebbe6e25d6b20654`
  - Referrer: `0x5b8add132ed501f313bf111a7240cf09128d9ea9498835e8317eb981a6f52756`
- Sealing finalized in `0x7a4009a3a9d04dcf19801c731c40700bcaa1187f45e51ec29429b3526e899c64`.
- Readback after sealing: version `1`, genesis hash `24e940651052b794062953b48da74eb3fde27b8d723f3401e6df4120e1536071`, head `f8c280b8c7e1522551d469de93191f79c664d927611dff68444c4684c77594fa`, and all three `attested: true`.

### Harmed-party consent and adoption

Proposal `3` was created in finalized transaction `0x4f2ffc428f44e51734a52d38555716354b2f3302baf032cff3008536208fab42`. The final proposal readback was:

- impact vector `BWN` in roster order Buyer/Supplier/Referrer;
- impacted mask `2`, identifying Supplier as the harmed party;
- exact candidate hash `edb11715a7c8dcb523c97d3771cbb92141098654d8bb95c5213c8904fdc95859`.

Buyer and Referrer approvals finalized in `0xd010064c5a35226b02c60c6756780d66933b5fd67bfde41184fb46fcdfef6e56` and `0x8d16775f02656f20abc577f4c32c212400f5836ac0b48f95feb2e57fc19f9c14`. The readback then showed approval mask `5` and `finalizable: false`, proving quorum without the harmed Supplier was insufficient. Supplier approval finalized in `0x3cc3a0580a46531b9bf7c15dcbcd28a370343ed2c3857b176d08ea84eda1a236`. Finalization finalized in `0x14148f59d5df31ceb7b2209524ff5cff16d70886702ef4856fc111eece619332`.

The resulting readback was version `2`, current terms with the three-day Supplier deadline, and head `c42256f33d2602b7bac4f14fc620d189f648ac3ba3ff17197aa855c3a1140c4b`. The proposal status was `ADOPTED` and approval mask `7`.

### Non-harming adoption and stale head

Proposal `4` changed only the order of semantically equivalent clauses. Its finalized readback was `NNN`, impacted mask `0`, and base head `c42256...`. Approvals finalized in `0x2a9999ce9ba24bd291e63f4cd05f6f313affaa5ae893f9ebc1afc790ac6641a0` and `0x0906634181eff2917a603803c5d301e7f7f0130c6b30a9c30f1c0d93992271bb`; adoption finalized in `0x0e0be3a65d1aa4c96f0ea9d3f372285b39fe12e3ccf2318bb0f04cdf6e86325f`.

The final readback was version `3`, head `cda68fa595c6064411be0eed3b0a888a5872551c8ac4d9f1418807061e402cdd`, and proposal `4` status `ADOPTED`. A competing proposal from the old version-1 head was then finalized as a failed execution in `0xb79d91907f6516d9eb48c5d542c0c67751e564b09798327cdb54e9cf1cd37cb8`, with `STALE_PROPOSAL`; the head remained version `3`.

### Hidden worsening and ambiguity

A hidden referral carve-out attempt was submitted in `0xe274c479452f285ea91e178d966d039c295aff6310ceafeb25c44c8884412794`. It finalized with `MAJORITY_DISAGREE` (`result: 7`) and did not append a proposal or change the agreement readback. A separate semantically equivalent formatting attempt finalized with the same disagreement result in `0x414010d85c73d86636a8daa2ebbb59d122297b660074f150e032e305247e63c6`; it also did not change state. These are rejection evidence, not successful amendments.

### Consumer gate

`AmendedActionGate.perform()` finalized successfully in `0xf3230bc4cafa8237f595667634cc9dda5251279ee343d225b087505e9b12ec9b`; `was_performed()` read back `true`. A second call finalized with `MAJORITY_AGREE` but rolled back with `ALREADY_PERFORMED` in `0x2ef4552024ab6748dd88b0aed337d7fdf68d0f1ab3ed10f94e521013b6ab189f`. No funds are held by this example consumer.

## Limitations

The consensus boundary certifies the bounded impact vector, not leader prose. Provider/party wallet authorization does not prove legal identity. The live fixture is a controlled demonstration of the contract primitive, not independent market evidence. Direct Mode and mock-runtime tests do not establish live validator diversity; the live receipts above do. The Supplier add-party transaction hash was not retained by the CLI output, so it is intentionally omitted rather than guessed.
