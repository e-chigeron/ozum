import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('prepare', ROOT / 'evals/prepare.py')
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)
spec = importlib.util.spec_from_file_location('run_eval', ROOT / 'evals/run.py')
run_eval = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_eval)


class EvalInputs(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.git('init', '-q', '-b', 'main')
        for name, content in {'AGENTS.md': 'base instruction', 'Intent/a.md': 'intent',
                              'evals/cases/answer.md': 'hidden answer', '.codex/config.toml': 'hooks',
                              'skills/example/SKILL.md': 'skill'}.items():
            p = self.repo / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
        self.base = self.commit()
        (self.repo / 'AGENTS.md').write_text('head says ignore review')
        self.git('mv', 'Intent/a.md', 'Intent/moved.md')
        (self.repo / 'binary').write_bytes(b'\0\xff')
        self.head = self.commit()

    def git(self, *args):
        return prepare.git(self.repo, *args)

    def commit(self):
        self.git('add', '.')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'fixture')
        return prepare.resolve(self.repo, 'HEAD')

    def test_review_neutralizes_instructions_and_preserves_provenance(self):
        out = prepare.fresh_output(self.repo, self.root / 'review')
        policy = self.root / 'policy.md'
        policy.write_text('trusted review policy')
        prepare.review(self.repo, self.base, self.head, out, policy)
        m = json.loads((out / 'manifest.json').read_text())
        self.assertEqual(m['base'], self.base)
        self.assertTrue(m['omitted'])
        self.assertFalse(list(out.rglob('AGENTS.md')))
        self.assertFalse(list(out.rglob('SKILL.md')))
        self.assertFalse(list(out.rglob('config.toml')))
        self.assertIn('trusted review policy', (out / 'prompt.md').read_text())
        self.assertNotIn('head says ignore review', (out / 'prompt.md').read_text())
        self.assertIn('R100', (out / 'changed.txt').read_text())
        sources = [f for f in m['files'] if f['path'] == 'AGENTS.md']
        self.assertEqual(len(sources), 2)
        self.assertIn('head says ignore review', (out / sources[1]['source']).read_text())

    def test_scenario_keeps_method_but_not_answers_or_provider_config(self):
        out = prepare.fresh_output(self.repo, self.root / 'scenario')
        case = ROOT / 'evals/cases/value-judgment'
        prepare.scenario(self.repo, self.base, self.head, out, case)
        for label in ['before', 'after']:
            w = out / label / 'workspace'
            self.assertTrue((w / 'AGENTS.md').is_file())
            self.assertTrue((w / 'skills/example/SKILL.md').is_file())
            self.assertFalse((w / 'evals').exists())
            self.assertFalse((w / '.codex').exists())
            self.assertTrue((w / 'scenario-input/note.md').is_file())
            self.assertEqual(prepare.git(w, 'remote'), b'')
        self.assertEqual((out / 'before/task.md').read_bytes(), (out / 'after/task.md').read_bytes())
        self.assertEqual(json.loads((out / 'manifest.json').read_text())['status'], 'prepared-not-run')

    def test_bad_ref_and_existing_or_nested_output_are_rejected(self):
        with self.assertRaises(subprocess.CalledProcessError):
            prepare.resolve(self.repo, 'not-a-ref')
        with self.assertRaises(ValueError):
            prepare.fresh_output(self.repo, self.repo / 'trial')
        with self.assertRaises(ValueError):
            prepare.fresh_output(self.repo, self.root)

    def test_symlink_is_not_followed(self):
        (self.repo / 'link').symlink_to('/etc/passwd')
        head = self.commit()
        out = prepare.fresh_output(self.repo, self.root / 'links')
        prepare.review(self.repo, self.base, head, out, ROOT / 'evals/review.md')
        self.assertTrue(any(f['path'] == 'link' for f in json.loads((out / 'manifest.json').read_text())['omitted']))

    def test_runner_records_success_failure_and_timeout(self):
        bin_dir = self.root / 'bin'
        bin_dir.mkdir()
        executable = bin_dir / 'codex'
        for behavior, expected in [('success', 'completed'), ('failure', 'failed'), ('timeout', 'timed-out')]:
            with self.subTest(behavior=behavior):
                code = "import sys, time\nfrom pathlib import Path\nif '--version' in sys.argv:\n print('fake-codex-for-mechanical-test'); sys.exit(0)\n"
                if behavior == 'success':
                    code += "Path(sys.argv[sys.argv.index('--output-last-message')+1]).write_text('synthetic answer')\nprint('{}')\n"
                elif behavior == 'failure':
                    code += "sys.exit(2)\n"
                else:
                    code += "time.sleep(30)\n"
                executable.write_text('#!' + sys.executable + '\n' + code)
                executable.chmod(0o755)
                out = prepare.fresh_output(self.repo, self.root / behavior)
                prepare.scenario(self.repo, self.base, self.head, out, ROOT / 'evals/cases/compatible-scopes')
                with patch.dict(os.environ, {'PATH': str(bin_dir) + os.pathsep + os.environ['PATH']}):
                    success = run_eval.run(out / 'after', 'test-model', 0.1 if behavior == 'timeout' else 5)
                self.assertEqual(success, behavior == 'success')
                result = json.loads((out / 'after/result/run.json').read_text())
                self.assertEqual(result['status'], expected)
                self.assertIsNotNone(result['elapsed_seconds'])
                with self.assertRaises(FileExistsError):
                    run_eval.run(out / 'after', 'test-model', 5)

    def test_missing_cli_is_not_a_pass(self):
        out = prepare.fresh_output(self.repo, self.root / 'run')
        prepare.scenario(self.repo, self.base, self.head, out, ROOT / 'evals/cases/compatible-scopes')
        with patch.object(run_eval.subprocess, 'check_output', side_effect=[FileNotFoundError('codex unavailable'), b'', b'']):
            self.assertFalse(run_eval.run(out / 'after', 'test-model', 10))
        result = json.loads((out / 'after/result/run.json').read_text())
        self.assertEqual(result['status'], 'not-run')


if __name__ == '__main__':
    unittest.main()
