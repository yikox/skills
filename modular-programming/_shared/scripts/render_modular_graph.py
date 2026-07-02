#!/usr/bin/env python3
"""Render Architecture Graph JSON files to a self-contained HTML/SVG document."""

from __future__ import annotations

import argparse
import heapq
import html
import json
import math
import os
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple
from urllib.parse import quote


MODULE_KIND_STYLES = {
    "layout-style": ("frame", "#2563eb", "#eff6ff"),
    "function-flow": ("hexagon", "#7c3aed", "#f5f3ff"),
    "interface-object": ("rounded-rect", "#059669", "#ecfdf5"),
    "data-state": ("cylinder", "#d97706", "#fffbeb"),
    "event-message": ("diamond", "#dc2626", "#fef2f2"),
    "config-rule": ("document", "#475569", "#f8fafc"),
    "resource-file": ("folder", "#0891b2", "#ecfeff"),
    "adapter-io": ("port", "#ea580c", "#fff7ed"),
    "utility-support": ("small-rect", "#64748b", "#f8fafc"),
}

NODE_WIDTH = 230
NODE_HEIGHT = 110
NODE_CIRCLE_RADIUS = 66
CELL_WIDTH = 340
CELL_HEIGHT = 240
MARGIN_X = 190
MARGIN_Y = 180
VIEWBOX_PADDING_X = 220
VIEWBOX_PADDING_Y = 180
LABEL_UNIT_WIDTH = 6.2
LABEL_LINE_HEIGHT = 15
LABEL_PADDING_X = 9
LABEL_PADDING_Y = 7
GROUP_MIN_GAP = 32
GROUP_PADDING_X = min(54, max(30, (CELL_WIDTH - NODE_WIDTH - GROUP_MIN_GAP) / 2))
GROUP_PADDING_TOP = 62
GROUP_PADDING_BOTTOM = min(52, max(28, CELL_HEIGHT - NODE_HEIGHT - GROUP_PADDING_TOP - GROUP_MIN_GAP))
ROUTE_TRACK_GAP = 34
ROUTE_OUTER_GAP = 96
ROUTE_ENDPOINT_STUB = 22
ROUTE_ENDPOINT_CLEARANCE_X = max(NODE_WIDTH / 2, NODE_CIRCLE_RADIUS) + ROUTE_ENDPOINT_STUB
ROUTE_ENDPOINT_CLEARANCE_Y = max(NODE_HEIGHT / 2, NODE_CIRCLE_RADIUS) + ROUTE_ENDPOINT_STUB
ROUTE_SEARCH_MAX_EXPANSIONS = 9000
BBox = Tuple[float, float, float, float]
Point = Tuple[float, float]
Segment = Tuple[Point, Point]


@dataclass
class DiagramObject:
    object_id: str
    ref: Optional[Path]
    shape: str
    name: str
    described: str
    at: Optional[Tuple[float, float]]
    stroke: str
    fill: str
    source_meta: Dict[str, str]


@dataclass
class Relation:
    source: str
    target: str
    described: str
    style: str
    label_offset: Tuple[float, float]


@dataclass
class GroupInterface:
    interface_id: str
    name: str
    described: str
    provided_by: List[str]


@dataclass
class DiagramGroup:
    group_id: str
    ref: Optional[Path]
    name: str
    described: str
    contains: List[str]
    interfaces: List[GroupInterface]
    at: Optional[Tuple[float, float]]
    source_meta: Dict[str, str]


@dataclass
class Diagram:
    path: Path
    meta: Dict[str, str]
    objects: List[DiagramObject]
    groups: List[DiagramGroup]
    relations: List[Relation]
    warnings: List[str]


@dataclass
class RoutedRelation:
    relation: Relation
    points: List[Point]
    bubble_lines: List[str]
    bubble_x: float
    bubble_y: float
    bubble_box: BBox
    dash: str
    layer: str


@dataclass
class RouteEndpoint:
    endpoint_id: str
    kind: str
    center: Point
    box: BBox
    scope: Optional[str]
    owner_object_ids: Set[str]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_key_values(text: str) -> Dict[str, str]:
    values: Dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        values[key.strip()] = value
    return values


def parse_front_matter(text: str) -> Tuple[Dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            front_matter = "\n".join(lines[1:index])
            body = "\n".join(lines[index + 1 :])
            return parse_key_values(front_matter), body

    return {}, text


def load_document_meta(
    path: Path,
    warnings: List[str],
    inline_fields: frozenset = frozenset(),
) -> Dict[str, str]:
    if not path.exists():
        warnings.append(f"引用文件不存在: {path}")
        return {"name": path.stem, "described": ""}

    meta, _ = parse_front_matter(read_text(path))
    if "name" not in meta:
        if "name" not in inline_fields:
            warnings.append(f"引用文件缺少 name: {path}")
        meta["name"] = path.stem
    if "described" not in meta:
        if "described" not in inline_fields:
            warnings.append(f"引用文件缺少 described: {path}")
        meta["described"] = ""
    return meta


def inline_meta_fields(item: Dict[str, Any]) -> frozenset:
    return frozenset(field for field in ("name", "described") if item.get(field))


def parse_number_pair(
    value: Any,
    warnings: List[str],
    item_id: str,
    field_name: str,
) -> Optional[Tuple[float, float]]:
    if value is None:
        return None
    if not isinstance(value, list) or len(value) != 2:
        warnings.append(f"{item_id} 的 {field_name} 格式无效，应为两个数字的数组: {value}")
        return None
    try:
        return float(value[0]), float(value[1])
    except (TypeError, ValueError):
        warnings.append(f"{item_id} 的 {field_name} 不是数字: {value}")
        return None


def parse_at(value: Any, warnings: List[str], item_id: str) -> Optional[Tuple[float, float]]:
    return parse_number_pair(value, warnings, item_id, "at")


def as_string_list(value: Any, warnings: List[str], field_name: str, item_id: str) -> List[str]:
    if value is None:
        warnings.append(f"{item_id} 缺少 {field_name}")
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        warnings.append(f"{item_id} 的 {field_name} 必须是字符串数组")
        return []
    return value


def as_optional_string_list(value: Any, warnings: List[str], field_name: str, item_id: str) -> List[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        warnings.append(f"{item_id} 的 {field_name} 必须是字符串数组")
        return []
    return value


def endpoint_scope_name(scope: Optional[str]) -> str:
    return "top" if scope is None else scope


def relation_endpoint_exists(
    endpoint_id: str,
    object_ids: Set[str],
    group_ids: Set[str],
    interface_ids_by_group: Dict[str, Set[str]],
) -> bool:
    if endpoint_id in object_ids or endpoint_id in group_ids:
        return True
    if "." not in endpoint_id:
        return False
    group_id, interface_id = endpoint_id.rsplit(".", 1)
    return interface_id in interface_ids_by_group.get(group_id, set())


def relation_endpoint_scope(
    endpoint_id: str,
    object_ids: Set[str],
    group_ids: Set[str],
    object_parent_by_id: Dict[str, str],
    interface_ids_by_group: Dict[str, Set[str]],
) -> Optional[str]:
    if endpoint_id in object_ids:
        return object_parent_by_id.get(endpoint_id)
    if endpoint_id in group_ids:
        return None
    if "." in endpoint_id:
        group_id, interface_id = endpoint_id.rsplit(".", 1)
        if interface_id in interface_ids_by_group.get(group_id, set()):
            return None
    return None


def load_graph(path: Path) -> Diagram:
    path = path.resolve()
    raw = json.loads(read_text(path))
    warnings: List[str] = []

    if raw.get("format") not in {"arch-graph/v0.1", "arch-graph/v0.2"}:
        warnings.append(f"图文件 format 不是 arch-graph/v0.1 或 arch-graph/v0.2: {raw.get('format')}")

    meta = {
        "name": raw.get("name") or path.stem,
        "described": raw.get("described") or "",
    }

    objects: List[DiagramObject] = []
    seen_object_ids = set()
    for item in raw.get("objects", []):
        object_id = item.get("id")
        if not isinstance(object_id, str) or not object_id:
            warnings.append(f"对象缺少有效 id: {item}")
            continue
        if object_id in seen_object_ids:
            warnings.append(f"重复对象 ID: {object_id}")
            continue
        seen_object_ids.add(object_id)

        ref_path: Optional[Path] = None
        source_meta: Dict[str, str] = {}
        if isinstance(item.get("ref"), str):
            ref_path = (path.parent / item["ref"]).resolve()
            source_meta = load_document_meta(ref_path, warnings, inline_meta_fields(item))
        else:
            warnings.append(f"对象缺少 ref，将使用内联信息: {object_id}")

        module_kind = item.get("module_kind") or source_meta.get("module_kind")
        default_shape, default_stroke, default_fill = MODULE_KIND_STYLES.get(
            module_kind or "",
            ("rounded-rect", "#334155", "#f8fafc"),
        )
        objects.append(
            DiagramObject(
                object_id=object_id,
                ref=ref_path,
                shape=item.get("shape") or default_shape,
                name=item.get("name") or source_meta.get("name") or object_id,
                described=item.get("described") or source_meta.get("described") or "",
                at=parse_at(item.get("at"), warnings, object_id),
                stroke=item.get("stroke") or default_stroke,
                fill=item.get("fill") or default_fill,
                source_meta=source_meta,
            )
        )

    object_ids = {item.object_id for item in objects}

    groups: List[DiagramGroup] = []
    seen_group_ids = set()
    for item in raw.get("groups", []):
        group_id = item.get("id")
        if not isinstance(group_id, str) or not group_id:
            warnings.append(f"组合模块缺少有效 id: {item}")
            continue
        if group_id in seen_group_ids:
            warnings.append(f"重复组合模块 ID: {group_id}")
            continue
        if group_id in object_ids:
            warnings.append(f"组合模块 ID 与对象 ID 冲突: {group_id}")
            continue
        seen_group_ids.add(group_id)

        ref_path: Optional[Path] = None
        source_meta: Dict[str, str] = {}
        if isinstance(item.get("ref"), str):
            ref_path = (path.parent / item["ref"]).resolve()
            source_meta = load_document_meta(ref_path, warnings, inline_meta_fields(item))

        contains = as_string_list(item.get("contains"), warnings, "contains", group_id)
        for child_id in contains:
            if child_id not in object_ids:
                warnings.append(f"组合模块 {group_id} 包含未知对象: {child_id}")

        interfaces: List[GroupInterface] = []
        seen_interface_ids = set()
        raw_interfaces = item.get("interfaces", [])
        if raw_interfaces is None:
            raw_interfaces = []
        if not isinstance(raw_interfaces, list):
            warnings.append(f"组合模块 {group_id} 的 interfaces 必须是数组")
            raw_interfaces = []
        for interface_item in raw_interfaces:
            if not isinstance(interface_item, dict):
                warnings.append(f"组合模块 {group_id} 的 interface 格式无效: {interface_item}")
                continue
            interface_id = interface_item.get("id")
            if not isinstance(interface_id, str) or not interface_id:
                warnings.append(f"组合模块 {group_id} 的 interface 缺少有效 id: {interface_item}")
                continue
            if "." in interface_id:
                warnings.append(f"组合模块 {group_id} 的 interface ID 不能包含点号: {interface_id}")
                continue
            if interface_id in seen_interface_ids:
                warnings.append(f"组合模块 {group_id} 存在重复 interface ID: {interface_id}")
                continue
            seen_interface_ids.add(interface_id)
            provided_by = as_optional_string_list(
                interface_item.get("provided_by"),
                warnings,
                "provided_by",
                f"{group_id}.{interface_id}",
            )
            for provider_id in provided_by:
                if provider_id not in object_ids:
                    warnings.append(f"组合模块接口 {group_id}.{interface_id} 由未知对象提供: {provider_id}")
                elif provider_id not in contains:
                    warnings.append(f"组合模块接口 {group_id}.{interface_id} 的 provider 不在 contains 内: {provider_id}")
            interfaces.append(
                GroupInterface(
                    interface_id=interface_id,
                    name=interface_item.get("name") or interface_id,
                    described=interface_item.get("described") or "",
                    provided_by=provided_by,
                )
            )

        groups.append(
            DiagramGroup(
                group_id=group_id,
                ref=ref_path,
                name=item.get("name") or source_meta.get("name") or group_id,
                described=item.get("described") or source_meta.get("described") or "",
                contains=contains,
                interfaces=interfaces,
                at=parse_at(item.get("at"), warnings, group_id),
                source_meta=source_meta,
            )
        )

    group_ids = {item.group_id for item in groups}
    interface_ids_by_group = {
        group.group_id: {item.interface_id for item in group.interfaces}
        for group in groups
    }
    object_parent_by_id: Dict[str, str] = {}
    for group in groups:
        for child_id in group.contains:
            if child_id not in object_ids:
                continue
            existing_parent = object_parent_by_id.get(child_id)
            if existing_parent is not None and existing_parent != group.group_id:
                warnings.append(f"对象 {child_id} 同时出现在多个组合模块: {existing_parent}, {group.group_id}")
                continue
            object_parent_by_id[child_id] = group.group_id

    relations: List[Relation] = []
    for item in raw.get("relations", []):
        source = item.get("from")
        target = item.get("to")
        if not isinstance(source, str) or not isinstance(target, str):
            warnings.append(f"关系缺少有效 from/to: {item}")
            continue
        source_exists = relation_endpoint_exists(source, object_ids, group_ids, interface_ids_by_group)
        target_exists = relation_endpoint_exists(target, object_ids, group_ids, interface_ids_by_group)
        if not source_exists:
            warnings.append(f"关系引用了未知起点端点: {source}")
        if not target_exists:
            warnings.append(f"关系引用了未知终点端点: {target}")
        if source_exists and target_exists:
            source_scope = relation_endpoint_scope(
                source,
                object_ids,
                group_ids,
                object_parent_by_id,
                interface_ids_by_group,
            )
            target_scope = relation_endpoint_scope(
                target,
                object_ids,
                group_ids,
                object_parent_by_id,
                interface_ids_by_group,
            )
            if source_scope != target_scope:
                warnings.append(
                    "关系跨越不同层级: "
                    f"{source}({endpoint_scope_name(source_scope)}) -> "
                    f"{target}({endpoint_scope_name(target_scope)})；"
                    "建议连接到共同父层级的模块或 group.interface"
                )
        relations.append(
            Relation(
                source=source,
                target=target,
                described=item.get("described") or item.get("label") or "",
                style=item.get("style") or "solid",
                label_offset=parse_number_pair(
                    item.get("label_offset"),
                    warnings,
                    f"{source}->{target}",
                    "label_offset",
                )
                or (0, 0),
            )
        )

    return Diagram(path=path, meta=meta, objects=objects, groups=groups, relations=relations, warnings=warnings)


def char_display_units(value: str) -> int:
    if unicodedata.east_asian_width(value) in {"F", "W"}:
        return 2
    return 1


def text_display_units(value: str) -> int:
    return sum(char_display_units(char) for char in value)


def trim_to_units(value: str, max_units: int) -> str:
    output: List[str] = []
    used = 0
    for char in value:
        units = char_display_units(char)
        if used + units > max_units:
            break
        output.append(char)
        used += units
    return "".join(output)


def ellipsize_to_units(value: str, max_units: int) -> str:
    suffix = "..."
    suffix_units = text_display_units(suffix)
    if text_display_units(value) + suffix_units <= max_units:
        return f"{value}{suffix}"
    return f"{trim_to_units(value, max(0, max_units - suffix_units)).rstrip()}{suffix}"


def wrap_text(value: str, max_units: int, max_lines: Optional[int] = None) -> List[str]:
    value = " ".join(value.strip().split())
    if not value:
        return []

    lines: List[str] = []
    current = ""
    current_units = 0
    for token in value.split():
        token_units = text_display_units(token)
        separator_units = 1 if current else 0
        if current and current_units + separator_units + token_units <= max_units:
            current = f"{current} {token}".strip()
            current_units += separator_units + token_units
            continue
        if current:
            lines.append(current)
            current = ""
            current_units = 0
        if token_units <= max_units:
            current = token
            current_units = token_units
            continue

        chunk = ""
        chunk_units = 0
        for char in token:
            char_units = char_display_units(char)
            if chunk and chunk_units + char_units > max_units:
                lines.append(chunk)
                chunk = ""
                chunk_units = 0
            chunk += char
            chunk_units += char_units
        current = chunk
        current_units = chunk_units
    if current:
        lines.append(current)
    if max_lines is not None and len(lines) > max_lines:
        visible = lines[:max_lines]
        visible[-1] = ellipsize_to_units(visible[-1], max_units)
        return visible
    return lines


def escape(value: str) -> str:
    return html.escape(value, quote=True)


def document_href(path: Optional[Path], link_base: Optional[Path]) -> Optional[str]:
    if path is None:
        return None
    resolved = path.resolve()
    if link_base is None:
        return resolved.as_uri()
    try:
        relative = os.path.relpath(resolved, start=link_base.resolve().parent)
    except ValueError:
        return resolved.as_uri()
    return quote(Path(relative).as_posix(), safe="/")


def wrap_svg_link(svg: str, href: Optional[str], class_name: str) -> str:
    if not href:
        return svg
    return f'<a class="{class_name}" href="{escape(href)}" target="_blank">\n{svg}\n</a>'


def render_svg_styles() -> str:
    return """    <style>
      .node-shape { stroke-width: 1.6; }
      .node-link,
      .group-link {
        cursor: pointer;
        text-decoration: none;
      }
      .node-link:hover .node-shape,
      .node-link:focus .node-shape,
      .group-link:hover .group-shape,
      .group-link:focus .group-shape {
        stroke-width: 2.6;
      }
      .node-line {
        fill: none;
        stroke-width: 1.6;
      }
      .group-shape {
        fill: #eef2ff;
        stroke: #4f46e5;
        stroke-width: 1.8;
        stroke-dasharray: 10 7;
      }
      .group-title {
        fill: #312e81;
        font-size: 14px;
        font-weight: 800;
      }
      .group-description {
        fill: #4338ca;
        font-size: 12px;
        font-weight: 600;
      }
      .node-title {
        fill: #1e293b;
        font-size: 15px;
        font-weight: 700;
      }
      .node-description {
        fill: #64748b;
        font-size: 12px;
      }
      .relation-line {
        fill: none;
        stroke: #111827;
        stroke-width: 2.8;
      }
      .relation-line-inner {
        stroke-width: 1.5;
      }
      .relation-line-outer {
        stroke-width: 3.4;
      }
      .relation-hitbox {
        fill: none;
        stroke: transparent;
        stroke-width: 18;
        pointer-events: stroke;
        cursor: help;
      }
      .relation-hover-line {
        fill: none;
        stroke: #111827;
        stroke-width: 4.4;
        opacity: 0;
        pointer-events: none;
      }
      .relation-hover-line-inner {
        stroke-width: 2.2;
      }
      .relation-hover-line-outer {
        stroke-width: 5.2;
      }
      .relation-hover:hover .relation-hover-line {
        opacity: 0.75;
      }
      .relation-bubble {
        opacity: 0;
        transition: opacity 120ms ease;
        pointer-events: none;
      }
      .relation-hover:hover .relation-bubble {
        opacity: 1;
      }
      .relation-bubble-box {
        fill: #ffffff;
        stroke: #94a3b8;
        stroke-width: 1;
      }
      .relation-bubble-text {
        fill: #0f172a;
        font-size: 12px;
        font-weight: 650;
        pointer-events: none;
      }
      .arrow { fill: #111827; }
    </style>"""


def object_positions(objects: List[DiagramObject]) -> Dict[str, Tuple[float, float]]:
    if not objects:
        return {}

    columns = max(1, math.ceil(math.sqrt(len(objects))))
    positions: Dict[str, Tuple[float, float]] = {}
    for index, item in enumerate(objects):
        if item.at is None:
            col = index % columns
            row = index // columns
        else:
            col, row = item.at
        positions[item.object_id] = (MARGIN_X + col * CELL_WIDTH, MARGIN_Y + row * CELL_HEIGHT)
    return positions


def text_svg(
    lines: Iterable[str],
    x: float,
    y: float,
    class_name: str,
    line_height: int = 18,
    anchor: str = "middle",
) -> str:
    output: List[str] = []
    for index, line in enumerate(lines):
        output.append(
            f'<text x="{x:.1f}" y="{y + index * line_height:.1f}" '
            f'class="{class_name}" text-anchor="{anchor}">{escape(line)}</text>'
        )
    return "\n".join(output)


def boxes_overlap(first: BBox, second: BBox) -> bool:
    return first[0] < second[2] and first[2] > second[0] and first[1] < second[3] and first[3] > second[1]


def overlap_area(first: BBox, second: BBox) -> float:
    if not boxes_overlap(first, second):
        return 0
    width = min(first[2], second[2]) - max(first[0], second[0])
    height = min(first[3], second[3]) - max(first[1], second[1])
    return max(0, width) * max(0, height)


def padded_box(box: BBox, padding: float) -> BBox:
    return box[0] - padding, box[1] - padding, box[2] + padding, box[3] + padding


def render_object(item: DiagramObject, x: float, y: float, link_base: Optional[Path] = None) -> str:
    width = NODE_WIDTH
    height = NODE_HEIGHT
    shape = item.shape
    top = y - height / 2
    left = x - width / 2
    shape_style = f' style="fill: {escape(item.fill)}; stroke: {escape(item.stroke)};"'
    title_lines = wrap_text(item.name, 24, 2)
    description_lines = wrap_text(item.described, 30, 2)
    text_lines = title_lines + description_lines
    text_start = y - (len(text_lines) - 1) * 10

    if shape == "circle":
        shape_svg = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{NODE_CIRCLE_RADIUS}" class="node-shape"{shape_style} />'
    elif shape == "hexagon":
        points = [
            (left + 28, top),
            (left + width - 28, top),
            (left + width, y),
            (left + width - 28, top + height),
            (left + 28, top + height),
            (left, y),
        ]
        shape_svg = f'<polygon points="{" ".join(f"{px:.1f},{py:.1f}" for px, py in points)}" class="node-shape"{shape_style} />'
    elif shape == "diamond":
        points = [(x, top - 8), (left + width + 8, y), (x, top + height + 8), (left - 8, y)]
        shape_svg = f'<polygon points="{" ".join(f"{px:.1f},{py:.1f}" for px, py in points)}" class="node-shape"{shape_style} />'
    elif shape == "folder":
        tab_w = 72
        tab_h = 18
        path = (
            f"M {left:.1f} {top + 10:.1f} "
            f"H {left + tab_w:.1f} L {left + tab_w + 16:.1f} {top + tab_h:.1f} "
            f"H {left + width:.1f} V {top + height:.1f} H {left:.1f} Z"
        )
        shape_svg = f'<path d="{path}" class="node-shape"{shape_style} />'
    elif shape == "port":
        points = [(left + 18, top), (left + width, top), (left + width - 18, top + height), (left, top + height)]
        shape_svg = f'<polygon points="{" ".join(f"{px:.1f},{py:.1f}" for px, py in points)}" class="node-shape"{shape_style} />'
    elif shape == "frame":
        shape_svg = "\n".join(
            [
                f'<rect x="{left:.1f}" y="{top:.1f}" width="{width:.1f}" height="{height:.1f}" rx="8" class="node-shape"{shape_style} />',
                f'<line x1="{left:.1f}" y1="{top + 24:.1f}" x2="{left + width:.1f}" y2="{top + 24:.1f}" class="node-line" style="stroke: {escape(item.stroke)};" />',
            ]
        )
    elif shape == "cylinder":
        shape_svg = "\n".join(
            [
                f'<rect x="{left:.1f}" y="{top + 12:.1f}" width="{width:.1f}" height="{height - 24:.1f}" class="node-shape"{shape_style} />',
                f'<ellipse cx="{x:.1f}" cy="{top + 12:.1f}" rx="{width / 2:.1f}" ry="16" class="node-shape"{shape_style} />',
                f'<path d="M {left:.1f} {top + height - 12:.1f} C {left:.1f} {top + height + 10:.1f}, {left + width:.1f} {top + height + 10:.1f}, {left + width:.1f} {top + height - 12:.1f}" class="node-line" style="stroke: {escape(item.stroke)};" />',
            ]
        )
    elif shape == "document":
        fold = 20
        shape_svg = "\n".join(
            [
                f'<path d="M {left:.1f} {top:.1f} H {left + width - fold:.1f} L {left + width:.1f} {top + fold:.1f} V {top + height:.1f} H {left:.1f} Z" class="node-shape"{shape_style} />',
                f'<path d="M {left + width - fold:.1f} {top:.1f} V {top + fold:.1f} H {left + width:.1f}" class="node-line" style="stroke: {escape(item.stroke)};" />',
            ]
        )
    elif shape == "rect":
        shape_svg = f'<rect x="{left:.1f}" y="{top:.1f}" width="{width:.1f}" height="{height:.1f}" rx="0" class="node-shape"{shape_style} />'
    elif shape == "small-rect":
        shape_svg = f'<rect x="{left + 12:.1f}" y="{top + 7:.1f}" width="{width - 24:.1f}" height="{height - 14:.1f}" rx="6" class="node-shape"{shape_style} />'
    else:
        shape_svg = f'<rect x="{left:.1f}" y="{top:.1f}" width="{width:.1f}" height="{height:.1f}" rx="12" class="node-shape"{shape_style} />'

    title_svg = text_svg(title_lines, x, text_start, "node-title", 21)
    desc_start = text_start + max(len(title_lines), 1) * 21
    desc_svg = text_svg(description_lines, x, desc_start, "node-description", 18)
    tooltip = f"<title>{escape(item.object_id)}"
    if item.ref:
        tooltip += f" - {escape(str(item.ref))}"
    tooltip += "</title>"
    node_svg = f'<g class="node" data-id="{escape(item.object_id)}">\n{tooltip}\n{shape_svg}\n{title_svg}\n{desc_svg}\n</g>'
    return wrap_svg_link(node_svg, document_href(item.ref, link_base), "node-link")


def object_half_size(item: DiagramObject) -> Tuple[float, float]:
    if item.shape == "circle":
        return NODE_CIRCLE_RADIUS, NODE_CIRCLE_RADIUS
    return NODE_WIDTH / 2, NODE_HEIGHT / 2


def object_box(item: DiagramObject, x: float, y: float, padding: float = 10) -> BBox:
    half_w, half_h = object_half_size(item)
    return x - half_w - padding, y - half_h - padding, x + half_w + padding, y + half_h + padding


def object_run_bounds(
    child_ids: List[str],
    positions: Dict[str, Tuple[float, float]],
    objects_by_id: Dict[str, DiagramObject],
) -> BBox:
    left_values = []
    right_values = []
    top_values = []
    bottom_values = []
    for child_id in child_ids:
        x, y = positions[child_id]
        half_w, half_h = object_half_size(objects_by_id[child_id])
        left_values.append(x - half_w)
        right_values.append(x + half_w)
        top_values.append(y - half_h)
        bottom_values.append(y + half_h)

    return (
        min(left_values) - GROUP_PADDING_X,
        min(top_values) - GROUP_PADDING_TOP,
        max(right_values) + GROUP_PADDING_X,
        max(bottom_values) + GROUP_PADDING_BOTTOM,
    )


def group_frame_bounds(
    group: DiagramGroup,
    positions: Dict[str, Tuple[float, float]],
    objects_by_id: Dict[str, DiagramObject],
) -> List[BBox]:
    contained = [child_id for child_id in group.contains if child_id in positions and child_id in objects_by_id]
    if not contained:
        if group.at is None:
            return []
        x, y = group.at
        return [(x, y, x + 280, y + 180)]

    return [object_run_bounds(contained, positions, objects_by_id)]


def group_bounds(
    group: DiagramGroup,
    positions: Dict[str, Tuple[float, float]],
    objects_by_id: Dict[str, DiagramObject],
) -> Optional[Tuple[float, float, float, float]]:
    frames = group_frame_bounds(group, positions, objects_by_id)
    if not frames:
        return None
    frame = frames[0]
    return (
        frame[0],
        frame[1],
        frame[2],
        frame[3],
    )


def render_group(
    group: DiagramGroup,
    positions: Dict[str, Tuple[float, float]],
    objects_by_id: Dict[str, DiagramObject],
    link_base: Optional[Path] = None,
) -> str:
    frames = group_frame_bounds(group, positions, objects_by_id)
    if not frames:
        return ""

    label_bounds = frames[0]
    label_left, label_top, label_right, _ = label_bounds
    label_units = max(16, int((label_right - label_left - 36) / LABEL_UNIT_WIDTH))
    title_svg = text_svg(
        wrap_text(group.name, min(44, label_units), 1),
        label_left + 18,
        label_top + 28,
        "group-title",
        18,
        "start",
    )
    desc_svg = text_svg(
        wrap_text(group.described, min(76, label_units), 1),
        label_left + 18,
        label_top + 48,
        "group-description",
        16,
        "start",
    )
    tooltip = f"<title>{escape(group.group_id)}"
    if group.ref:
        tooltip += f" - {escape(str(group.ref))}"
    tooltip += "</title>"
    left, top, right, bottom = frames[0]
    shape_svg = f'<rect x="{left:.1f}" y="{top:.1f}" width="{right - left:.1f}" height="{bottom - top:.1f}" rx="10" class="group-shape" />'
    group_svg = "\n".join(
        [
            f'<g class="group" data-id="{escape(group.group_id)}">',
            tooltip,
            shape_svg,
            title_svg,
            desc_svg,
            "</g>",
        ]
    )
    return wrap_svg_link(group_svg, document_href(group.ref, link_base), "group-link")


def group_label_box(bounds: Tuple[float, float, float, float]) -> BBox:
    left, top, right, _ = bounds
    return left + 10, top + 8, right - 10, top + 66


def union_box(boxes: List[BBox]) -> BBox:
    return (
        min(box[0] for box in boxes),
        min(box[1] for box in boxes),
        max(box[2] for box in boxes),
        max(box[3] for box in boxes),
    )


def box_center(box: BBox) -> Point:
    return (box[0] + box[2]) / 2, (box[1] + box[3]) / 2


def box_port(box: BBox, side: str, padding: float = 0) -> Point:
    left, top, right, bottom = box
    center_x, center_y = box_center(box)
    if side == "left":
        return left - padding, center_y
    if side == "right":
        return right + padding, center_y
    if side == "top":
        return center_x, top - padding
    if side == "bottom":
        return center_x, bottom + padding
    raise ValueError(f"Unknown side: {side}")


def object_port(item: DiagramObject, center: Point, side: str, padding: float = 0) -> Point:
    x, y = center
    half_w, half_h = object_half_size(item)
    if side == "left":
        return x - half_w - padding, y
    if side == "right":
        return x + half_w + padding, y
    if side == "top":
        return x, y - half_h - padding
    if side == "bottom":
        return x, y + half_h + padding
    raise ValueError(f"Unknown side: {side}")


def route_endpoint_port(endpoint: RouteEndpoint, side: str, padding: float = 0) -> Point:
    return box_port(endpoint.box, side, padding)


def simplify_points(points: List[Point]) -> List[Point]:
    simplified: List[Point] = []
    for point in points:
        if simplified and math.isclose(point[0], simplified[-1][0]) and math.isclose(point[1], simplified[-1][1]):
            continue
        simplified.append(point)

    index = 1
    while index < len(simplified) - 1:
        prev_point = simplified[index - 1]
        point = simplified[index]
        next_point = simplified[index + 1]
        same_x = math.isclose(prev_point[0], point[0]) and math.isclose(point[0], next_point[0])
        same_y = math.isclose(prev_point[1], point[1]) and math.isclose(point[1], next_point[1])
        if same_x or same_y:
            simplified.pop(index)
            continue
        index += 1
    return simplified


def route_segments(points: List[Point]) -> List[Segment]:
    return [
        (points[index], points[index + 1])
        for index in range(len(points) - 1)
        if not (
            math.isclose(points[index][0], points[index + 1][0])
            and math.isclose(points[index][1], points[index + 1][1])
        )
    ]


def segment_length(segment: Segment) -> float:
    (x1, y1), (x2, y2) = segment
    return abs(x2 - x1) + abs(y2 - y1)


def route_length(points: List[Point]) -> float:
    return sum(segment_length(segment) for segment in route_segments(points))


def route_midpoint(points: List[Point]) -> Point:
    segments = route_segments(points)
    total = sum(segment_length(segment) for segment in segments)
    if not segments or total == 0:
        return points[0] if points else (0, 0)

    target = total / 2
    walked = 0.0
    for (x1, y1), (x2, y2) in segments:
        length = abs(x2 - x1) + abs(y2 - y1)
        if walked + length >= target:
            remaining = target - walked
            if math.isclose(x1, x2):
                return x1, y1 + math.copysign(remaining, y2 - y1)
            return x1 + math.copysign(remaining, x2 - x1), y1
        walked += length
    return points[-1]


def path_data(points: List[Point]) -> str:
    if not points:
        return ""
    first = points[0]
    commands = [f"M {first[0]:.1f} {first[1]:.1f}"]
    commands.extend(f"L {x:.1f} {y:.1f}" for x, y in points[1:])
    return " ".join(commands)


def horizontal_overlap(first: Tuple[float, float], second: Tuple[float, float]) -> float:
    left = max(min(first), min(second))
    right = min(max(first), max(second))
    return max(0.0, right - left)


def segment_box_overlap(segment: Segment, box: BBox) -> float:
    (x1, y1), (x2, y2) = segment
    if math.isclose(y1, y2):
        if box[1] <= y1 <= box[3]:
            return horizontal_overlap((x1, x2), (box[0], box[2]))
        return 0
    if math.isclose(x1, x2):
        if box[0] <= x1 <= box[2]:
            return horizontal_overlap((y1, y2), (box[1], box[3]))
        return 0
    return 0


def parallel_overlap(first: Segment, second: Segment, tolerance: float = 12) -> float:
    (x1, y1), (x2, y2) = first
    (x3, y3), (x4, y4) = second
    first_horizontal = math.isclose(y1, y2)
    second_horizontal = math.isclose(y3, y4)
    if first_horizontal and second_horizontal and abs(y1 - y3) <= tolerance:
        return horizontal_overlap((x1, x2), (x3, x4))
    first_vertical = math.isclose(x1, x2)
    second_vertical = math.isclose(x3, x4)
    if first_vertical and second_vertical and abs(x1 - x3) <= tolerance:
        return horizontal_overlap((y1, y2), (y3, y4))
    return 0


def segments_cross(first: Segment, second: Segment) -> bool:
    (x1, y1), (x2, y2) = first
    (x3, y3), (x4, y4) = second
    first_horizontal = math.isclose(y1, y2)
    second_horizontal = math.isclose(y3, y4)
    if first_horizontal == second_horizontal:
        return False
    if first_horizontal:
        return min(x1, x2) <= x3 <= max(x1, x2) and min(y3, y4) <= y1 <= max(y3, y4)
    return min(x3, x4) <= x1 <= max(x3, x4) and min(y1, y2) <= y3 <= max(y1, y2)


def relation_dash(relation: Relation) -> str:
    return ' stroke-dasharray="8 7"' if relation.style == "dashed" else ""


def normalize_route_coord(value: float) -> float:
    return round(value, 1)


def normalize_route_point(point: Point) -> Point:
    return normalize_route_coord(point[0]), normalize_route_coord(point[1])


def route_key(points: List[Point]) -> Tuple[Point, ...]:
    return tuple(normalize_route_point(point) for point in points)


def dedupe_routes(routes: List[List[Point]]) -> List[List[Point]]:
    deduped: List[List[Point]] = []
    seen: Set[Tuple[Point, ...]] = set()
    for route in routes:
        key = route_key(route)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(route)
    return deduped


def endpoint_axis(center: Point, endpoint: Point) -> Tuple[int, int]:
    dx = endpoint[0] - center[0]
    dy = endpoint[1] - center[1]
    if abs(dx) >= abs(dy):
        if math.isclose(dx, 0):
            return (0, 0)
        return (1 if dx > 0 else -1, 0)
    if math.isclose(dy, 0):
        return (0, 0)
    return (0, 1 if dy > 0 else -1)


def endpoint_stub(center: Point, endpoint: Point) -> Optional[Point]:
    axis_x, axis_y = endpoint_axis(center, endpoint)
    if axis_x == 0 and axis_y == 0:
        return None
    return (
        endpoint[0] + axis_x * ROUTE_ENDPOINT_STUB,
        endpoint[1] + axis_y * ROUTE_ENDPOINT_STUB,
    )


def points_aligned(first: Point, second: Point) -> bool:
    return math.isclose(first[0], second[0]) or math.isclose(first[1], second[1])


def source_endpoint_points(start: Point, next_point: Point, source_center: Point) -> List[Point]:
    stub = endpoint_stub(source_center, start)
    if stub is None:
        return [start]

    axis_x, axis_y = endpoint_axis(source_center, start)
    points = [start, stub]
    if axis_x != 0 and (next_point[0] - start[0]) * axis_x < 0:
        lane_y = source_center[1] + (ROUTE_ENDPOINT_CLEARANCE_Y if next_point[1] >= source_center[1] else -ROUTE_ENDPOINT_CLEARANCE_Y)
        points.extend([(stub[0], lane_y), (next_point[0], lane_y)])
        return points
    if axis_y != 0 and (next_point[1] - start[1]) * axis_y < 0:
        lane_x = source_center[0] + (ROUTE_ENDPOINT_CLEARANCE_X if next_point[0] >= source_center[0] else -ROUTE_ENDPOINT_CLEARANCE_X)
        points.extend([(lane_x, stub[1]), (lane_x, next_point[1])])
        return points
    if not points_aligned(stub, next_point):
        bridge = (stub[0], next_point[1]) if axis_x != 0 else (next_point[0], stub[1])
        points.append(bridge)
    return points


def target_endpoint_points(prev_point: Point, end: Point, target_center: Point) -> List[Point]:
    stub = endpoint_stub(target_center, end)
    if stub is None:
        return [end]

    axis_x, axis_y = endpoint_axis(target_center, end)
    points: List[Point] = []
    if axis_x != 0 and (prev_point[0] - end[0]) * axis_x < 0:
        lane_y = target_center[1] + (ROUTE_ENDPOINT_CLEARANCE_Y if prev_point[1] >= target_center[1] else -ROUTE_ENDPOINT_CLEARANCE_Y)
        points.extend([(prev_point[0], lane_y), (stub[0], lane_y)])
    elif axis_y != 0 and (prev_point[1] - end[1]) * axis_y < 0:
        lane_x = target_center[0] + (ROUTE_ENDPOINT_CLEARANCE_X if prev_point[0] >= target_center[0] else -ROUTE_ENDPOINT_CLEARANCE_X)
        points.extend([(lane_x, prev_point[1]), (lane_x, stub[1])])
    elif not points_aligned(prev_point, stub):
        bridge = (stub[0], prev_point[1]) if axis_x != 0 else (prev_point[0], stub[1])
        points.append(bridge)
    points.extend([stub, end])
    return points


def route_with_endpoint_stubs(points: List[Point], source_center: Point, target_center: Point) -> List[Point]:
    route = simplify_points(points)
    if len(route) < 2:
        return route

    start = route[0]
    end = route[-1]
    start_points = source_endpoint_points(start, route[1], source_center)
    middle_points = route[1:-1]
    prev_for_target = middle_points[-1] if middle_points else start_points[-1]
    end_points = target_endpoint_points(prev_for_target, end, target_center)
    return simplify_points(start_points + middle_points + end_points)


def segment_hits_obstacle(segment: Segment, obstacles: List[BBox]) -> bool:
    return any(segment_box_overlap(segment, box) > 0 for box in obstacles)


def search_segment_cost(
    segment: Segment,
    hard_obstacles: List[BBox],
    soft_obstacles: List[BBox],
    placed_segments: List[Segment],
) -> Optional[float]:
    if segment_hits_obstacle(segment, hard_obstacles):
        return None

    cost = segment_length(segment) * 0.06
    for box in soft_obstacles:
        overlap = segment_box_overlap(segment, box)
        if overlap > 0:
            cost += 420 + overlap * 4
    for placed in placed_segments:
        overlap = parallel_overlap(segment, placed)
        if overlap > 0:
            cost += min(overlap, 96) * 0.5 + max(0.0, overlap - 96) * 3
        elif segments_cross(segment, placed):
            cost += 28
    return cost


def route_search_values(start: Point, end: Point, boxes: List[BBox]) -> Tuple[List[float], List[float]]:
    x_values = {normalize_route_coord(start[0]), normalize_route_coord(end[0])}
    y_values = {normalize_route_coord(start[1]), normalize_route_coord(end[1])}

    if boxes:
        left = min(box[0] for box in boxes)
        top = min(box[1] for box in boxes)
        right = max(box[2] for box in boxes)
        bottom = max(box[3] for box in boxes)
    else:
        left = min(start[0], end[0])
        top = min(start[1], end[1])
        right = max(start[0], end[0])
        bottom = max(start[1], end[1])

    x_values.update(
        [
            normalize_route_coord(left - ROUTE_OUTER_GAP),
            normalize_route_coord(right + ROUTE_OUTER_GAP),
        ]
    )
    y_values.update(
        [
            normalize_route_coord(top - ROUTE_OUTER_GAP),
            normalize_route_coord(bottom + ROUTE_OUTER_GAP),
        ]
    )

    for box in boxes:
        box_left, box_top, box_right, box_bottom = box
        for gap in (ROUTE_TRACK_GAP, ROUTE_TRACK_GAP * 2):
            x_values.add(normalize_route_coord(box_left - gap))
            x_values.add(normalize_route_coord(box_right + gap))
            y_values.add(normalize_route_coord(box_top - gap))
            y_values.add(normalize_route_coord(box_bottom + gap))

    return sorted(x_values), sorted(y_values)


def route_search_neighbors(
    point: Point,
    x_values: List[float],
    y_values: List[float],
    x_indexes: Dict[float, int],
    y_indexes: Dict[float, int],
) -> Iterable[Tuple[Point, str]]:
    x, y = point
    x_index = x_indexes[x]
    y_index = y_indexes[y]
    if x_index > 0:
        yield (x_values[x_index - 1], y), "H"
    if x_index < len(x_values) - 1:
        yield (x_values[x_index + 1], y), "H"
    if y_index > 0:
        yield (x, y_values[y_index - 1]), "V"
    if y_index < len(y_values) - 1:
        yield (x, y_values[y_index + 1]), "V"


def reconstruct_route(
    end_state: Tuple[Point, Optional[str]],
    previous: Dict[Tuple[Point, Optional[str]], Tuple[Point, Optional[str]]],
) -> List[Point]:
    points = [end_state[0]]
    state = end_state
    while state in previous:
        state = previous[state]
        points.append(state[0])
    points.reverse()
    return simplify_points(points)


def orthogonal_search_route(
    start: Point,
    end: Point,
    boxes: List[BBox],
    hard_obstacles: List[BBox],
    soft_obstacles: List[BBox],
    placed_segments: List[Segment],
) -> Optional[List[Point]]:
    start = normalize_route_point(start)
    end = normalize_route_point(end)
    if start == end:
        return None

    x_values, y_values = route_search_values(start, end, boxes)
    if start[0] not in x_values or end[0] not in x_values or start[1] not in y_values or end[1] not in y_values:
        return None
    x_indexes = {value: index for index, value in enumerate(x_values)}
    y_indexes = {value: index for index, value in enumerate(y_values)}

    def heuristic(point: Point) -> float:
        return (abs(point[0] - end[0]) + abs(point[1] - end[1])) * 0.06

    start_state = (start, None)
    distances: Dict[Tuple[Point, Optional[str]], float] = {start_state: 0.0}
    previous: Dict[Tuple[Point, Optional[str]], Tuple[Point, Optional[str]]] = {}
    queue: List[Tuple[float, float, int, Point, Optional[str]]] = [(heuristic(start), 0.0, 0, start, None)]
    counter = 1
    expansions = 0

    while queue and expansions < ROUTE_SEARCH_MAX_EXPANSIONS:
        _, cost, _, point, direction = heapq.heappop(queue)
        state = (point, direction)
        if cost > distances.get(state, math.inf):
            continue
        if point == end:
            return reconstruct_route(state, previous)

        expansions += 1
        for next_point, next_direction in route_search_neighbors(point, x_values, y_values, x_indexes, y_indexes):
            segment = (point, next_point)
            segment_cost = search_segment_cost(segment, hard_obstacles, soft_obstacles, placed_segments)
            if segment_cost is None:
                continue
            turn_cost = 0 if direction in (None, next_direction) else 85
            next_state = (next_point, next_direction)
            next_cost = cost + segment_cost + turn_cost
            if next_cost >= distances.get(next_state, math.inf):
                continue
            distances[next_state] = next_cost
            previous[next_state] = state
            heapq.heappush(
                queue,
                (next_cost + heuristic(next_point), next_cost, counter, next_point, next_direction),
            )
            counter += 1

    return None


def relation_port_pairs(
    relation: Relation,
    endpoints_by_id: Dict[str, RouteEndpoint],
) -> List[Tuple[Point, Point]]:
    source = endpoints_by_id[relation.source]
    target = endpoints_by_id[relation.target]
    source_center = source.center
    target_center = target.center
    sx, sy = source_center
    tx, ty = target_center
    dx = tx - sx
    dy = ty - sy

    h_source_side = "right" if dx >= 0 else "left"
    h_target_side = "left" if dx >= 0 else "right"
    v_source_side = "bottom" if dy >= 0 else "top"
    v_target_side = "top" if dy >= 0 else "bottom"

    preferred_sides = [
        (h_source_side, h_target_side),
        (v_source_side, v_target_side),
        (h_source_side, v_target_side),
        (v_source_side, h_target_side),
        ("top", "top"),
        ("bottom", "bottom"),
        ("left", "left"),
        ("right", "right"),
    ]
    if abs(dy) > abs(dx):
        preferred_sides[0], preferred_sides[1] = preferred_sides[1], preferred_sides[0]

    pairs: List[Tuple[Point, Point]] = []
    seen: Set[Tuple[Point, Point]] = set()
    for source_side, target_side in preferred_sides:
        pair = (
            normalize_route_point(route_endpoint_port(source, source_side)),
            normalize_route_point(route_endpoint_port(target, target_side)),
        )
        if pair in seen:
            continue
        seen.add(pair)
        pairs.append(pair)
    return pairs


def orthogonal_search_route_candidates(
    relation: Relation,
    endpoints_by_id: Dict[str, RouteEndpoint],
    object_boxes_by_id: Dict[str, BBox],
    group_label_boxes: List[BBox],
    placed_segments: List[Segment],
) -> List[List[Point]]:
    boxes = list(object_boxes_by_id.values()) + group_label_boxes
    endpoint_owner_ids = (
        endpoints_by_id[relation.source].owner_object_ids
        | endpoints_by_id[relation.target].owner_object_ids
    )
    hard_obstacles = [
        box
        for object_id, box in object_boxes_by_id.items()
        if object_id not in endpoint_owner_ids
    ]
    soft_obstacles = group_label_boxes
    candidates: List[List[Point]] = []
    for start, end in relation_port_pairs(relation, endpoints_by_id):
        route = orthogonal_search_route(start, end, boxes, hard_obstacles, soft_obstacles, placed_segments)
        if route is not None and len(route) >= 2:
            candidates.append(route)
    return dedupe_routes(candidates)


def relation_route_candidates(
    relation: Relation,
    endpoints_by_id: Dict[str, RouteEndpoint],
    all_boxes: List[BBox],
) -> List[List[Point]]:
    source = endpoints_by_id[relation.source]
    target = endpoints_by_id[relation.target]
    source_center = source.center
    target_center = target.center
    sx, sy = source_center
    tx, ty = target_center
    dx = tx - sx
    dy = ty - sy

    h_source_side = "right" if dx >= 0 else "left"
    h_target_side = "left" if dx >= 0 else "right"
    v_source_side = "bottom" if dy >= 0 else "top"
    v_target_side = "top" if dy >= 0 else "bottom"

    start_h = route_endpoint_port(source, h_source_side)
    end_h = route_endpoint_port(target, h_target_side)
    start_v = route_endpoint_port(source, v_source_side)
    end_v = route_endpoint_port(target, v_target_side)

    candidates: List[List[Point]] = []

    def add(points: List[Point]) -> None:
        route = simplify_points(points)
        if len(route) >= 2:
            candidates.append(route)

    if abs(dy) < 1:
        add([start_h, end_h])
    if abs(dx) < 1:
        add([start_v, end_v])

    for fraction in [0.5, 0.35, 0.65, 0.22, 0.78]:
        bend_x = start_h[0] + (end_h[0] - start_h[0]) * fraction
        add([start_h, (bend_x, start_h[1]), (bend_x, end_h[1]), end_h])

    for fraction in [0.5, 0.35, 0.65, 0.22, 0.78]:
        bend_y = start_v[1] + (end_v[1] - start_v[1]) * fraction
        add([start_v, (start_v[0], bend_y), (end_v[0], bend_y), end_v])

    add([start_h, (end_h[0], start_h[1]), end_h])
    add([start_v, (start_v[0], end_v[1]), end_v])

    for offset in [-78, 78, -126, 126, -178, 178]:
        lane_y = (sy + ty) / 2 + offset
        source_side = "top" if lane_y < sy else "bottom"
        target_side = "top" if lane_y < ty else "bottom"
        start = route_endpoint_port(source, source_side)
        end = route_endpoint_port(target, target_side)
        add([start, (start[0], lane_y), (end[0], lane_y), end])

    for offset in [-92, 92, -146, 146, -210, 210]:
        lane_x = (sx + tx) / 2 + offset
        source_side = "left" if lane_x < sx else "right"
        target_side = "left" if lane_x < tx else "right"
        start = route_endpoint_port(source, source_side)
        end = route_endpoint_port(target, target_side)
        add([start, (lane_x, start[1]), (lane_x, end[1]), end])

    if all_boxes:
        outer_top = min(box[1] for box in all_boxes) - 72
        outer_bottom = max(box[3] for box in all_boxes) + 72
        outer_left = min(box[0] for box in all_boxes) - 72
        outer_right = max(box[2] for box in all_boxes) + 72
    else:
        outer_top = min(sy, ty) - 180
        outer_bottom = max(sy, ty) + 180
        outer_left = min(sx, tx) - 180
        outer_right = max(sx, tx) + 180

    for lane_y, side in [(outer_top, "top"), (outer_bottom, "bottom")]:
        start = route_endpoint_port(source, side)
        end = route_endpoint_port(target, side)
        add([start, (start[0], lane_y), (end[0], lane_y), end])

    for lane_x, side in [(outer_left, "left"), (outer_right, "right")]:
        start = route_endpoint_port(source, side)
        end = route_endpoint_port(target, side)
        add([start, (lane_x, start[1]), (lane_x, end[1]), end])

    return candidates


def route_score(points: List[Point], obstacles: List[BBox], placed_segments: List[Segment]) -> float:
    segments = route_segments(points)
    score = route_length(points) * 0.08 + max(0, len(points) - 2) * 82
    for segment in segments:
        for box in obstacles:
            overlap = segment_box_overlap(segment, box)
            if overlap > 0:
                score += 1000 + overlap * 8
        for placed in placed_segments:
            overlap = parallel_overlap(segment, placed)
            if overlap > 0:
                score += min(overlap, 96) * 0.8 + max(0.0, overlap - 96) * 5
            elif segments_cross(segment, placed):
                score += 40
    return score


def route_relation(
    relation: Relation,
    endpoints_by_id: Dict[str, RouteEndpoint],
    object_boxes_by_id: Dict[str, BBox],
    group_label_boxes: List[BBox],
    placed_segments: List[Segment],
) -> Optional[RoutedRelation]:
    if relation.source not in endpoints_by_id or relation.target not in endpoints_by_id:
        return None

    source_endpoint = endpoints_by_id[relation.source]
    target_endpoint = endpoints_by_id[relation.target]
    relation_layer = (
        "inner"
        if source_endpoint.scope is not None and source_endpoint.scope == target_endpoint.scope
        else "outer"
    )
    all_boxes = list(object_boxes_by_id.values()) + group_label_boxes
    endpoint_owner_ids = source_endpoint.owner_object_ids | target_endpoint.owner_object_ids
    route_obstacles = [
        box
        for object_id, box in object_boxes_by_id.items()
        if object_id not in endpoint_owner_ids
    ] + group_label_boxes
    candidates = [
        route_with_endpoint_stubs(candidate, source_endpoint.center, target_endpoint.center)
        for candidate in relation_route_candidates(relation, endpoints_by_id, all_boxes)
    ]
    candidates = dedupe_routes(candidates)
    quick_score = min((route_score(candidate, route_obstacles, placed_segments) for candidate in candidates), default=math.inf)
    if quick_score >= 900:
        search_candidates = orthogonal_search_route_candidates(
            relation,
            endpoints_by_id,
            object_boxes_by_id,
            group_label_boxes,
            placed_segments,
        )
        candidates.extend(
            route_with_endpoint_stubs(candidate, source_endpoint.center, target_endpoint.center)
            for candidate in search_candidates
        )
        candidates = dedupe_routes(candidates)
    if not candidates:
        return None

    best = min(candidates, key=lambda item: route_score(item, route_obstacles, placed_segments))
    placed_segments.extend(route_segments(best))

    bubble_lines = wrap_text(relation.described, 34, 3)
    anchor_x, anchor_y = route_midpoint(best)
    anchor = (anchor_x + relation.label_offset[0], anchor_y + relation.label_offset[1])
    if bubble_lines:
        bubble_x, bubble_y, bubble_box = place_relation_label(
            bubble_lines,
            best[0],
            best[-1],
            anchor,
            all_boxes,
            [],
        )
    else:
        bubble_x, bubble_y = anchor
        bubble_box = (bubble_x, bubble_y, bubble_x, bubble_y)

    return RoutedRelation(
        relation=relation,
        points=best,
        bubble_lines=bubble_lines,
        bubble_x=bubble_x,
        bubble_y=bubble_y,
        bubble_box=bubble_box,
        dash=relation_dash(relation),
        layer=relation_layer,
    )


def render_routed_relation_line(routed: RoutedRelation) -> str:
    return "\n".join(
        [
            '<g class="relation relation-line-layer">',
            f'<path d="{path_data(routed.points)}" class="relation-line relation-line-{routed.layer}"{routed.dash} marker-end="url(#arrow-{routed.layer})" />',
            "</g>",
        ]
    )


def render_routed_relation_hover(routed: RoutedRelation) -> str:
    bubble_svg = ""
    if routed.bubble_lines:
        left, top, right, bottom = routed.bubble_box
        bubble_svg = "\n".join(
            [
                '<g class="relation-bubble">',
                f'<rect x="{left:.1f}" y="{top:.1f}" width="{right - left:.1f}" height="{bottom - top:.1f}" rx="6" class="relation-bubble-box" />',
                text_svg(routed.bubble_lines, routed.bubble_x, routed.bubble_y, "relation-bubble-text", LABEL_LINE_HEIGHT),
                "</g>",
            ]
        )

    return "\n".join(
        [
            '<g class="relation relation-hover">',
            f"<desc>{escape(routed.relation.described)}</desc>",
            f'<path d="{path_data(routed.points)}" class="relation-hitbox" />',
            f'<path d="{path_data(routed.points)}" class="relation-hover-line relation-hover-line-{routed.layer}"{routed.dash} />',
            bubble_svg,
            "</g>",
        ]
    )


def relation_label_box(lines: List[str], x: float, baseline_y: float) -> BBox:
    max_units = max((text_display_units(line) for line in lines), default=0)
    width = max_units * LABEL_UNIT_WIDTH + LABEL_PADDING_X * 2
    top = baseline_y - 12 - LABEL_PADDING_Y
    bottom = baseline_y + (len(lines) - 1) * LABEL_LINE_HEIGHT + 5 + LABEL_PADDING_Y
    return x - width / 2, top, x + width / 2, bottom


def relation_label_candidates(
    start: Tuple[float, float],
    end: Tuple[float, float],
    base: Tuple[float, float],
) -> Iterable[Tuple[float, float]]:
    start_x, start_y = start
    end_x, end_y = end
    dx = end_x - start_x
    dy = end_y - start_y
    distance = math.hypot(dx, dy) or 1
    normal_x = -dy / distance
    normal_y = dx / distance
    fractions = [0.5, 0.42, 0.58, 0.34, 0.66, 0.25, 0.75, 0.16, 0.84, 0.08, 0.92]
    normal_offsets = [
        0,
        -34,
        34,
        -58,
        58,
        -86,
        86,
        -116,
        116,
        -150,
        150,
        -190,
        190,
        -240,
        240,
        -300,
        300,
        -360,
        360,
    ]
    base_delta_x = base[0] - (start_x + dx * 0.5)
    base_delta_y = base[1] - (start_y + dy * 0.5)
    for fraction in fractions:
        line_x = start_x + dx * fraction + base_delta_x
        line_y = start_y + dy * fraction + base_delta_y
        for offset in normal_offsets:
            yield line_x + normal_x * offset, line_y + normal_y * offset


def label_collision_score(box: BBox, obstacles: List[BBox], placed_labels: List[BBox]) -> float:
    obstacle_score = sum(overlap_area(box, obstacle) for obstacle in obstacles) * 4
    label_score = sum(overlap_area(box, label) for label in placed_labels)
    return obstacle_score + label_score


def place_relation_label(
    lines: List[str],
    start: Tuple[float, float],
    end: Tuple[float, float],
    base: Tuple[float, float],
    obstacles: List[BBox],
    placed_labels: List[BBox],
) -> Tuple[float, float, BBox]:
    best: Optional[Tuple[float, float, BBox, float]] = None
    best_without_obstacle: Optional[Tuple[float, float, BBox, float]] = None
    for x, center_y in relation_label_candidates(start, end, base):
        baseline_y = center_y - (len(lines) - 1) * (LABEL_LINE_HEIGHT / 2) + 5
        box = relation_label_box(lines, x, baseline_y)
        obstacle_score = sum(overlap_area(box, obstacle) for obstacle in obstacles)
        label_score = sum(overlap_area(box, label) for label in placed_labels)
        if obstacle_score == 0 and label_score == 0:
            return x, baseline_y, box
        distance = math.hypot(x - base[0], center_y - base[1])
        if obstacle_score == 0:
            no_obstacle_score = label_score + distance * 0.08
            if best_without_obstacle is None or no_obstacle_score < best_without_obstacle[3]:
                best_without_obstacle = (x, baseline_y, box, no_obstacle_score)
        total_score = obstacle_score * 10 + label_score + distance * 0.08
        if best is None or total_score < best[3]:
            best = (x, baseline_y, box, total_score)
    if best_without_obstacle is not None:
        return best_without_obstacle[0], best_without_obstacle[1], best_without_obstacle[2]
    if best is None:
        fallback_y = base[1] - (len(lines) - 1) * (LABEL_LINE_HEIGHT / 2) + 5
        fallback_box = relation_label_box(lines, base[0], fallback_y)
        return base[0], fallback_y, fallback_box
    return best[0], best[1], best[2]


def object_parent_scopes(groups: List[DiagramGroup]) -> Dict[str, str]:
    parent_by_id: Dict[str, str] = {}
    for group in groups:
        for child_id in group.contains:
            parent_by_id.setdefault(child_id, group.group_id)
    return parent_by_id


def build_route_endpoints(
    positions: Dict[str, Point],
    objects_by_id: Dict[str, DiagramObject],
    groups: List[DiagramGroup],
    group_frames_by_id: Dict[str, List[BBox]],
) -> Dict[str, RouteEndpoint]:
    parent_by_id = object_parent_scopes(groups)
    endpoints: Dict[str, RouteEndpoint] = {}
    for object_id, item in objects_by_id.items():
        if object_id not in positions:
            continue
        center = positions[object_id]
        endpoints[object_id] = RouteEndpoint(
            endpoint_id=object_id,
            kind="object",
            center=center,
            box=object_box(item, *center, padding=0),
            scope=parent_by_id.get(object_id),
            owner_object_ids={object_id},
        )

    for group in groups:
        frames = group_frames_by_id.get(group.group_id, [])
        if not frames:
            continue
        group_box = union_box(frames)
        endpoints[group.group_id] = RouteEndpoint(
            endpoint_id=group.group_id,
            kind="group",
            center=box_center(group_box),
            box=group_box,
            scope=None,
            owner_object_ids=set(),
        )
        for interface in group.interfaces:
            endpoint_id = f"{group.group_id}.{interface.interface_id}"
            endpoints[endpoint_id] = RouteEndpoint(
                endpoint_id=endpoint_id,
                kind="interface",
                center=box_center(group_box),
                box=group_box,
                scope=None,
                owner_object_ids=set(),
            )
    return endpoints


def render_svg(diagram: Diagram, link_base: Optional[Path] = None) -> str:
    positions = object_positions(diagram.objects)
    objects_by_id = {item.object_id: item for item in diagram.objects}
    group_frames_by_id = {
        group.group_id: group_frame_bounds(group, positions, objects_by_id)
        for group in diagram.groups
    }
    endpoints_by_id = build_route_endpoints(
        positions,
        objects_by_id,
        diagram.groups,
        group_frames_by_id,
    )
    group_bounds_values = [bounds for frames in group_frames_by_id.values() for bounds in frames]
    object_boxes_by_id = {
        item.object_id: object_box(item, *positions[item.object_id])
        for item in diagram.objects
        if item.object_id in positions
    }
    group_label_boxes = [
        padded_box(group_label_box(frames[0]), 6)
        for frames in group_frames_by_id.values()
        if frames
    ]
    placed_segments: List[Segment] = []
    routed_relations: List[RoutedRelation] = []
    for relation in diagram.relations:
        routed = route_relation(
            relation,
            endpoints_by_id,
            object_boxes_by_id,
            group_label_boxes,
            placed_segments,
        )
        if routed is not None:
            routed_relations.append(routed)

    extent_boxes: List[BBox] = group_bounds_values + list(object_boxes_by_id.values())
    for routed in routed_relations:
        route_xs = [point[0] for point in routed.points]
        route_ys = [point[1] for point in routed.points]
        if route_xs and route_ys:
            extent_boxes.append((min(route_xs) - 18, min(route_ys) - 18, max(route_xs) + 18, max(route_ys) + 18))
        if routed.bubble_lines:
            extent_boxes.append(routed.bubble_box)

    if extent_boxes:
        view_left = min(0.0, min(box[0] for box in extent_boxes) - 72)
        view_top = min(0.0, min(box[1] for box in extent_boxes) - 72)
        view_right = max(box[2] for box in extent_boxes) + VIEWBOX_PADDING_X
        view_bottom = max(box[3] for box in extent_boxes) + VIEWBOX_PADDING_Y
        view_width = view_right - view_left
        view_height = view_bottom - view_top
    else:
        view_left = 0.0
        view_top = 0.0
        view_width = 600.0
        view_height = 300.0

    groups_svg = "\n".join(render_group(item, positions, objects_by_id, link_base) for item in diagram.groups)
    relation_lines_svg = "\n".join(render_routed_relation_line(item) for item in routed_relations)
    objects_svg = "\n".join(
        render_object(item, *positions[item.object_id], link_base)
        for item in diagram.objects
        if item.object_id in positions
    )
    relation_hover_svg = "\n".join(render_routed_relation_hover(item) for item in routed_relations)

    return f"""<svg class="diagram" style="min-width: {view_width:.0f}px;" viewBox="{view_left:.0f} {view_top:.0f} {view_width:.0f} {view_height:.0f}" role="img" aria-labelledby="diagram-title diagram-desc">
  <title id="diagram-title">{escape(diagram.meta.get("name", diagram.path.stem))}</title>
  <desc id="diagram-desc">{escape(diagram.meta.get("described", ""))}</desc>
  <defs>
{render_svg_styles()}
    <marker id="arrow-inner" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" class="arrow" />
    </marker>
    <marker id="arrow-outer" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="10" markerHeight="10" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" class="arrow" />
    </marker>
  </defs>
  {groups_svg}
  {relation_lines_svg}
  {objects_svg}
  {relation_hover_svg}
</svg>"""


def render_html(diagram: Diagram, link_base: Optional[Path] = None) -> str:
    warning_items = "\n".join(f"<li>{escape(item)}</li>" for item in diagram.warnings)
    warnings_html = ""
    if warning_items:
        warnings_html = f"""
      <section class="warnings">
        <h2>Warnings</h2>
        <ul>{warning_items}</ul>
      </section>"""

    return f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(diagram.meta.get("name", diagram.path.stem))}</title>
    <style>
      :root {{
        color-scheme: light;
        --ink: #1e293b;
        --muted: #64748b;
        --line: #111827;
        --paper: #ffffff;
        --warning-bg: #fff7ed;
        --warning-line: #fb923c;
      }}
      body {{
        margin: 0;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: #eef2f7;
        color: var(--ink);
      }}
      main {{
        max-width: none;
        margin: 0 auto;
        padding: 32px 24px 44px;
      }}
      header {{
        max-width: 1120px;
        margin-bottom: 20px;
      }}
      h1 {{
        margin: 0 0 8px;
        font-size: 28px;
        line-height: 1.2;
        letter-spacing: 0;
      }}
      p {{
        margin: 0;
        color: var(--muted);
        line-height: 1.6;
      }}
      .canvas {{
        overflow: auto;
        background: var(--paper);
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        box-shadow: 0 18px 55px rgba(30, 41, 59, 0.12);
      }}
      .diagram {{
        display: block;
        width: 100%;
        height: auto;
      }}
      .node-shape {{
        stroke-width: 1.6;
      }}
      .node-link,
      .group-link {{
        cursor: pointer;
        text-decoration: none;
      }}
      .node-link:hover .node-shape,
      .node-link:focus .node-shape,
      .group-link:hover .group-shape,
      .group-link:focus .group-shape {{
        stroke-width: 2.6;
      }}
      .node-line {{
        fill: none;
        stroke-width: 1.6;
      }}
      .group-shape {{
        fill: #eef2ff;
        stroke: #4f46e5;
        stroke-width: 1.8;
        stroke-dasharray: 10 7;
      }}
      .group-title {{
        fill: #312e81;
        font-size: 14px;
        font-weight: 800;
      }}
      .group-description {{
        fill: #4338ca;
        font-size: 12px;
        font-weight: 600;
      }}
      .node-title {{
        fill: var(--ink);
        font-size: 15px;
        font-weight: 700;
      }}
      .node-description {{
        fill: var(--muted);
        font-size: 12px;
      }}
      .relation-line {{
        fill: none;
        stroke: var(--line);
        stroke-width: 2.8;
      }}
      .relation-line-inner {{
        stroke-width: 1.5;
      }}
      .relation-line-outer {{
        stroke-width: 3.4;
      }}
      .relation-hitbox {{
        fill: none;
        stroke: transparent;
        stroke-width: 18;
        pointer-events: stroke;
        cursor: help;
      }}
      .relation-hover-line {{
        fill: none;
        stroke: var(--line);
        stroke-width: 4.4;
        opacity: 0;
        pointer-events: none;
      }}
      .relation-hover-line-inner {{
        stroke-width: 2.2;
      }}
      .relation-hover-line-outer {{
        stroke-width: 5.2;
      }}
      .relation-hover:hover .relation-hover-line {{
        opacity: 0.75;
      }}
      .relation-bubble {{
        opacity: 0;
        transition: opacity 120ms ease;
        pointer-events: none;
      }}
      .relation-hover:hover .relation-bubble {{
        opacity: 1;
      }}
      .relation-bubble-box {{
        fill: #ffffff;
        stroke: #94a3b8;
        stroke-width: 1;
      }}
      .relation-bubble-text {{
        fill: #0f172a;
        font-size: 12px;
        font-weight: 650;
        pointer-events: none;
      }}
      .arrow {{ fill: var(--line); }}
      .warnings {{
        margin-top: 18px;
        padding: 12px 14px;
        border-left: 4px solid var(--warning-line);
        background: var(--warning-bg);
        border-radius: 6px;
      }}
      .warnings h2 {{
        margin: 0 0 8px;
        font-size: 15px;
      }}
      .warnings ul {{
        margin: 0;
        padding-left: 20px;
      }}
    </style>
  </head>
  <body>
    <main>
      <header>
        <h1>{escape(diagram.meta.get("name", diagram.path.stem))}</h1>
        <p>{escape(diagram.meta.get("described", ""))}</p>
      </header>
      <section class="canvas">
        {render_svg(diagram, link_base)}
      </section>{warnings_html}
    </main>
  </body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render Architecture Graph JSON to HTML.")
    parser.add_argument("input", type=Path, help="Input .arch.json file")
    parser.add_argument("-o", "--output", type=Path, help="Output HTML file")
    parser.add_argument("--svg-output", type=Path, help="Optional standalone SVG output file")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = args.input
    if not input_path.name.endswith(".arch.json"):
        raise SystemExit("Input file must use the .arch.json suffix.")

    output_path = args.output or input_path.with_suffix(".html")
    diagram = load_graph(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_html(diagram, output_path), encoding="utf-8")
    print(f"Rendered {input_path} -> {output_path}")
    if args.svg_output:
        args.svg_output.parent.mkdir(parents=True, exist_ok=True)
        args.svg_output.write_text(render_svg(diagram, args.svg_output), encoding="utf-8")
        print(f"Rendered {input_path} -> {args.svg_output}")
    for warning in diagram.warnings:
        print(f"Warning: {warning}")


if __name__ == "__main__":
    main()
