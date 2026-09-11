#!/usr/bin/env bash
# 把 zh/ 下全部 skill 平铺安装到各 agent 的 skills 目录,并清理历史遗留的旧 skill 名。
# 兼容 bash 3.2(macOS 自带),不使用 readarray / 关联数组 / globstar。
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
dry_run=0

usage() {
  cat <<'USAGE'
Usage:
  ./install.sh zh [--dry-run] [target_dir ...]

把本仓库 zh/ 下的全部 skill(按目录名平铺)复制到目标 skills 目录,并清理
deprecated 列表中的旧 skill 名。语言参数必填且只接受 zh。

  zh   source is zh/

en 已冻结:modular-programming v1 套件(en + zh)只读存放在 legacy/
(git tag modular-v1-frozen),不参与安装。

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
  echo "Missing required <lang> (zh)." >&2
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

# 发现 skill:凡含 SKILL.md 的目录即一个 skill,取其目录名。
skills=()
while IFS= read -r -d '' skill_file; do
  skills+=("$(dirname "$skill_file")")
done < <(find "$src_dir" -name SKILL.md -type f -print0)

if ((${#skills[@]} == 0)); then
  echo "No skills found in $src_dir" >&2
  exit 1
fi

# 排序(while read 而非 readarray:兼容 bash 3.2);数组下标顺序决定安装顺序。
sorted_skills=()
while IFS= read -r skill; do
  sorted_skills+=("$skill")
done < <(printf '%s\n' "${skills[@]}" | LC_ALL=C sort)
skills=("${sorted_skills[@]}")

# 本仓库历史版本产出过的 skill 名,安装时从目标目录清除。
# 分组仅作注释,匹配是精确目录名。
deprecated_skills=(
  # v1 治理套件(modular-programming,已冻结入 legacy/)
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
  # v1 之前的 PM / 架构 / 记忆套件
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
  project-management-docs
  # 已被 git-commit 取代的 AI 署名 skill
  auto-ai-coauthor
)

rsync_flags=(-a --delete)
if ((dry_run)); then
  rsync_flags+=(--dry-run --itemize-changes)
  echo "Dry run: no files will be changed."
fi

echo "Found ${#skills[@]} skill(s) in $src_dir:"
for skill in "${skills[@]}"; do
  echo "  $(basename "$skill")"
done

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
        echo "  would remove deprecated $deprecated_skill"
      else
        echo "  removed deprecated $deprecated_skill"
        rm -rf "$deprecated_destination"
      fi
    fi
  done
done

if ((dry_run)); then
  echo "Dry run: would install ${#skills[@]} skill(s) to ${#targets[@]} target(s)."
else
  echo "Installed ${#skills[@]} skill(s) to ${#targets[@]} target(s)."
fi
