#!/usr/bin/env bash
# Scan skills/ directory and register all skills
# Usage: ./scan-and-register.sh [pack-dir]

set -euo pipefail

BASE_DIR="${1:-skills}"

if [ ! -d "$BASE_DIR" ]; then
  echo "Error: directory $BASE_DIR not found"
  echo "Usage: $0 [pack-dir]"
  exit 1
fi

echo "Scanning $BASE_DIR for skills..."

find "$BASE_DIR" -name "SKILL.md" | while read -r skill_file; do
  skill_dir=$(dirname "$skill_file")
  skill_name=$(basename "$skill_dir")
  pack_name=$(basename "$(dirname "$skill_dir")")

  echo "  Registering [$pack_name] $skill_name..."
  skill-manager register "$skill_dir" 2>/dev/null || true
done

echo "Done. Run 'skill-manager list' to see registered skills."
