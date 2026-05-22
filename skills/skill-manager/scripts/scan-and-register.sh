#!/usr/bin/env bash
# Scan skills/ directory and register all skills directly via Python modules
# Usage: ./scan-and-register.sh [skills-dir]

set -euo pipefail

BASE_DIR="${1:-skills}"

if [ ! -d "$BASE_DIR" ]; then
  echo "Error: directory $BASE_DIR not found"
  echo "Usage: $0 [skills-dir]"
  exit 1
fi

echo "Scanning $BASE_DIR for skills..."

python -c "
from pathlib import Path
from skill_library.registry.scanner import scan_skills
from skill_library.registry.parser import parse_skill_md
from skill_library.state.manager import StateManager
import sys

sm = StateManager('state.json')
state = sm.load()
skills = scan_skills('$BASE_DIR')
registered = 0

for s in skills:
    try:
        meta = parse_skill_md(s)
        name = meta['name']
        if not name:
            print(f'  SKIP {s.name}: empty name', file=sys.stderr)
            continue
        pack_name = s.parent.name
        state.setdefault('skills', {})[name] = {
            'name': name,
            'path': str(s),
            'pack': pack_name,
            'version': meta.get('version', '0.0.0'),
            'mount-status': 'unmounted',
            'quality-status': 'unchecked',
        }
        print(f'  Registered [{pack_name}] {name} v{meta.get(\"version\", \"0.0.0\")}')
        registered += 1
    except Exception as e:
        print(f'  SKIP {s.name}: {e}', file=sys.stderr)

sm.save(state)
print(f'\nDone. {registered} skills registered.')
"
