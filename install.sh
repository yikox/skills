#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
dry_run=0

usage() {
  cat <<'USAGE'
Usage:
  ./install.sh [--dry-run] [target_dir ...]

Installs every skill directory in this repository into one or more agent
skills directories. A repository child directory is treated as a skill when it
contains SKILL.md.

Default targets:
  ~/.codex/skills
  ~/.claude/skills
  ~/codex/skills
  ~/claude/skills

Examples:
  ./install.sh
  ./install.sh --dry-run
  ./install.sh ~/.codex/skills ~/.claude/skills ~/my-agent/skills
USAGE
}

targets=()
while (($#)); do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --dry-run)
      dry_run=1
      shift
      ;;
    --)
      shift
      while (($#)); do
        targets+=("$1")
        shift
      done
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      targets+=("$1")
      shift
      ;;
  esac
done

if ((${#targets[@]} == 0)); then
  targets=(
    "$HOME/.codex/skills"
    "$HOME/.claude/skills"
    "$HOME/codex/skills"
    "$HOME/claude/skills"
  )
fi

skills=()
for entry in "$repo_dir"/*; do
  if [[ -d "$entry" && -f "$entry/SKILL.md" ]]; then
    skills+=("$entry")
  fi
done

if ((${#skills[@]} == 0)); then
  echo "No skills found in $repo_dir" >&2
  exit 1
fi

rsync_flags=(-a --delete)
if ((dry_run)); then
  rsync_flags+=(--dry-run --itemize-changes)
  echo "Dry run: no files will be changed."
fi

for target in "${targets[@]}"; do
  expanded_target="${target/#\~/$HOME}"

  if ((dry_run)); then
    echo "Would install to: $expanded_target"
  else
    mkdir -p "$expanded_target"
    echo "Installing to: $expanded_target"
  fi

  for skill in "${skills[@]}"; do
    skill_name="$(basename "$skill")"
    destination="$expanded_target/$skill_name"

    if ((dry_run)); then
      echo "  $skill_name -> $destination"
    else
      mkdir -p "$destination"
    fi

    rsync "${rsync_flags[@]}" "$skill/" "$destination/"
  done
done

echo "Installed ${#skills[@]} skill(s) to ${#targets[@]} target(s)."
