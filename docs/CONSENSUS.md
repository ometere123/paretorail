# Consensus specification

The exact agreed input is a tuple of the sealed `purpose`, ordered `[(wallet, role)]` roster, operative previous full agreement text, and proposed complete replacement text. The proposer cannot change a party, omit one from the vector, supply a substitute per-party summary, or replace `old_terms` with a different source. All user-authored text in prompts is untrusted data.

## Classifications

`N` no material worsening or improvement; `B` material improvement with no material worsening; `W` one or more material worsenings regardless of offsetting benefits; `U` ambiguous, inconsistent, unsafe-to-classify. Positive claims are `N` or `B`. There is no scalar "fairness score" and no objective "net benefit". All parties must be classified in roster index order; unknown outcomes produce a permanently blocked proposal, never a neutral assumption.

## Non-determinism and validator agreement

- Leader calls `gl.nondet.exec_prompt(response_format='json')` and normalises output to exactly one bounded vector/reason/witness record. Malformed verdicts normalise to an all-`U` record.
- Validator independently reruns the full old/new agreement comparison, checks exact identity/order/count of outcome codes and rejects any disagreement. It does not require the same wording of explanation.
- For any proposed `N`/`B` classifier, validator also executes an independent counterexample search against deleted remedies, shifting liability, deadlines, exceptions, scope expansion and hidden obligations. Any identified hidden material worsening of such a party, validator uncertainty, malformed audit or callback exception rejects agreement.
- The leader's reason and worsening witness are stored as explanations with explicit `LEADER_REPORTED_NOT_CERTIFIED` provenance. They are not cryptographically corroborated natural-language facts.

## Deterministic transitions

`assessment_vector → harmed_mask`, where bit `i` is set if and only if party `i` is W. Required: all `harmed_mask` bits in current explicit approval mask and popcount of approvals >= fixed quorum. Any `U` blocks the entire proposal. No float arithmetic, implicit votes, moral balancing, separate model-derived consent, owner bypass or automatic adoption.

On finalisation, the new head incorporates genesis, predecessor, proposal id, frozen semantic-receipt hash, candidate text hash and version. Once the head moves, competing proposals become stale even if they had gathered sufficient consent earlier. Historical proposal record remains intact.

## Proposal liveness and history

Submission capacity is scoped to the current sealed head rather than to a
permanent agreement-wide lifetime counter. Each registered party has one
proposal opportunity per head. A blocked or cancelled proposal consumes only
the submitting party's opportunity, so one participant cannot exhaust the
other parties' capacity. Adoption resets all party opportunities for the new
head; old-head proposals become stale and cannot consume new-head capacity.

Proposal records are append-only and retain globally unique IDs. Because
history can outlive a single fixed lifetime cap, `get_agreement()` exposes a
bounded recent proposal window and `get_proposal_ids_page()` provides
bounded historical enumeration (`limit <= 25`); individual old proposals
remain directly readable with `get_proposal()`.

## Security intuition and limits

Even multiple independent LLMs can share blind spots. This protocol is *not* formal semantic proof or legal determination. It is an auditable conservative voting mechanism that raises the bar for adverse changes. The protocol cannot bind an unregistered third party and cannot certify outcomes beyond material changes visible in the supplied old/new texts.
