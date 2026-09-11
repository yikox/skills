#!/usr/bin/env bash
# living-docs 同步门(docs-init 安装到 .git/hooks/pre-push)。
#
# 与本目录的 living-docs-check-sync.py 配套安装:hook 靠自身所在目录定位检查
# 脚本,因此不依赖用户机器上的 skill 安装位置。阻止"代码动了、文档没动"的
# 变更进入受管分支;受管分支列表读 main-design.md frontmatter 的
# sync_branches(默认 main)。
#
# 跳过出口:commit message 加一行 "Arch-Sync: skip <module> <理由>"。

ARCH_DIR="architecture"   # docs-init 按项目实际路径改写

hook_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
check="$hook_dir/living-docs-check-sync.py"

# 门是事后归纳工具,不是安全边界:环境缺失时警告并放行,不阻断 push。
if ! command -v python3 >/dev/null 2>&1; then
  echo "living-docs 同步门: 未找到 python3,本次跳过检查。" >&2
  exit 0
fi
if [ ! -f "$check" ]; then
  echo "living-docs 同步门: 缺少 $check,本次跳过检查。" >&2
  exit 0
fi

zero=0000000000000000000000000000000000000000
status=0
while read -r local_ref local_sha remote_ref remote_sha; do
  branch="${remote_ref#refs/heads/}"
  [ "$local_sha" = "$zero" ] && continue    # 删除远程分支,无内容可查
  [ "$remote_sha" = "$zero" ] && continue   # 新建远程分支,不受管(受管分支应已存在)
  python3 "$check" --arch-dir "$ARCH_DIR" --branch "$branch" \
    --range "$remote_sha..$local_sha" || status=1
done
exit "$status"
