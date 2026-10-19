#!/usr/bin/env python3
"""Run one prepared scenario with an installed, authenticated Codex CLI."""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import time


def run(trial, model, timeout):
    trial = trial.resolve()
    workspace = trial / 'workspace'
    if not (workspace / '.git').is_dir() or not (trial / 'task.md').is_file():
        raise ValueError('expected a prepared before/after trial')
    result = trial / 'result'
    result.mkdir()  # Never mix repeated trials or silently overwrite evidence.
    metadata = {'model': model, 'timeout_seconds': timeout, 'status': 'starting',
                'started_at_unix': time.time(), 'elapsed_seconds': None}
    try:
        metadata['harness'] = subprocess.check_output(['codex', '--version'], text=True).strip()
        command = ['codex', 'exec', '--cd', str(workspace), '--model', model,
                   '--sandbox', 'workspace-write', '--json',
                   '--output-last-message', str(result / 'answer.md'), '-']
        metadata['command'] = command
        start = time.monotonic()
        with (trial / 'task.md').open('rb') as prompt, (result / 'events.jsonl').open('wb') as events, (result / 'stderr.log').open('wb') as errors:
            proc = subprocess.Popen(command, stdin=prompt, stdout=events, stderr=errors, start_new_session=True)
            try:
                code = proc.wait(timeout=timeout)
                metadata['exit_code'] = code
                metadata['status'] = 'completed' if code == 0 and (result / 'answer.md').is_file() else 'failed'
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
                metadata['status'] = 'timed-out'
        metadata['elapsed_seconds'] = time.monotonic() - start
    except OSError as error:
        metadata['status'] = 'not-run'
        metadata['error'] = str(error)
    finally:
        (result / 'run.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    # Preserve the actual final state, including untracked additions, for the evaluator.
    (result / 'changes.patch').write_bytes(subprocess.check_output(['git', '-C', str(workspace), 'diff', 'HEAD', '--']))
    (result / 'status.txt').write_bytes(subprocess.check_output(['git', '-C', str(workspace), 'status', '--short']))
    return metadata['status'] == 'completed'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('trial', type=Path)
    parser.add_argument('--model', required=True)
    parser.add_argument('--timeout', type=int, default=600)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error('timeout must be positive')
    raise SystemExit(0 if run(args.trial, args.model, args.timeout) else 1)
