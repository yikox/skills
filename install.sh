#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
dry_run=0

usage() {
  cat <<'USAGE'
Usage:
  ./install.sh <lang> [--dry-run] [target_dir ...]

Installs one language edition of the skills in this repo into one or more
agent skills directories. The first positional argument selects the language
and is required:

  <lang>   zh   (source is <lang>/)

en is frozen: the modular-programming v1 suite (en + zh) lives read-only in
legacy/ (git tag modular-v1-frozen) and is not installed. Deprecated skill
names, including the frozen modular-* suite and its _shared layer, are removed
from the targets.

Default targets:
  ~/.agents/skills
  ~/.codex/skills
  ~/.claude/skills

Examples:
  ./install.sh zh
  ./install.sh zh --dry-run
  ./install.sh zh ~/.codex/skills ~/.claude/skills ~/my-agent/skills
USAGE
}

positional=()
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
        positional+=("$1")
        shift
      done
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      positional+=("$1")
      shift
      ;;
  esac
done

if ((${#positional[@]} == 0)); then
  echo "Missing required <lang> (zh|en)." >&2
  usage >&2
  exit 2
fi

lang="${positional[0]}"
case "$lang" in
  zh) ;;
  en)
    echo "en edition is frozen: see legacy/ (git tag modular-v1-frozen)." >&2
    exit 2
    ;;
  *)
    echo "Invalid <lang>: $lang (expected zh)." >&2
    usage >&2
    exit 2
    ;;
esac

src_dir="$repo_dir/$lang"

if [[ ! -d "$src_dir" ]]; then
  echo "Source not found: $src_dir" >&2
  exit 1
fi

targets=("${positional[@]:1}")
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
  find "$src_dir" -name SKILL.md -type f -print0
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
  modular-init
  modular-architecture
  modular-change
  modular-autopilot
  modular-advisor
  modular-narrator
  modular-status
  modular-review
  modular-audit
  modular-knowledge
  _shared
)

if ((${#skills[@]} == 0)); then
  echo "No skills found in $src_dir" >&2
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
