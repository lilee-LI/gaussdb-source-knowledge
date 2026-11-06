"""Version-bound, content-addressed source evidence. Standard library, no source execution.

Bindings freeze selected files, not an entire product or a deployed binary.
Diffs suggest review work; they never certify semantic compatibility.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


def require(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save_new(path, raw):
    """Never silently refresh a frozen object or binding, including a corrupt one."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        require(path.is_file() and not path.is_symlink() and path.read_bytes() == raw,
                'Immutable destination changed')
        return
    require(not path.is_symlink(), 'Redirected immutable destination')
    with path.open('xb') as handle:
        handle.write(raw)


def source_path(value):
    require(isinstance(value, str) and bool(value), 'Source path required')
    require('\\' not in value and ':' not in value and '\x00' not in value and
            not PurePosixPath(value).is_absolute() and
            all(x not in ('', '.', '..') for x in value.split('/')), 'Unsafe source path')
    return value


def stored_path(root, relative):
    root = Path(root).resolve()
    path = root / source_path(relative)
    require(path.resolve().is_relative_to(root), 'Store path escapes root')
    require(not any(p.is_symlink() for p in (path, *path.parents) if p != root.parent),
            'Store paths must not be redirected')
    return path


def hash_value(value):
    require(isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value), 'Invalid SHA256')
    return value


def blob_path(store, sha):
    sha = hash_value(sha)
    return stored_path(store, 'objects/sha256/' + sha[:2] + '/' + sha + '.source')


def lines(raw):
    return raw.decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n').splitlines()


def excerpt(raw, start, end):
    data = lines(raw)
    require(type(start) is int and type(end) is int and 1 <= start <= end <= len(data),
            'Invalid inclusive evidence range')
    return '\n'.join(data[start - 1:end])


def create_binding(store, product, repository_id, revision, files, kind='controlled_snapshot', patches=None):
    for value in (product, repository_id, revision):
        require(isinstance(value, str) and value.strip(), 'Explicit source identity required')
    require(kind in ('git_commit', 'controlled_snapshot'), 'Unknown source provenance kind')
    if kind == 'git_commit':
        require(re.fullmatch('[0-9a-f]{40}|[0-9a-f]{64}', revision), 'Git binding needs a full commit ID')
        require(not patches, 'Git capture reads committed blobs; bind patched bytes as a controlled snapshot')
    patches = patches or []
    for patch in patches:
        require(set(patch) == {'id', 'sha256'} and bool(patch['id']), 'Patch needs ID and content digest')
        hash_value(patch['sha256'])
    require(isinstance(files, dict) and files, 'Nonempty selected source files required')
    entries = []
    for name, raw in sorted(files.items()):
        source_path(name)
        require(isinstance(raw, bytes), 'Raw bytes required')
        raw.decode('utf-8-sig')
        entries.append({'path': name, 'sha256': digest(raw), 'bytes': len(raw)})
    identity = {'product': product, 'repository_id': repository_id, 'revision': revision,
                'kind': kind, 'patches': patches}
    # An archive label is not a unique source identity; include its supplied bytes.
    source_identity = identity if kind == 'git_commit' else {**identity, 'supplied_files': entries}
    manifest = {'schema': 'source-binding/v1', **identity,
                'source_id': 'src-' + digest(canonical(source_identity)),
                'completeness': 'selected_files_only', 'files': entries}
    binding_id = 'sb-' + digest(canonical(manifest))
    manifest['binding_id'] = binding_id
    for row in entries:
        save_new(blob_path(store, row['sha256']), files[row['path']])
    save_new(stored_path(store, 'bindings/' + binding_id + '.json'), canonical(manifest) + b'\n')
    return manifest


def capture_git(store, repository, revision, product, repository_id, paths):
    repository = Path(repository).resolve(strict=True)
    require(paths and len(paths) == len(set(paths)), 'Unique nonempty capture paths required')
    def git(*args):
        result = subprocess.run(['git', '--no-replace-objects', '-C', str(repository), *args],
                                capture_output=True, check=True)
        return result.stdout
    require(isinstance(revision, str) and not revision.startswith('-'), 'Explicit Git revision required')
    commit = git('rev-parse', '--verify', revision + '^{commit}').decode().strip()
    files = {}
    for name in sorted(paths):
        source_path(name)
        tree = git('ls-tree', '-z', commit, '--', name).split(b'\0')
        require(len(tree) == 2 and tree[1] == b'', 'Source file missing or ambiguous in commit')
        meta, actual = tree[0].split(b'\t', 1)
        require(meta.startswith((b'100644 blob ', b'100755 blob ')) and actual.decode() == name,
                'Only regular committed files can be captured')
        files[name] = git('show', commit + ':' + name)
    return create_binding(store, product, repository_id, commit, files, kind='git_commit')


def capture_snapshot(store, directory, revision, product, repository_id, paths, patches=None):
    root = Path(directory).resolve(strict=True)
    require(paths and len(paths) == len(set(paths)), 'Unique nonempty capture paths required')
    files = {}
    for name in paths:
        path = stored_path(root, name)
        require(path.is_file(), 'Selected snapshot file missing')
        files[name] = path.read_bytes()
    return create_binding(store, product, repository_id, revision, files, patches=patches)


def binding(store, identity):
    require(isinstance(identity, str) and re.fullmatch('sb-[0-9a-f]{64}', identity), 'Invalid binding ID')
    value = load(stored_path(store, 'bindings/' + identity + '.json'))
    original = {k: v for k, v in value.items() if k != 'binding_id'}
    require(value.get('schema') == 'source-binding/v1' and value.get('binding_id') == identity and
            identity == 'sb-' + digest(canonical(original)), 'Source binding digest mismatch')
    require(len({r['path'] for r in value['files']}) == len(value['files']), 'Duplicate bound source path')
    return value


def read_source(store, manifest, path):
    row = next((r for r in manifest['files'] if r['path'] == source_path(path)), None)
    require(row is not None, 'Source file outside binding')
    raw = blob_path(store, row['sha256']).read_bytes()
    require(digest(raw) == row['sha256'] and len(raw) == row['bytes'], 'Frozen source blob changed')
    return raw


def bind_profile(profile, manifest):
    require(profile.get('product') == manifest['product'] and profile.get('revision') == manifest['revision'],
            'Profile/source identity mismatch')
    value = json.loads(json.dumps(profile))
    value.update(binding_id=manifest['binding_id'], source_id=manifest['source_id'],
                 source_binding_contract='source-binding/v1')
    return value


def compact_evidence(profile, legacy, store, manifest, purposes=None):
    """Convert old quotes only after comparing them to newly bound immutable bytes."""
    require(legacy.get('schema') == 'source-evidence/v1', 'Expected legacy evidence document')
    require(legacy.get('execution') == 'not_run' and legacy.get('field_conclusion') == 'not_assessed',
            'Cannot migrate runtime/field assertions into source-only evidence')
    for key in ('product', 'revision', 'binding_id'):
        require(legacy.get(key) == profile.get(key), 'Legacy profile/evidence mismatch')
    new_profile = bind_profile(profile, manifest)
    rows = []
    for old in legacy['evidence']:
        for key in ('product', 'revision', 'binding_id'):
            require(old.get(key) == profile[key], 'Legacy evidence entry identity mismatch')
        raw = read_source(store, manifest, old['path'])
        quote = excerpt(raw, old['start_line'], old['end_line'])
        require(digest(raw) == old['sha256'] and quote == old.get('quote'), 'Legacy quote/source mismatch')
        row = {k: old[k] for k in ('id', 'path', 'sha256', 'start_line', 'end_line')}
        row.update(product=new_profile['product'], revision=new_profile['revision'],
                   binding_id=new_profile['binding_id'], quote_sha256=digest(quote.encode('utf-8')),
                   purpose=(purposes or {}).get(old['id'], '研究上下文；具体结论及限制见研究记录。'))
        rows.append(row)
    data = {k: new_profile[k] for k in ('product', 'revision', 'binding_id')}
    data.update(schema='source-evidence/v2', execution='not_run', field_conclusion='not_assessed', evidence=rows)
    verify(new_profile, data, store)
    return new_profile, data


def verify(profile, evidence, store):
    require(profile.get('schema') == 'source-product-profile/v1' and profile.get('profile_status') == 'bound',
            'Bound source product profile required')
    require(profile.get('execution_profile') == 'source_only' and profile.get('database_execution') == 'not_run',
            'Only source-only evidence supported')
    require(evidence.get('schema') == 'source-evidence/v2' and evidence.get('execution') == 'not_run' and
            evidence.get('field_conclusion') == 'not_assessed', 'Expected source-evidence/v2 with not_run')
    manifest = binding(store, evidence.get('binding_id'))
    for key in ('product', 'revision', 'binding_id'):
        require(profile.get(key) == evidence.get(key) == manifest.get(key), 'Source identity mismatch: ' + key)
    require(profile.get('source_id') == manifest['source_id'], 'Profile source ID mismatch')
    require(evidence.get('evidence'), 'Nonempty evidence required')
    ids, files, quoted = set(), set(), 0
    for row in evidence['evidence']:
        require(isinstance(row.get('id'), str) and row['id'] and row['id'] not in ids, 'Unique evidence IDs required')
        ids.add(row['id'])
        require('quote' not in row, 'Compact evidence must not embed source quotes')
        for key in ('product', 'revision', 'binding_id'):
            require(row.get(key) == evidence[key], 'Evidence entry identity mismatch')
        require(isinstance(row.get('purpose'), str) and row['purpose'].strip(), 'Evidence purpose required')
        raw = read_source(store, manifest, row['path'])
        require(digest(raw) == row.get('sha256'), 'Evidence file hash mismatch')
        quote = excerpt(raw, row['start_line'], row['end_line'])
        require(digest(quote.encode('utf-8')) == row.get('quote_sha256'), 'Evidence range hash mismatch')
        files.add(row['path'])
        quoted += row['end_line'] - row['start_line'] + 1
    return {'integrity': 'passed', 'evidence_entries': len(ids), 'files_checked': len(files),
            'quoted_lines_on_demand': quoted, 'inline_source_copies': 0,
            'source_provenance': manifest['kind'] + '; local capture, not vendor/binary attestation',
            'semantic_review': 'not_assessed', 'completeness': manifest['completeness'],
            'database_execution': 'not_run', 'field_conclusion': 'not_assessed'}


def show(store, evidence, identity):
    row = next((r for r in evidence['evidence'] if r['id'] == identity), None)
    require(row is not None, 'Unknown evidence ID')
    manifest = binding(store, evidence['binding_id'])
    for key in ('product', 'revision', 'binding_id'):
        require(row.get(key) == evidence.get(key) == manifest.get(key), 'Evidence identity mismatch: ' + key)
    raw = read_source(store, manifest, row['path'])
    text = excerpt(raw, row['start_line'], row['end_line'])
    require(digest(raw) == row['sha256'] and digest(text.encode()) == row['quote_sha256'],
            'Evidence changed')
    return text


def cite(store, binding_id, identity, path, start, end, purpose):
    manifest = binding(store, binding_id)
    raw = read_source(store, manifest, path)
    quote = excerpt(raw, start, end)
    require(identity and purpose, 'Citation ID and purpose required')
    return {'id': identity, **{k: manifest[k] for k in ('product', 'revision', 'binding_id')},
            'path': path, 'sha256': digest(raw), 'start_line': start, 'end_line': end,
            'quote_sha256': digest(quote.encode('utf-8')), 'purpose': purpose}


def evidence_index(evidence, store_relative):
    """Navigation only: source lives in the shared store, not in Markdown code fences."""
    rows = ['# 源码证据索引', '', '仅保存定位和用途；完整源码按需打开。此页不进入常规知识检索。', '',
            '源码绑定：`' + evidence['binding_id'] + '`。', '']
    for item in evidence['evidence']:
        sha = item['sha256']
        relative = store_relative.rstrip('/') + '/objects/sha256/' + sha[:2] + '/' + sha + '.source'
        rows.extend(['<a id="' + item['id'].lower() + '"></a>',
                     '- **' + item['id'] + '** [' + item['path'] + '](' + relative + ')：' +
                     str(item['start_line']) + '–' + str(item['end_line']) + '；' + item['purpose']])
    return '\n'.join(rows) + '\n'


def validate_scope(scope, profile, evidence, ledger, store):
    verify(profile, evidence, store)
    require(scope.get('schema') == 'knowledge-source-scope/v1', 'Unknown knowledge scope')
    for key in ('product', 'revision', 'binding_id', 'source_id'):
        require(scope.get(key) == profile.get(key), 'Knowledge source scope mismatch: ' + key)
    require(scope.get('status') == 'reviewed_conditional', 'Only explicitly reviewed conditional source scope supported')
    review = scope.get('review', {})
    require(review.get('kind') in ('self_reviewed', 'independent_reviewed') and review.get('findings') and
            re.fullmatch(r'\d{4}-\d{2}-\d{2}', review.get('date', '')), 'Actual source review record required')
    require(ledger.get('source_binding') == {k: profile[k] for k in ('product', 'revision', 'binding_id')},
            'Scope/variant source binding mismatch')
    variants = {v['id']: v for v in ledger['variants']}
    require(scope.get('target_build_status') == 'conditional', 'No binary/build attestation from source scope')
    claims, known = scope.get('claims'), {e['id']: e for e in evidence['evidence']}
    require(claims and len({r['id'] for r in claims}) == len(claims), 'Unique nonempty scope claims required')
    manifest = binding(store, profile['binding_id'])
    files = {r['path'] for r in manifest['files']}
    for row in claims:
        require(row.get('text') and row.get('conditions'), 'Claim needs meaning and conditions')
        refs, vids = row.get('evidence_ids', []), row.get('variant_ids', [])
        require(refs and len(refs) == len(set(refs)) and set(refs) <= set(known), 'Unknown/duplicate claim evidence')
        require(vids and len(vids) == len(set(vids)) and set(vids) <= set(variants), 'Unknown/duplicate claim variants')
        deps = row.get('dependency_paths', [])
        require(deps and len(deps) == len(set(deps)) and set(deps) <= files and
                {known[e]['path'] for e in refs} <= set(deps), 'Claim source dependencies incomplete')
        require(row.get('claim_kind') in ('mechanism', 'cause', 'observation', 'recovery', 'build_fact'), 'Unknown claim kind')
        if row['claim_kind'] != 'build_fact':
            require(all(variants[v]['build_status'] == 'supported' for v in vids),
                    'Executable claim cannot apply to unknown/infeasible builds')
    require(scope.get('other_versions_policy') == 'unreviewed_until_rebound', 'No automatic version inheritance')
    return {'scope': 'passed', 'claims': len(claims), 'source_bindings_reviewed': 1,
            'target_build': 'conditional', 'other_versions': 'unreviewed', 'semantic_validation': 'not_performed'}


def assess_changes(store, old_id, new_id, claims):
    old, new = binding(store, old_id), binding(store, new_id)
    for manifest in (old, new):
        for row in manifest['files']:
            read_source(store, manifest, row['path'])
    maps = [{r['path']: r['sha256'] for r in m['files']} for m in (old, new)]
    changed = sorted(p for p in maps[0].keys() & maps[1].keys() if maps[0][p] != maps[1][p])
    added, removed = sorted(maps[1].keys() - maps[0].keys()), sorted(maps[0].keys() - maps[1].keys())
    result = []
    for claim in claims:
        deps = set(claim.get('dependency_paths', []))
        require(deps and deps <= set(maps[0]), 'Old claim dependencies must be captured')
        impact = sorted(deps & (set(changed) | set(removed)))
        same_product = old['product'] == new['product'] and old['repository_id'] == new['repository_id']
        result.append({'id': claim['id'], 'status': 'requires_review' if impact or not same_product else 'candidate_unchanged',
                       'impacted_paths': impact, 'applicability': 'unreviewed'})
    return {'old_binding': old_id, 'new_binding': new_id, 'changed_files': changed,
            'added_to_capture': added, 'missing_from_new_capture': removed, 'claims': result,
            'notice': 'Selected-file diff only; missing means not captured, not proven deleted. New or unlisted callers, '
                      'macros, configuration and build context still require review. No automatic applicability transfer.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('bind-git', 'bind-snapshot'):
        cmd = sub.add_parser(name)
        for arg in ('store', 'source', 'revision', 'product', 'repository-id', 'paths'):
            cmd.add_argument('--' + arg, required=True)
        if name == 'bind-snapshot':
            cmd.add_argument('--patches')
    for name in ('verify', 'show', 'scope', 'index'):
        cmd = sub.add_parser(name)
        cmd.add_argument('--store', required=True)
        cmd.add_argument('--evidence', required=True)
        if name in ('verify', 'scope', 'index'):
            cmd.add_argument('--profile', required=True)
        if name == 'show': cmd.add_argument('--id', required=True)
        if name == 'scope':
            cmd.add_argument('--scope', required=True)
            cmd.add_argument('--ledger', required=True)
        if name == 'index':
            cmd.add_argument('--output', required=True)
            cmd.add_argument('--store-link', required=True)
    cmd = sub.add_parser('compare')
    for arg in ('store', 'old', 'new', 'scope'): cmd.add_argument('--' + arg, required=True)
    cmd = sub.add_parser('profile')
    for arg in ('store', 'binding', 'profile', 'output'): cmd.add_argument('--' + arg, required=True)
    cmd = sub.add_parser('cite')
    for arg in ('store', 'binding', 'id', 'path', 'purpose'): cmd.add_argument('--' + arg, required=True)
    for arg in ('start', 'end'): cmd.add_argument('--' + arg, type=int, required=True)
    args = parser.parse_args()
    try:
        if args.command.startswith('bind-'):
            paths = load(args.paths)
            if args.command == 'bind-git':
                result = capture_git(args.store, args.source, args.revision, args.product, args.repository_id, paths)
            else:
                result = capture_snapshot(args.store, args.source, args.revision, args.product, args.repository_id,
                                          paths, load(args.patches) if args.patches else None)
        elif args.command == 'profile':
            result = bind_profile(load(args.profile), binding(args.store, args.binding))
            save_new(args.output, canonical(result) + b'\n')
        elif args.command == 'cite':
            result = cite(args.store, args.binding, args.id, args.path, args.start, args.end, args.purpose)
        elif args.command == 'show':
            print(show(args.store, load(args.evidence), args.id))
            return 0
        elif args.command == 'compare':
            result = assess_changes(args.store, args.old, args.new, load(args.scope)['claims'])
        else:
            profile, data = load(args.profile), load(args.evidence)
            result = verify(profile, data, args.store)
            if args.command == 'scope':
                result = validate_scope(load(args.scope), profile, data, load(args.ledger), args.store)
            if args.command == 'index':
                save_new(args.output, evidence_index(data, args.store_link).encode('utf-8'))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, UnicodeError, subprocess.CalledProcessError) as exc:
        print(json.dumps({'status': 'failed', 'reason': str(exc) if type(exc) is ValueError else type(exc).__name__}))
        return 1


if __name__ == '__main__':
    sys.exit(main())
