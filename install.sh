#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
dry_run=0

usage() {
  cat <<'USAGE'
Usage:
  ./install.sh <lang> [--dry-run] [target_dir ...]

Installs one language edition of the skills in this repo (the
modular-programming suite plus any standalone skills) into one or more agent
skills directories. The first positional argument selects the language and is
required:

  <lang>   zh | en   (source is <lang>/)

Legacy project-memory and architecture-design skill names are removed from the
targets. The installer also copies <lang>/modular-programming/_shared to each
target as _shared so installed modular-* skills can read ../_shared resources.

Default targets:
  ~/.agents/skills
  ~/.codex/skills
  ~/.claude/skills

Examples:
  ./install.sh en
  ./install.sh zh --dry-run
  ./install.sh en ~/.codex/skills ~/.claude/skills ~/my-agent/skills
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
  zh|en) ;;
  *)
    echo "Invalid <lang>: $lang (expected zh|en)." >&2
    usage >&2
    exit 2
    ;;
esac

src_dir="$repo_dir/$lang"
shared_dir="$src_dir/modular-programming/_shared"

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
