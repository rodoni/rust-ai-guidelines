#!/usr/bin/env python3
"""Regression coverage for installed artifacts, ownership, and shared destinations."""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('deploy', ROOT / 'scripts/deploy.py')
deploy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deploy)


class DeploymentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dest = Path(self.tmp.name)

    def test_all_targets_links_idempotence_and_clean(self):
        for target, folder in deploy.TARGETS.items():
            with self.subTest(target=target):
                user = self.dest / folder / 'user.txt'
                user.parent.mkdir(parents=True, exist_ok=True)
                user.write_text('custom')
                deploy.run(target, self.dest)
                expected, _ = deploy.artifacts(target)
                for relative, body in expected.items():
                    self.assertEqual((self.dest / relative).read_text(), body)
                before = {str(p): p.read_bytes() for p in self.dest.rglob('*') if p.is_file()}
                deploy.run(target, self.dest)
                self.assertEqual(before, {str(p): p.read_bytes() for p in self.dest.rglob('*') if p.is_file()})
                for p in (self.dest / folder).rglob('*'):
                    if p.suffix not in ('.md', '.mdc'):
                        continue
                    for link in re.findall(r'\]\(([^)]+)\)', p.read_text()):
                        if not link.startswith(('https:', 'http:', '#', 'mailto:')):
                            self.assertTrue((p.parent / link.split('#')[0]).exists(), (p, link))
                if target == 'cursor' and deploy.LANG == 'ts':
                    self.assertIn('**/*.vue', (self.dest / folder / 'rules/ts--vue-composition-api.mdc').read_text())
                deploy.run(target, self.dest, clean=True)
                self.assertEqual(user.read_text(), 'custom')
                self.assertEqual([p for p in (self.dest / folder).rglob('*') if p.is_file()], [user])

    def test_modified_files_preserved_on_update_and_clean(self):
        deploy.run('opencode', self.dest)
        file = self.dest / f'.opencode/rules/{deploy.LANG}--m-app-error.md'
        file.write_text('my customization')
        with self.assertRaises(ValueError):
            deploy.run('opencode', self.dest)
        deploy.run('opencode', self.dest, clean=True)
        self.assertEqual(file.read_text(), 'my customization')

    def test_instruction_update_and_user_content(self):
        path = self.dest / 'CLAUDE.md'
        path.write_text('User preface\n')
        deploy.run('claude', self.dest)
        path.write_text(path.read_text() + 'User epilogue\n')
        original = deploy.artifacts
        def changed(target):
            files, blocks = original(target)
            return files, {name: body + '\nUpdated release\n' for name, body in blocks.items()}
        deploy.artifacts = changed
        try:
            deploy.run('claude', self.dest)
            self.assertIn('Updated release', path.read_text())
            deploy.run('claude', self.dest, clean=True)
            self.assertEqual(path.read_text(), 'User preface\nUser epilogue\n')
        finally:
            deploy.artifacts = original

    def test_modified_instruction_block_preserved(self):
        deploy.run('claude', self.dest)
        path = self.dest / 'CLAUDE.md'
        path.write_text(path.read_text().replace('<!-- END', 'Custom text\n<!-- END'))
        before = path.read_text()
        with self.assertRaises(ValueError):
            deploy.run('claude', self.dest)
        deploy.run('claude', self.dest, clean=True)
        self.assertEqual(path.read_text(), before)

    def test_legacy_and_unmanaged_content(self):
        path = self.dest / 'CLAUDE.md'
        template = (ROOT / 'targets/claude/CLAUDE.md').read_text()
        path.write_text('User notes\n' + template)
        deploy.run('claude', self.dest)
        self.assertEqual(path.read_text().count('<!-- BEGIN'), 1)
        self.assertTrue(path.read_text().startswith('User notes\n'))
        legacy = self.dest / '.opencode/rules/m-app-error.md'
        legacy.parent.mkdir(parents=True)
        legacy.write_text((ROOT / 'rules/m-app-error.md').read_text())
        deploy.run('opencode', self.dest)
        self.assertFalse(legacy.exists())
        other = self.dest / '.cursor/custom.txt'
        other.parent.mkdir()
        other.write_text('legacy')
        deploy.run('cursor', self.dest, clean=True)
        self.assertEqual(other.read_text(), 'legacy')

    def test_legacy_cursor_migration_preserves_edits(self):
        folder = self.dest / '.cursor/rules'
        folder.mkdir(parents=True)
        source = (ROOT / 'rules/m-app-error.md').read_text()
        desc = next(line[1:].strip() for line in source.splitlines() if line.startswith('>'))
        globs = '**/*.rs, **/Cargo.toml' if deploy.LANG == 'rust' else '**/*.ts, **/*.tsx, **/tsconfig*.json'
        legacy = folder / 'm-app-error.mdc'
        legacy.write_text(f'---\ndescription: {desc}\nglobs: "{globs}"\nalwaysApply: false\n---\n\n' + source)
        edited = folder / 'wf-tdd-loop.mdc'
        edited.write_text('user edited legacy rule')
        deploy.run('cursor', self.dest)
        self.assertFalse(legacy.exists())
        self.assertEqual(edited.read_text(), 'user edited legacy rule')

    def test_symlink_destination_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            (self.dest / '.opencode').symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                deploy.run('opencode', self.dest)
            self.assertEqual(list(Path(outside).iterdir()), [])

    def test_release_updates_and_removes_only_unchanged_files(self):
        deploy.run('opencode', self.dest)
        original = deploy.artifacts
        files, _ = original('opencode')
        names = list(files)
        removed, edited, updated = names[:3]
        (self.dest / edited).write_text('custom retired rule')
        def changed(target):
            new_files, blocks = original(target)
            new_files.pop(removed)
            new_files.pop(edited)
            new_files[updated] += '\nNew release\n'
            return new_files, blocks
        deploy.artifacts = changed
        try:
            deploy.run('opencode', self.dest)
            self.assertFalse((self.dest / removed).exists())
            self.assertEqual((self.dest / edited).read_text(), 'custom retired rule')
            self.assertTrue((self.dest / updated).read_text().endswith('New release\n'))
        finally:
            deploy.artifacts = original

    def test_unmanaged_conflict_preflight_and_existing_config(self):
        file = self.dest / f'.opencode/rules/{deploy.LANG}--m-app-error.md'
        file.parent.mkdir(parents=True)
        file.write_text('user-owned')
        with self.assertRaises(ValueError):
            deploy.run('opencode', self.dest)
        self.assertEqual([p for p in self.dest.rglob('*') if p.is_file()], [file])
        config = self.dest / 'kilo.jsonc'
        config.write_text('{"custom": true}')
        deploy.run('kilocode', self.dest)
        deploy.run('kilocode', self.dest, clean=True)
        self.assertEqual(config.read_text(), '{"custom": true}')

    def test_cli_from_another_working_directory(self):
        for args in [('all', str(self.dest)), ('clean', 'all', str(self.dest))]:
            result = subprocess.run(['bash', str(ROOT / 'sync.sh'), *args], cwd=self.dest, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(list(self.dest.rglob('.guidelines-*.json')))

    def test_languages_coexist(self):
        peer = ROOT.parent / ('ts-ai-guidelines' if deploy.LANG == 'rust' else 'rust-ai-guidelines')
        if not (peer / 'scripts/deploy.py').exists():
            self.skipTest('Sibling package unavailable; run workspace integration to cover both languages')
        for target in deploy.TARGETS:
            deploy.run(target, self.dest)
            subprocess.run(['python3', str(peer / 'scripts/deploy.py'), 'install', target, str(self.dest)], check=True, capture_output=True)
            deploy.run(target, self.dest)
            peer_lang = 'ts' if deploy.LANG == 'rust' else 'rust'
            folder = deploy.TARGETS[target]
            peer_manifest = self.dest / folder / f'.guidelines-{peer_lang}.json'
            peer_state = json.loads(peer_manifest.read_text())
            peer_files = {self.dest / name: (self.dest / name).read_bytes() for name in peer_state['files']}
            peer_files[peer_manifest] = peer_manifest.read_bytes()
            if target != 'copilot':
                actual_agents = {p.stem for p in (self.dest / folder / 'agents').glob('*.md')}
                self.assertEqual(actual_agents, {f'{lang}-{role}' for lang in ('ts', 'rust') for role in ('dev', 'reviewer', 'tester')})
            if target != 'copilot':
                self.assertTrue((self.dest / folder / (f'rules/{peer_lang}--m-app-error' + ('.mdc' if target == 'cursor' else '.md'))).exists())
            deploy.run(target, self.dest, clean=True)
            for p, data in peer_files.items():
                self.assertEqual(p.read_bytes(), data)
            if target != 'copilot':
                self.assertEqual({p.stem for p in (self.dest / folder / 'agents').glob('*.md')},
                                 {f'{peer_lang}-{role}' for role in ('dev', 'reviewer', 'tester')})
            for relative, expected_hash in peer_state['blocks'].items():
                text = (self.dest / relative).read_text()
                match = re.search(rf'<!-- BEGIN {peer_lang}-ai-guidelines v1 -->\n.*?<!-- END {peer_lang}-ai-guidelines -->\n', text, re.S)
                self.assertIsNotNone(match)
                self.assertEqual(deploy.digest(match.group()), expected_hash)
            _, blocks = deploy.artifacts(target)
            for relative in blocks:
                self.assertIn(f'<!-- BEGIN {peer_lang}-ai-guidelines', (self.dest / relative).read_text())


if __name__ == '__main__':
    unittest.main()
