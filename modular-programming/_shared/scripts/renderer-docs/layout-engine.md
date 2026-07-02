---
format: arch-module/v0.1
name: Layout Engine
described: 计算对象坐标、组合框范围和关系端点边界
module_form: atomic
module_kind: function-flow
main_subject: object_positions() + group_bounds()
status: draft
---

# Layout Engine

## 模块定位

Layout Engine 把 Graph Model 中的对象和组合关系转换成 SVG 坐标。

## 当前实现

当前实现位于 `render_modular_graph.py`：

- `object_positions()` 计算节点位置。
- `object_half_size()` 提供节点半尺寸。
- `group_frame_bounds()` / `group_bounds()` 根据 `contains` 计算复合模块的单一完整外框。
- `build_route_endpoints()` 把对象、group 和 group interface 统一成关系路由端点；group interface 复用所属复合模块的完整边界。
- route helpers 计算正交折线路径、端点桩线、避让轨道和 hover 气泡位置。

## 约束

当前布局基于网格坐标、复合模块完整外框和正交关系路由，不解决通用图布局问题。复杂项目需要通过同层关系建模、复合模块接口、显式 `at` 坐标和合理的设计层级控制图的阅读层次；渲染器不拆分复合模块边界，也不把接口渲染成独立小框。
