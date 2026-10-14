"""Behavioral mutation checks for ParetoRail's security-critical gates.

Each mutant is written to a temporary source file and exercised by the real
offline behavioral harness in a subprocess.  A mutant is killed only when a
targeted invariant test fails; source-text presence alone is not evidence.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'contracts' / 'paretorail.py'


MUTATIONS = [
    (
        'remove harmed-party consent',
        [('if (int(p.impacted_mask) & approvals) != int(p.impacted_mask):', 'if False:')],
        'test_worsened_party_mandatory_consent',
    ),
    (
        'weaken quorum',
        [('return count >= int(a.quorum)', 'return count >= 0')],
        'test_no_worsening_still_requires_quorum',
    ),
    (
        'ignore stale head and version',
        [
            ('if not bool(a.sealed) or str(a.head_hash) != str(p.base_head_hash):', 'if not bool(a.sealed):'),
            ('if int(p.base_version) != int(a.version):', 'if False:'),
        ],
        'test_conflicting_proposals_head_invalidation',
    ),
    (
        'treat unknown as pending and finalizable',
        [
            ("p.status = u8(STATUS_BLOCKED if IMPACT_UNKNOWN in assessment['vector'] else STATUS_PENDING)", 'p.status = u8(STATUS_PENDING)'),
            ("if IMPACT_UNKNOWN in str(p.impact_vector):", 'if False:'),
        ],
        'test_ambiguous_impact_blocks',
    ),
    (
        'trust leader vector without equality check',
        [("if proposed['vector'] != independent['vector']:", 'if False:')],
        'test_leader_malicious_vector_rejected_by_independent_validator',
    ),
    (
        'ignore adversarial hidden-worsening findings',
        [('if missed:', 'if False:')],
        'test_adversarial_findings_reject_positive_leader',
    ),
    (
        'allow duplicate approvals',
        [('if int(p.approvals_mask) & (1 << i):', 'if False:')],
        'test_duplicate_votes_and_withdrawal',
    ),
    (
        'remove per-party quota',
        [('if int(a.head_proposal_counts[party_index]) >= MAX_PROPOSALS_PER_PARTY_PER_HEAD:', 'if False:')],
        'test_per_party_head_quota_preserves_other_parties_and_resets_after_adoption',
    ),
    (
        'restore shared proposal cap',
        [('if int(a.head_proposal_counts[party_index]) >= MAX_PROPOSALS_PER_PARTY_PER_HEAD:', 'if len(a.proposal_ids) >= 1:')],
        'test_per_party_head_quota_preserves_other_parties_and_resets_after_adoption',
    ),
    (
        'remove quota reset after adoption',
        [('self._reset_head_proposal_counts(a)', 'if False:\n            self._reset_head_proposal_counts(a)')],
        'test_per_party_head_quota_preserves_other_parties_and_resets_after_adoption',
    ),
]


@pytest.mark.parametrize('label,replacements,target', MUTATIONS, ids=[m[0] for m in MUTATIONS])
def test_security_critical_mutation_is_killed(tmp_path, label, replacements, target):
    source = SOURCE.read_text(encoding='utf-8')
    for old, new in replacements:
        assert source.count(old) == 1, f'{label}: mutation anchor is not unique'
        source = source.replace(old, new, 1)

    mutant_path = tmp_path / 'paretorail_mutant.py'
    mutant_path.write_text(source, encoding='utf-8')
    env = os.environ.copy()
    env['PARETORAIL_TEST_SOURCE'] = str(mutant_path)
    result = subprocess.run(
        [sys.executable, '-m', 'pytest', 'tests/test_offline.py', '-q', '-k', target],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, (
        f'Mutant survived: {label}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}'
    )
