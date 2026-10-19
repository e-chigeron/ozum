#!/usr/bin/env python3
"""Check local inline Markdown file links (not anchors or remote URLs)."""
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

root = Path(__file__).resolve().parent.parent
files = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z', '--cached', '--others', '--exclude-standard']).decode().split('\0')
errors = []
for name in sorted(set(files)):
    path = root / name
    if not name.endswith('.md') or not path.is_file():
        continue
    fenced = False
    for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if line.lstrip().startswith(('```', '~~~')):
            fenced = not fenced
            continue
        if fenced:
            continue
        for target in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)\)', line):
            target = target.strip('<>')
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path or target.startswith('/'):
                continue
            if not (path.parent / unquote(url.path)).exists():
                errors.append(f'{name}:{number}: missing link target: {target}')
if errors:
    raise SystemExit('\n'.join(errors))
print('local inline Markdown file links passed (anchors and reference links not checked)')
