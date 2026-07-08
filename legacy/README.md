# legacy/ — 契约冻结,只读参考

本目录存放 **modular-programming v1 套件**(en + zh 双语,10 个 skill + 共享层)的最终冻结状态。

- 冻结时点:2026-07-09,对应 git tag `modular-v1-frozen`。
- 契约冻结:本目录内容不再修改、不再修 bug、不再接受需求。
- 不再安装:`install.sh` 不会安装本目录下的任何内容,并会从目标目录清理旧的 `modular-*` skill,避免与新套件抢触发。
- 冻结原因与后继设计见 `PM/skills/architecture/changes/2026-07-09-living-docs-v2-redesign.md`:v1 的事前门禁治理(L0-L3 分级、review、autopilot 等)被诊断为机制体量远超产品本身;v2 回归初心,产品重新定义为两份文档(项目文档 + 设计文档),机制减为三个 skill(init / sync / acceptance),中文单源。

如需取用 v1,直接读本目录或 checkout tag `modular-v1-frozen`。
