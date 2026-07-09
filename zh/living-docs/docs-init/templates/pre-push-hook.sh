#!/usr/bin/env bash
# living-docs 同步门(docs-init 安装到 .git/hooks/pre-push)。
# 阻止"代码动了、文档没动"的变更进入受管分支;受管分支列表读
# main-design.md frontmatter 的 sync_branches(默认 main)。
# 跳过出口:commit message 加 "Arch-Sync: skip <module> <理由>"。

ARCH_DIR="architecture"   # docs-init 按项目实际路径改写
CHECK="CHECK_SYNC_PATH"   # docs-init 按 check_sync.py 实际路径改写

zero=0000000000000000000000000000000000000000
while read -r local_ref local_sha remote_ref remote_sha; do
  branch="${remote_ref#refs/heads/}"
  [ "$local_sha" = "$zero" ] && continue    # 删除远程分支,无内容可查
  [ "$remote_sha" = "$zero" ] && continue   # 新建远程分支,不受管(受管分支应已存在)
  python3 "$CHECK" --arch-dir "$ARCH_DIR" --branch "$branch" \
    --range "$remote_sha..$local_sha" || exit 1
done
exit 0
