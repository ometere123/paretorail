# Historical ParetoRail evidence

The following deployment was the pre-hardening deployment. It is retained for auditability only and is not current evidence for the corrected source.

## Superseded deployment

- ParetoRail: `0x3cF4773bAC377CeaA3f90b5AE3bC1E317F315411`
- deployment transaction: `0xf054cc46ea3677d9aa5aa5012f1393fc644bc871beb96252ccd72a4472db13cd`
- source commit: `380e81b08518ea57be66fdc6c64d693c8e011cd6`
- source SHA-256: `f19d28c009259ddf22c289936beb43b7d7c064dcaa83f69e7049ff314580215d`
- source bytes: `23,686`

## Superseded Consumer

- AmendedActionGate: `0xd3b91F93ECE55c188D2E8938A37cF35ded583f39`
- deployment transaction: `0x822d7b52af0b3fae3878e29f1b37f159fa77bbbc62bb4f4eec464e59c5bc8eb3`
- source SHA-256: `2044110f4e6c20ade3335eabaf1765be71738440713ac6f81b6773fe4dc55c7c`
- immutable binding: proposal `4`, head `cda68fa595c6064411be0eed3b0a888a5872551c8ac4d9f1418807061e402cdd`

The complete machine-readable record from that deployment is preserved at [`artifacts/studionet_proof_historical_690b6e.json`](../artifacts/studionet_proof_historical_690b6e.json). Those addresses, transactions and readbacks must not be presented as evidence for the corrected deployment at `0x45df5A40bf702306bd9A30Ae5Bec1847C2e6efE1`.

## Superseded corrected deployment (pre-recovery)

The following deployment contained the earlier per-party/per-head lifetime-opportunity implementation. It is retained as historical evidence because the final source replaces its terminal-proposal capacity behavior with recoverable active slots.

- ParetoRail: `0x45df5A40bf702306bd9A30Ae5Bec1847C2e6efE1`
- deployment transaction: `0xec1809fb315effc9b7a37212fe508a2f005a0a16479e42bcfd6efb455f9f270d`
- source commit: `83a2dbb53e247e54aa73f3224c174dcf6b1625f5`
- source SHA-256: `f96cd5dc10d5ddbdfad3d573b50eb2533cda8d82c88695a47d6480b2199f0a32`
- source bytes: `26,200`

### Superseded corrected consumer

- AmendedActionGate: `0xAA543bF4395A87A744fc4b5813BA6cc8960C18AE`
- deployment transaction: `0x3a0948c43ff77efe22d3c57af30254f6b48604b76f28346a49f04fdb12e99a24`
- immutable binding: ParetoRail `0x45df5A40bf702306bd9A30Ae5Bec1847C2e6efE1`, proposal `2`, head `416b1751429f20d20e5c3c3edb6c884dd5fd36e5ff287fd51e4f6a643d5c8138`
- source SHA-256: `2044110f4e6c20ade3335eabaf1765be71738440713ac6f81b6773fe4dc55c7c`

The machine-readable pre-recovery record is preserved at [`artifacts/studionet_proof_historical_06ed.json`](../artifacts/studionet_proof_historical_06ed.json). It must not be presented as evidence for the final deployment at `0x7a785f8790c44A470898D24772773E1A2713b15D`.
