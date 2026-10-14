"""Network-lock and structural checks runnable without installed GenLayer tooling."""
from pathlib import Path
import ast
import json
import hashlib

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'contracts'/'paretorail.py'


def main():
    failures = []
    def check(ok, message):
        print(('PASS' if ok else 'FAIL')+' '+message)
        if not ok:
            failures.append(message)
    package = json.loads((ROOT/'package.json').read_text())
    src = SOURCE.read_text()
    tree = ast.parse(src)
    funcs = {n.name:n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    check(package['devDependencies']['genlayer']=='0.39.1','local CLI fixed to 0.39.1')
    check('61999' in (ROOT/'.env.example').read_text(), 'stable chain configured')
    check('https://studio.genlayer.com/api' in (ROOT/'.env.example').read_text(), 'stable RPC configured')
    check('py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6' in src,'stable GenVM dependency header')
    check('gl.vm.run_nondet_unsafe' in src, 'custom consensus boundary')
    check('INDEPENDENT VALIDATOR' in src, 'independent party-by-party assessment')
    check('INDEPENDENT ADVERSARIAL' in src, 'adversarial falsification')
    check('impacted_mask' in src and 'approvals_mask' in src,'harmed parties require approval')
    check('STALE_PROPOSAL' in src and 'STALE_HEAD' in src,'head pin and replay resistance')
    check('roster_revision' in src and 'MISSING_ATTESTATION' in src,'complete roster attestation')
    check('U' in src and 'STATUS_BLOCKED' in src,'ambiguous verdict fail closed')
    check(isinstance(tree, ast.Module) and len(tree.body) > 5, 'Python AST parse succeeded')
    check(all(name in funcs for name in ('create_agreement','add_party','attest_initial',
        'seal_agreement','propose_amendment','approve','withdraw_approval','finalize_amendment',
        'get_agreement','get_proposal','matches_head','is_adopted')), 'complete contract API')
    check(not any((ROOT/x).exists() for x in ('frontend','backend','app','pages')), 'contract-only package')
    check(not any(x in src for x in ('0.40.0rc','studio-dev.genlayer.com','61997')), 'contract has no preview-network references')
    print('SHA256 '+hashlib.sha256(src.encode()).hexdigest())
    if failures:
        raise SystemExit(f'{len(failures)} preflight checks failed')


if __name__=='__main__':
    main()
