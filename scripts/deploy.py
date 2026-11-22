#!/usr/bin/env python3
"""Install language-scoped artifacts and track ownership by content digest."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
LANG = 'rust' if (ROOT / 'skills/rust-guidelines').exists() else 'ts'
TARGETS = {'antigravity': '.agents', 'opencode': '.opencode', 'kilocode': '.kilo',
           'cursor': '.cursor', 'claude': '.claude', 'copilot': '.github'}


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def scoped(text, cursor=False):
    # Flat filenames preserve native rule discovery while avoiding language collisions.
    for rule in (ROOT / 'rules').glob('*.md'):
        name = f'{LANG}--{rule.stem}' + ('.mdc' if cursor else '.md')
        text = text.replace(f'rules/{rule.name}', f'rules/{name}')
        text = text.replace(f']({rule.name})', f']({name})')
    text = text.replace('rules/<rule-id>.md', f'rules/{LANG}--<rule-id>.md')
    return text


def render_rule(name, body, target, legacy=False):
    if not legacy:
        body = scoped(body, target == 'cursor')
    if target != 'cursor':
        return body
    desc = next((line[1:].strip() for line in body.splitlines() if line.startswith('>')), name)
    globs = '**/*.rs, **/Cargo.toml' if LANG == 'rust' else '**/*.ts, **/*.tsx, **/tsconfig*.json'
    if LANG == 'ts' and not legacy:
        globs += ', **/*.vue'
    description = desc if legacy else json.dumps(desc)
    return f'---\ndescription: {description}\nglobs: {json.dumps(globs)}\nalwaysApply: false\n---\n\n' + body


def artifacts(target):
    folder = TARGETS[target]
    files = {}
    if target != 'copilot':
        for rule in (ROOT / 'rules').glob('*.md'):
            suffix = '.mdc' if target == 'cursor' else '.md'
            files[f'{folder}/rules/{LANG}--{rule.stem}{suffix}'] = render_rule(rule.stem, rule.read_text(), target)
        for category in ('skills', 'agents'):
            for path in (ROOT / category).rglob('*'):
                if path.is_file():
                    files[f'{folder}/{path.relative_to(ROOT)}'] = scoped(path.read_text(), target == 'cursor')
    blocks = {}
    if target in ('antigravity', 'opencode', 'kilocode'):
        blocks[f'{folder}/AGENTS.md'] = scoped((ROOT / f'targets/{target}/AGENTS.md').read_text())
    elif target == 'claude':
        blocks['CLAUDE.md'] = scoped((ROOT / 'targets/claude/CLAUDE.md').read_text())
    elif target == 'copilot':
        blocks['.github/copilot-instructions.md'] = (ROOT / 'targets/copilot/copilot-instructions.md').read_text()
    return files, blocks


def checked(dest, relative):
    path = dest / relative
    if path.is_symlink() or not path.resolve().is_relative_to(dest):
        raise ValueError(f'Refusing symlink or path outside destination: {path}')
    return path


def block_pattern():
    return re.compile(rf'<!-- BEGIN {LANG}-ai-guidelines v1 -->\n.*?<!-- END {LANG}-ai-guidelines -->\n', re.S)


def wrapped(body):
    return f'<!-- BEGIN {LANG}-ai-guidelines v1 -->\n{body.rstrip()}\n<!-- END {LANG}-ai-guidelines -->\n'


def legacy_catalog():
    path = ROOT / f'scripts/legacy-{LANG}-v1.json'
    return json.loads(path.read_text()) if path.exists() else {}


def legacy_versions(body):
    return {body, scoped(body), scoped(body, cursor=True)}


def run(target, dest, clean=False):
    dest = dest.resolve()
    manifest = checked(dest, f'{TARGETS[target]}/.guidelines-{LANG}.json')
    state = json.loads(manifest.read_text()) if manifest.exists() else {'files': {}, 'blocks': {}}
    files, blocks = artifacts(target)
    history = legacy_catalog()
    changes = {}
    next_state = {'files': {}, 'blocks': {}}
    if clean:
        # Only delete bytes recorded by this installer; edited files remain user-owned.
        for relative, expected in state['files'].items():
            path = checked(dest, relative)
            if path.exists() and digest(path.read_text()) == expected:
                changes[relative] = None
        for relative, expected in state['blocks'].items():
            path = checked(dest, relative)
            if path.exists():
                text = path.read_text()
                match = block_pattern().search(text)
                if match and digest(match.group()) == expected:
                    remaining = text[:match.start()] + text[match.end():]
                    changes[relative] = remaining if remaining.strip() else None
        if not manifest.exists():
            print(f'{target}: no ownership manifest; legacy/user files preserved')
            return
    else:
        # Preflight every conflict before changing any installed file.
        for relative, body in files.items():
            path = checked(dest, relative)
            if path.exists():
                current = path.read_text()
                original = ROOT / relative.split('/', 1)[1]
                legacy = original.is_file() and current == original.read_text()
                category, _, item = relative.split('/', 1)[1].partition('/')
                key = item if category == 'skills' else Path(item).stem.removeprefix(f'{LANG}--')
                previous = history.get(category, {}).get(key)
                if previous is not None:
                    versions = ({render_rule(key, previous, target)} if category == 'rules'
                                else legacy_versions(previous))
                    legacy = legacy or current in versions
                if current != body and digest(current) != state['files'].get(relative) and not legacy:
                    raise ValueError(f'Preserved modified/unmanaged file: {path}')
            changes[relative] = body
            next_state['files'][relative] = digest(body)
        for relative, body in blocks.items():
            path = checked(dest, relative)
            text = path.read_text() if path.exists() else ''
            new = wrapped(body)
            matches = list(block_pattern().finditer(text))
            if len(matches) > 1:
                raise ValueError(f'Duplicate managed blocks: {path}')
            if matches:
                match = matches[0]
                if match.group() != new and digest(match.group()) != state['blocks'].get(relative):
                    raise ValueError(f'Preserved modified/unmanaged instruction block: {path}')
                text = text[:match.start()] + new + text[match.end():]
            else:
                # Migrate only an exact legacy template; never guess ownership by title.
                template = ROOT / f'targets/{target}/' / ('CLAUDE.md' if target == 'claude' else 'copilot-instructions.md' if target == 'copilot' else 'AGENTS.md')
                candidates = [template.read_text()]
                previous = history.get('instructions', {}).get(target)
                if previous:
                    candidates.extend(sorted(legacy_versions(previous), key=len, reverse=True))
                old = next((candidate for candidate in candidates if candidate in text), None)
                if old is not None:
                    text = text.replace(old, new, 1)
                else:
                    text += ('\n' if text and not text.endswith('\n') else '') + new
            changes[relative] = text
            next_state['blocks'][relative] = digest(new)
        for relative, expected in state['files'].items():
            path = checked(dest, relative)
            if relative not in files and path.exists() and digest(path.read_text()) == expected:
                changes[relative] = None
        # Historical personas are data, never discoverable active agents. Match contents,
        # not just names, so retired custom personas and other languages survive updates.
        if target != 'copilot':
            active = {path.stem for path in (ROOT / 'agents').glob('*.md')}
            for name, old_body in history.get('agents', {}).items():
                if name in active:
                    continue
                relative = f'{TARGETS[target]}/agents/{name}.md'
                path = checked(dest, relative)
                if path.exists():
                    if path.read_text() in legacy_versions(old_body):
                        changes[relative] = None
                    elif changes.get(relative, 'preserved') is not None:
                        print(f'Preserved customized retired agent; review manually: {path}')
        # Retire exact, unchanged pre-manifest rules. Unknown historical files stay intact.
        if target != 'copilot':
            for rule in (ROOT / 'rules').glob('*.md'):
                suffix = '.mdc' if target == 'cursor' else '.md'
                relative = f'{TARGETS[target]}/rules/{rule.stem}{suffix}'
                path = checked(dest, relative)
                candidates = {render_rule(rule.stem, rule.read_text(), target, legacy=True)}
                previous = history.get('rules', {}).get(rule.stem)
                if previous:
                    candidates.add(render_rule(rule.stem, previous, target, legacy=True))
                if path.exists() and path.read_text() in candidates:
                    changes[relative] = None
    if not clean and target == 'kilocode':
        config = checked(dest, 'kilo.jsonc')
        if not config.exists():
            # Shared project configuration stays user-owned, including after clean.
            changes['kilo.jsonc'] = (ROOT / 'targets/kilocode/kilo.jsonc').read_text()
    for relative, body in changes.items():
        path = checked(dest, relative)
        if body is None:
            path.unlink(missing_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body)
    if clean:
        manifest.unlink()
        # Remove only empty directories under the integration root.
        root = dest / TARGETS[target]
        for path in sorted(root.rglob('*'), key=lambda p: len(p.parts), reverse=True):
            if path.is_dir() and not path.is_symlink():
                try:
                    path.rmdir()
                except OSError:
                    pass
        try:
            root.rmdir()
        except OSError:
            pass
    else:
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps(next_state, indent=2) + '\n')
    print(f'{LANG}: {target} {"cleaned" if clean else "installed"}; user-owned content preserved')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['install', 'clean'])
    parser.add_argument('target', choices=[*TARGETS, 'all'])
    parser.add_argument('destination', nargs='?', default='.')
    args = parser.parse_args()
    try:
        for target in TARGETS if args.target == 'all' else [args.target]:
            run(target, Path(args.destination), args.action == 'clean')
    except (OSError, ValueError) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    main()
