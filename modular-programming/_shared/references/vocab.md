# 受控词表（单一事实源）

本文件是 modular 工作流**受控词表的唯一事实源**。audit-checker（`check_modular_project.py`）在启动时解析本文件，用它校验模块 front matter、设计/变更/ADR front matter 与架构图关系；其它规则文档（storage-schema、review-rules、module-authoring-rules、module-kind-classification、architecture-graph-json-format）解释各词的语义，但**枚举值以本文件为准**。

## 解析约定

- 每个二级标题（`## <vocab-name>`，名字见下方映射）定义一张词表。
- 词表标题下方**所有以反引号包裹的 token 都被当作该词表的合法值**——因此在词表小节内，除词表值外不要再用反引号包裹文件名或其它术语（把这类说明放在本小节之外，或不加反引号）。
- 顺序不重要；checker 解析失败或缺少某词表时，回退到脚本内置默认值并告警，不会因本文件问题而全表失效。
- 词表名与 checker 常量的映射：module_form→MODULE_FORMS、module_kind→MODULE_KINDS、relation_kind→RELATION_KINDS、relation_style→RELATION_STYLES、design_status→DESIGN_STATUSES、review_status→REVIEW_STATUSES。
- 各词的语义解释见对应规则文档：module_kind 见 module-kind-classification.md 与 module-kinds/；relation_kind/relation_style 见 architecture-graph-json-format.md；design_status/review_status 见 storage-schema.md。

## module_form

`atomic`、`composite`

## module_kind

`layout-style`、`function-flow`、`interface-object`、`data-state`、`event-message`、`config-rule`、`resource-file`、`adapter-io`、`utility-support`

## relation_kind

`uses`、`reads`、`writes`、`triggers`、`distributes`

## relation_style

`solid`、`dashed`

## design_status

`draft`、`proposed`、`accepted`、`implemented`、`obsolete`

## review_status

`not-reviewed`、`needs-review`、`reviewed`
