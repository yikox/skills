#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
shared_dir="$repo_dir/modular-programming/_shared"
dry_run=0

usage() {
  cat <<'USAGE'
Usage:
  ./install.sh [--dry-run] [target_dir ...]

Installs the current modular-programming skill suite into one or more agent
skills directories. Legacy project-memory and architecture-design skill
names are removed from the targets.

The installer also copies modular-programming/_shared to each target as
_shared so installed modular-* skills can read ../_shared resources.

Default targets:
  ~/.agents/skills
  ~/.codex/skills
  ~/.claude/skills

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
    "$HOME/.agents/skills"
    "$HOME/.codex/skills"
    "$HOME/.claude/skills"
  )
fi

skills=()
while IFS= read -r -d '' skill_file; do
  skills+=("$(dirname "$skill_file")")
done < <(
  find "$repo_dir" \
    -path "$repo_dir/.git" -prune -o \
    -path "$repo_dir/.git/*" -prune -o \
    -name SKILL.md -type f -print0
)

deprecated_skills=(
  architecture-design
  pm-audit-memory
  pm-design-requirement
  pm-document-architecture
  pm-groom-roadmap
  pm-init
  pm-migrate-memory
  pm-record-knowledge
  pm-record-requirement
  pm-review-artifact
  pm-track-status
  notes-project-memory
  project-memory-init
  project-management-memory
  project-knowledge-memory
  pm-architecture-docs
  pm-requirement-to-design
  modular-architect
)

if ((${#skills[@]} == 0)); then
  echo "No skills found in $repo_dir" >&2
  exit 1
fi

IFS=$'\n' skills=($(printf '%s\n' "${skills[@]}" | sort))
unset IFS

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

  shared_destination="$expanded_target/_shared"
  if [[ -d "$shared_dir" ]]; then
    if ((dry_run)); then
      echo "  _shared -> $shared_destination"
    else
      mkdir -p "$shared_destination"
    fi

    rsync "${rsync_flags[@]}" "$shared_dir/" "$shared_destination/"
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

  for deprecated_skill in "${deprecated_skills[@]}"; do
    deprecated_destination="$expanded_target/$deprecated_skill"
    if [[ -e "$deprecated_destination" ]]; then
      if ((dry_run)); then
        echo "  remove deprecated $deprecated_skill -> $deprecated_destination"
      else
        rm -rf "$deprecated_destination"
      fi
    fi
  done
done

echo "Installed ${#skills[@]} skill(s) to ${#targets[@]} target(s)."
