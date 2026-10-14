# ParetoRail

**A standalone GenLayer Intelligent Contract for party-specific consent to adverse amendments.** No frontend. No backend. Stable **StudioNet `studionet` / chain ID `61999` / RPC `https://studio.genlayer.com/api` / repository-local CLI `genlayer@0.39.1` only.**

## The missing invariant

Three parties adopt a service agreement. Later, a majority wants to reduce Carol's referral fee. Ordinary majority voting can remove Carol's right without Carol's consent; an AI summary that says "the amendment is fair" is not a defensible rule.

ParetoRail enforces a bounded invariant: **a proposed amended agreement can become operative only when the frozen base quorum approves and every original party that materially worsens also individually approves the exact version.** A party who receives both a benefit and a material loss still counts as worsened. Any ambiguous party impact blocks amendment adoption. This is *not* a proof of globally Pareto-efficient economics; it is an enforceable no-unconsented-worsening rule for up to six explicitly identified parties.

```
Initial agreement: all parties attest the full text and frozen roster.
  Buyer pays 50 GEN; supplier delivers in 5 days; referrer gets 10%.

Proposed terms:
  Buyer pays 50 GEN; supplier delivers in 8 days; referrer gets 5%.

Independent semantic assessment, in fixed party order:
  Buyer     W (worse: receives delivery later)
  Supplier  B (better: extra delivery time)
  Referrer  W (worse: referral reduced)

Base quorum 2/3 votes YES (Buyer + Supplier).
  => NOT FINALIZABLE (Referrer's express YES is missing)
Referrer votes YES after inspecting exact immutable candidate.
  => FINALIZABLE; anyone can finalize the exact head-pinned amendment.
```

## Why semantic consensus is essential

An amendment may move costs, deadlines, rights, defenses, compensation, exclusions, exceptions, liability, remedies and authorizations without mentioning a party by name. Deterministic text diffs cannot reliably establish party-specific material impacts. `gl.vm.run_nondet_unsafe` makes that bounded relation the only nondeterministic boundary:

1. The leader compares the **entire frozen old/new agreement** against the exact sealed party roster and emits only `N`, `B`, `W`, `U` for every party, plus non-authoritative explanation.
2. An independent validator runs its own LLM comparison over the same full evidence, and **requires exact agreement on every party's impact code**. Merely checking JSON shape is never enough.
3. For any proposal claiming at least one party is neutral or improved, validators independently hunt for concealed worsening and reject a leader that misses it or cannot rule it out.
4. The contract deterministically derives a `W` bitmask from the consensus result; validates exact signature-sender votes and quorum; checks head/version; then creates a hash-linked immutable amendment version. `U` fails closed before voting.

Consensus binds the material **impact vector**, not the witness prose. Reasons and witnesses are stored as *leader-reported explanations*, never advertised as independently certified facts. Models can err; ParetoRail is a conservative mechanism, not a substitute for legal advice, formal proofs or independent financial review.

## Agreement lifecycle

1. `create_agreement(purpose, baseline_terms, creator_role, quorum)` creates a draft and installs the sender as participant 0.
2. The creator `add_party(agreement_id, wallet, role)` until there are 2–6 distinct parties. No zero address or additions after sealing. Role and party order are part of the immutable genesis binding.
3. Every party, including creator, calls `attest_initial(agreement_id)` **after the final roster is set**. Any later addition increments roster revision and invalidates all earlier attestations.
4. `seal_agreement(agreement_id)` is permitted only after unanimous attestation. It fixes the party set, roles, policy purpose, quorum, genesis and initial head.
5. Any party calls `propose_amendment(agreement_id, new_terms, expected_head_hash)`. Every proposal freezes the old head, full old/new texts, exact vote/impact vector and a hash of the semantic assessment.
   Each party has one independent submission opportunity per sealed head. A blocked or cancelled proposal consumes only that proposer's slot; adoption resets all party slots for the new head.
6. All approval calls are explicit on-chain, one wallet per roster index: `approve(proposal_id)` and `withdraw_approval(proposal_id)`.
7. `finalize_amendment(proposal_id)` succeeds only when minimum quorum **AND every harmed party's explicit approval** are present. Its caller cannot override those rules. No unapproved party votes by proxy.
8. The operative head increments and is hash-linked to genesis, predecessor, proposal and consensus receipt. Other proposals from the previous head go stale; no hidden rebasing.

No unilateral privileged override, admin mutation of a sealed agreement, or backdoor change of party identity. Historical proposals retain their original interpretation, even after head advance. Proposer may cancel a live unfinalized proposal.

## API

| Writes | Purpose |
|---|---|
| `create_agreement(purpose, baseline_terms, creator_role, quorum) -> u256` | Create draft. Creator is participant zero. |
| `add_party(agreement_id, wallet, role) -> u256` | Append bounded roster member. |
| `attest_initial(agreement_id) -> str` | Exact-roster current-revision attestation. |
| `seal_agreement(agreement_id) -> str` | Unanimously attested genesis head. |
| `propose_amendment(agreement_id, new_terms, expected_head_hash) -> u256` | Independently classify party impacts. |
| `approve(proposal_id)` | Self-consent to frozen candidate. |
| `withdraw_approval(proposal_id)` | Withdraw before adoption. |
| `cancel_proposal(proposal_id)` | Proposer cancels a still-live proposal. |
| `finalize_amendment(proposal_id) -> str` | Apply only if all deterministic conditions hold. |

| Views | Purpose |
|---|---|
| `get_agreement(id)` | Purpose, roster, attestations, terms, genesis, head, version. |
| `get_proposal(id)` | Impact vector, harmed/approval masks, evidence, receipts, state. |
| `get_proposal_ids_page(id, offset, limit)` | Bounded historical proposal-ID pagination; `limit` is at most 25. |
| `can_finalize(id)` | Current deterministic approval predicate. |
| `current_head(id)` | Current head or empty. |
| `matches_head(id, hash)` | Exact current-head consumer gate. |
| `is_adopted(proposal_id, expected_head)` | Adopted proposal AND current head still matches. |

**Status enum:** `1=PENDING`, `2=BLOCKED` (ambiguous), `3=ADOPTED`, `4=CANCELLED`. **Impact symbols:** `N=neutral`, `B=better and not worse`, `W=materially worse on any dimension`, `U=unknown/ambiguous`.

**Consumer example:** `contracts/consumer_example.py` is optional. Its `AmendedActionGate` checks typed GenLayer IC-to-IC view status and refuses to perform if the exact proposal/head is not currently adopted. The action is one-shot and intentionally has no escrow or funds. This example is *source code*, not a claim that a live cross-contract lifecycle was executed.

## Running locally — important compatibility lock

The developer workstation's global CLI `0.40.0rc2` is incompatible with this stable StudioNet target. **Never invoke global `genlayer`.** Install the repository-local version and call its exact binary:

```bash
npm install --no-audit --no-fund
./node_modules/.bin/genlayer --version         # must print 0.39.1
./node_modules/.bin/genlayer network set studionet
./node_modules/.bin/genlayer network info
node scripts/network-guard.cjs                 # must verify 61999 + stable RPC
python scripts/rpc-guard.py                   # optional live chainId check
```

Only then deploy:

```bash
./node_modules/.bin/genlayer deploy --contract contracts/paretorail.py --rpc https://studio.genlayer.com/api
```

Before deployment, fund/choose a CLI account via `./node_modules/.bin/genlayer account --help`; do not commit any private keys. **Record deployment tx/hash/address and wait for `FINALIZED` with successful execution**, not merely ACCEPTED. Then verify `genlayer code`, `genlayer schema`, and actual view readbacks against the source digest.

### Test layers and precise evidence status

```bash
python -m pip install -r requirements.txt
python -m pytest tests/test_offline.py -q
python scripts/preflight.py
# On a workstation with internet access:
python -m pip install -r requirements-direct.txt
python -m pytest tests/direct/ -v
genvm-lint check contracts/paretorail.py
```

The current verified run reports **36/36 offline mock-runtime tests**, **14/14 official Direct Mode tests**, **10/10 behavioral security mutations killed**, and **3/3 GenVM lint checks for each deployable contract**. The local CLI is `genlayer@0.39.1`; the network guards verify stable StudioNet `61999` at `https://studio.genlayer.com/api`.

The corrected ParetoRail deployment used for the current live evidence is `0x45df5A40bf702306bd9A30Ae5Bec1847C2e6efE1`. Its deployment transaction is `0xec1809fb315effc9b7a37212fe508a2f005a0a16479e42bcfd6efb455f9f270d`, finalized with `MAJORITY_AGREE` and successful execution. The deployed source is the exact `83a2dbb53e247e54aa73f3224c174dcf6b1625f5` contract source: 26,200 bytes at SHA-256 `f96cd5dc10d5ddbdfad3d573b50eb2533cda8d82c88695a47d6480b2199f0a32`.

The corrected head-pinned consumer is deployed as `AmendedActionGate` at `0xAA543bF4395A87A744fc4b5813BA6cc8960C18AE`, bound at construction to ParetoRail `0x45df5A40bf702306bd9A30Ae5Bec1847C2e6efE1`, proposal `2`, and adopted head `416b1751429f20d20e5c3c3edb6c884dd5fd36e5ff287fd51e4f6a643d5c8138`. Its deployment transaction is `0x3a0948c43ff77efe22d3c57af30254f6b48604b76f28346a49f04fdb12e99a24`; its 1,210-byte source has SHA-256 `2044110f4e6c20ade3335eabaf1765be71738440713ac6f81b6773fe4dc55c7c`, and retrieved deployed code matches exactly. See [DEPLOYMENT.md](DEPLOYMENT.md) and [SUBMISSION.md](SUBMISSION.md) for the transaction-level record. These live proofs are bounded demonstrations, not legal or commercial-market certification. The superseded deployment is preserved in [docs/HISTORY.md](docs/HISTORY.md).

## Boundaries / safety

- Up to **6 parties** and one proposal opportunity per party per sealed head; historical proposal IDs remain append-only and are exposed through bounded pages of at most 25. Entire text is bounded to 3,500 chars per version.
- A party cannot refill its head slot through trivial wording changes. Blocked and cancelled proposals consume only that party's current-head slot; an adopted head resets all party slots, while old proposals remain immutable and directly addressable.
- Every party explicitly attests initial roster and agreement; creator alone cannot invent their consent.
- Proposals pin both old head/version and new text/consensus receipt.
- Quorum never substitutes for a harmed party's explicit approval.
- A good outcome cannot be inferred from other parties' net benefit; any loss marks a party `W`.
- Independent validators compare every party's material economic position and run counterexample search for claimed non-worsening.
- `U`, source/party ambiguity, malformed output and validator mismatch cannot advance the head.
- Consensus explanation is leader-reported and unauthoritative; only classification vector is certified.
- No third-party obligations are made binding without becoming roster parties.
- No frontend, backend, escrow, payment custody, wallet connector, Docker stack, privileged admin or cross-network fallbacks.

Read [Consensus & Safety](docs/CONSENSUS.md), [Threat model](docs/THREAT_MODEL.md) and [StudioNet evidence checklist](docs/STUDIONET_EXECUTION.md) before deploying.
