---
format: arch-module/v0.1
name: Layout Engine
described: 计算对象坐标、组合框范围和连线起止边界
module_form: atomic
module_kind: function-flow
main_subject: object_positions() + group_bounds()
status: draft
---

# Layout Engine

## 模块定位

Layout Engine 把 Graph Model 中的对象和组合关系转换成 SVG 坐标。

## 当前实现

当前实现位于 `scripts/render_arch_graph.py`：

- `object_positions()` 计算节点位置。
- `object_half_size()` 提供节点半尺寸。
- `group_bounds()` 根据 `contains` 计算组合模块外框。
- `boundary_point()` 计算连线贴近节点边界的位置。

## 约束

当前布局基于网格坐标和简单自动排列，不解决通用图布局问题。复杂项目需要引入层级布局、避让和边关系路由。
