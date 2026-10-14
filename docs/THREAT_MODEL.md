# Threat model

| Attacker / failure | Defense | Remaining limitation |
|---|---|---|
| Creator changes roster after parties sign | `roster_revision` invalidates all earlier attestations, seal requires everyone at latest revision | Party must review text/roster before attesting |
| Creator impersonates party | `gl.message.sender_address` exclusively determines signature/approval | Compromised private keys remain a general wallet risk |
| Majority votes to harm minority | Affected party bitmask must be subset of actual approvals | Semantic classification could miss a material loss |
| LLM net-benefit argument hides loss | `W` if **any** material harm regardless of offsetting benefit | No mathematical proof of all natural-language implications |
| Malicious leader returns all neutral | Validator independently compares full terms and adversarially searches for hidden losses | Shared-model blind spots possible |
| Malformed JSON / missing parties | Whole record normalised to all `U`; invalid shape rejected | A blocked proposal must be resubmitted, no automatic retry |
| Malicious text prompt injection | Delimited untrusted content; validator independently processes same frozen inputs | General prompt-injection robustness cannot be mathematically guaranteed |
| Proposal substitution after approval | Candidate text immutable, hashed, version/head bound | Participants should check receipt and exact candidate before approval |
| Simultaneous proposals | First finalised advances head; others fail stale-check | Requires new proposal on new head |
| Proposal-slot griefing | One submission opportunity per party per sealed head; adoption resets all slots; blocked/cancelled proposals consume only their proposer's slot | A party that uses its own slot must wait for head advancement; historical records are append-only and paginated |
| Historical-view exhaustion | Writes do not scan proposal history; agreement summary is bounded and proposal IDs have a max-25 page view | Total immutable history grows over successful or abandoned heads and must be paged |
| Vote replay/duplicate | Per proposal/party bitmask; no implicit approvals | Wallet compromise outside contract scope |
| Unilateral cancellation | Only proposer can cancel live proposal, cannot cancel adopted head | Pending proposal may remain indefinitely; no forced expiration |
| Unknown party harmed by terms | Fixed roster, prompt U for unclear nonparty effects, docs forbid nonparty binding | Contract cannot identify all external legal effects |
| False claims of certification | Witness explicitly leader-reported; no live evidence assertions | True semantic confidence is not numerically certified |
| Wrong-network deployment | Local CLI 0.39.1, chain 61999, RPC guarded; no preview fallback | Human must run guards before signing |
| External contract stale consumption | `is_adopted(proposal_id, expected_head)` verifies both adoption and current exact head | Consumer must pin exact contract address + expected head |

No GEN custody, escrow, slashing, user data, network fetches, frontend or backend are present in the primitive. Its semantic security boundary is deliberately small.
