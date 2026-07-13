"""PPT 生成节点：生成两份演示文稿 — 主持人手卡 + 活动现场展示PPT"""

import json
import re
from datetime import datetime
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

from models import ActivityState

# ── 配色 ──────────────────────────────────────────────────────
C_BLUE = RGBColor(0x1A, 0x56, 0xDB)
C_DARK = RGBColor(0x1E, 0x29, 0x3B)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C_LIGHT = RGBColor(0xF1, 0xF5, 0xF9)
C_ACCENT = RGBColor(0xE8, 0x3E, 0x8C)
C_GRAY = RGBColor(0x94, 0xA3, 0xB8)
C_GREEN = RGBColor(0x10, 0xB9, 0x81)
C_ORANGE = RGBColor(0xF5, 0x9E, 0x0B)
C_GOLD = RGBColor(0xF5, 0x9E, 0x0B)
C_TEAL = RGBColor(0x14, 0xB8, 0xA6)
C_PURPLE = RGBColor(0x8B, 0x5C, 0xF6)

PPT_DIR = Path("PPT演示文稿")


def _bg(slide, color):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def _rect(slide, l, t, w, h, color):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    s.fill.solid()
    s.fill.fore_color.rgb = color
    s.line.fill.background()
    return s


def _textbox(slide, l, t, w, h, text, size=18, bold=False, color=C_DARK, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = "Microsoft YaHei"
    p.alignment = align
    return tb


def _ml(slide, l, t, w, h, lines, size=16, color=C_DARK, spacing=0.35):
    """多行文本框。"""
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.font.name = "Microsoft YaHei"
        p.space_after = Pt(spacing * 6)
    return tb


def _header(slide, title, subtitle=""):
    """统一标题栏。"""
    _rect(slide, Inches(0), Inches(0), Inches(10), Inches(0.9), C_BLUE)
    _textbox(slide, Inches(0.5), Inches(0.08), Inches(9), Inches(0.7),
             title, size=26, bold=True, color=C_WHITE)
    if subtitle:
        _textbox(slide, Inches(0.5), Inches(1.0), Inches(9), Inches(0.35),
                 subtitle, size=12, color=C_GRAY)


def _parse_segments(schedule: str) -> list[dict]:
    """从日程文本提取环节列表。"""
    segments = []
    for line in schedule.split("\n"):
        line = line.strip()
        if not line:
            continue
        m = re.match(r"^[-\d:：\s]*(\d{1,2}[:：]\d{2})[-~至到]?\s*(\d{1,2}[:：]\d{2})?", line)
        if m:
            time_str = m.group(0).strip("- ").strip()[:12]
            rest = line[m.end():].strip("- ").strip()
            segments.append({"time": time_str, "activity": rest or line, "detail": ""})
        else:
            if segments:
                segments[-1]["detail"] += " " + line
            else:
                segments.append({"time": "", "activity": line, "detail": ""})
    return segments


def _find_title(plan: str) -> str:
    for line in plan.split("\n"):
        s = line.strip("# ").strip()
        if "主题" in s and len(s) < 30:
            t = s.split("主题")[-1].strip(""""""' ')
            if t:
                return t
        if 3 < len(s) < 25:
            return s
    return "校园活动"


def _get_confirmed_info(state: dict) -> dict:
    confirmed = state.get("poster_info_confirmed", "{}")
    try:
        return json.loads(confirmed)
    except (json.JSONDecodeError, TypeError):
        return {}


# ══════════════════════════════════════════════════════════════
# PPT-A：主持人手卡（紧凑·流程导向·含主要角色）
# ══════════════════════════════════════════════════════════════
def _build_host_card(prs: Presentation, state: dict) -> str:
    plan = state.get("activity_plan", "")
    schedule = state.get("schedule", "")
    host_script = state.get("host_script", "")
    info = _get_confirmed_info(state)

    title_text = _find_title(plan)
    segments = _parse_segments(schedule) or [{"time": "", "activity": "（日程待生成）", "detail": ""}]

    # ── Slide 1: 封面 ──
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _bg(s, C_BLUE)
    _rect(s, Inches(0), Inches(3.0), Inches(10), Inches(0.04), C_ACCENT)
    _textbox(s, Inches(0.5), Inches(1.5), Inches(9), Inches(1.2),
             title_text, size=36, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    _textbox(s, Inches(0.5), Inches(3.4), Inches(9), Inches(0.5),
             f"主持人手卡  |  {info.get('date', '')} {info.get('time', '')}",
             size=16, color=C_WHITE, align=PP_ALIGN.CENTER)
    if info.get("venue"):
        _textbox(s, Inches(0.5), Inches(4.0), Inches(9), Inches(0.5),
                 f"📍 {info['venue']}", size=14, color=C_GRAY, align=PP_ALIGN.CENTER)

    # ── Slide 2: 流程总览 —— 一目了然的时间线 ──
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _header(s, "📋 活动流程总览")
    y = Inches(1.3)
    for i, seg in enumerate(segments[:8]):
        c = C_BLUE if i % 2 == 0 else C_TEAL
        _rect(s, Inches(0.4), y, Inches(1.5), Inches(0.42), c)
        _textbox(s, Inches(0.4), y + Inches(0.03), Inches(1.5), Inches(0.36),
                 seg["time"] or f"环节{i+1}", size=13, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
        _textbox(s, Inches(2.1), y + Inches(0.03), Inches(7.4), Inches(0.36),
                 seg["activity"][:35], size=14, color=C_DARK)
        y += Inches(0.55)

    # ── Slide 3+: 每环节一页（时间 + 内容 + 主持提示 + 主要角色） ──
    for i, seg in enumerate(segments[:8]):
        s = prs.slides.add_slide(prs.slide_layouts[6])
        _header(s, f"环节 {i+1}：{seg['activity'][:20]}", seg["time"])

        lines = []
        lines.append(f"⏱ 时间：{seg['time']}")
        lines.append(f"📋 内容：{seg['activity']}")
        lines.append("")

        if seg.get("detail"):
            lines.append(f"📌 {seg['detail'][:80]}")

        # 主持话术
        if host_script:
            script_lines = [l.strip() for l in host_script.split("\n") if l.strip()]
            matched = [l for l in script_lines
                       if seg["time"][:5] in l or seg["activity"][:6] in l]
            if matched:
                lines.append("")
                lines.append(f"🎤 主持词：{matched[0][:70]}")

        lines.append("")
        lines.append(f"💡 提示：注意控制时间，灵活过渡")

        _ml(s, Inches(0.5), Inches(1.4), Inches(9), Inches(5.5),
            lines, size=15, color=C_DARK, spacing=0.4)

    # ── 主要角色页（只含上台/关键角色，不含负责人） ──
    # 从 info 提取主要角色信息
    role_lines = []
    if info.get("organizer") and info["organizer"] != "待定":
        role_lines.append(f"🏢 主办单位：{info['organizer']}")
    if info.get("target_audience") and info["target_audience"] != "待定":
        role_lines.append(f"👥 面向对象：{info['target_audience']}")
    role_lines += [
        "",
        "🎤 本场主要角色",
        "   主持人 — 全场串场、氛围调动",
        "   活动总负责人 — 统筹协调、应急处理",
        "   技术支持 — 音响/灯光/投影操作",
    ]
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _header(s, "主要角色")
    _ml(s, Inches(0.5), Inches(1.3), Inches(9), Inches(5.5),
        role_lines, size=15, color=C_DARK, spacing=0.35)

    # ── 现场提醒页 ──
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _header(s, "⏰ 现场提醒")
    _ml(s, Inches(0.5), Inches(1.3), Inches(9), Inches(5.5), [
        "🔹 提前 30 分钟到场，检查设备（话筒·投影·音响）",
        "🔹 确认各环节准备就绪",
        "🔹 控制每个环节时长，必要时灵活调整",
        "🔹 突发情况及时与总负责人沟通",
        "🔹 活动结束后组织合影留念",
    ], size=15, color=C_DARK, spacing=0.4)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"主持人手卡_{ts}.pptx"
    path = PPT_DIR / filename
    prs.save(str(path))
    return str(path)


# ══════════════════════════════════════════════════════════════
# PPT-B：活动现场展示PPT（大屏投影用）
# ══════════════════════════════════════════════════════════════
def _build_display_ppt(prs: Presentation, state: dict) -> str:
    plan = state.get("activity_plan", "")
    schedule = state.get("schedule", "")
    info = _get_confirmed_info(state)

    title_text = _find_title(plan)
    segments = _parse_segments(schedule) or [{"time": "", "activity": "（日程待生成）", "detail": ""}]

    # ── Slide 1: 封面 ──
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _bg(s, C_DARK)
    # 装饰线条
    _rect(s, Inches(0), Inches(3.0), Inches(10), Inches(0.04), C_BLUE)
    _rect(s, Inches(0), Inches(3.1), Inches(10), Inches(0.02), C_ACCENT)
    # 大字标题
    _textbox(s, Inches(1), Inches(1.5), Inches(8), Inches(1.5),
             title_text, size=44, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    # 信息
    info_lines = []
    if info.get("date"):
        info_lines.append(f"📅 {info['date']}")
    if info.get("time"):
        info_lines.append(f"⏰ {info['time']}")
    if info.get("venue"):
        info_lines.append(f"📍 {info['venue']}")
    if info_lines:
        _textbox(s, Inches(1), Inches(3.5), Inches(8), Inches(0.8),
                 "  |  ".join(info_lines), size=18, color=C_GRAY, align=PP_ALIGN.CENTER)
    # 主办方
    if info.get("organizer") and info["organizer"] != "待定":
        _textbox(s, Inches(1), Inches(4.5), Inches(8), Inches(0.5),
                 f"主办：{info['organizer']}", size=14, color=C_GRAY, align=PP_ALIGN.CENTER)

    # ── Slide 2: 欢迎页 ──
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _bg(s, C_BLUE)
    _textbox(s, Inches(1), Inches(2.0), Inches(8), Inches(1.2),
             "欢迎参加", size=24, color=C_WHITE, align=PP_ALIGN.CENTER)
    _textbox(s, Inches(1), Inches(3.0), Inches(8), Inches(1.5),
             title_text, size=40, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    _textbox(s, Inches(1), Inches(4.8), Inches(8), Inches(0.6),
             "请将手机调至静音，享受本次活动", size=16, color=C_GRAY, align=PP_ALIGN.CENTER)

    # ── Slide 3: 流程总览 ──
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _bg(s, C_LIGHT)
    _rect(s, Inches(0), Inches(0), Inches(10), Inches(0.9), C_BLUE)
    _textbox(s, Inches(0.5), Inches(0.1), Inches(9), Inches(0.7),
             "活动流程", size=28, bold=True, color=C_WHITE)

    y = Inches(1.3)
    for i, seg in enumerate(segments[:7]):
        c = C_BLUE if i % 2 == 0 else C_TEAL
        _rect(s, Inches(0.6), y, Inches(1.8), Inches(0.5), c)
        _textbox(s, Inches(0.6), y + Inches(0.05), Inches(1.8), Inches(0.4),
                 seg["time"] or f"0{i+1}", size=15, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
        _textbox(s, Inches(2.6), y + Inches(0.05), Inches(7), Inches(0.4),
                 seg["activity"][:40], size=16, bold=True, color=C_DARK)
        y += Inches(0.65)

    # ── Slide 4+: 每环节过渡页（大屏展示） ──
    for i, seg in enumerate(segments[:6]):
        s = prs.slides.add_slide(prs.slide_layouts[6])
        # 左半色块
        _rect(s, Inches(0), Inches(0), Inches(4), Inches(7.5), C_BLUE)
        # 环节编号
        _textbox(s, Inches(0.5), Inches(1.5), Inches(3), Inches(0.8),
                 f"0{i+1}", size=48, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
        # 环节名称
        _textbox(s, Inches(0.5), Inches(2.5), Inches(3), Inches(0.6),
                 seg["activity"][:15], size=22, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
        # 时间
        if seg["time"]:
            _textbox(s, Inches(0.5), Inches(3.3), Inches(3), Inches(0.5),
                     seg["time"], size=14, color=C_GRAY, align=PP_ALIGN.CENTER)
        # 右侧大字
        _textbox(s, Inches(4.5), Inches(2.5), Inches(5), Inches(2),
                 seg["activity"][:20], size=36, bold=True, color=C_DARK, align=PP_ALIGN.CENTER)

    # ── 结尾页 ──
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _bg(s, C_DARK)
    _rect(s, Inches(0), Inches(3.5), Inches(10), Inches(0.04), C_BLUE)
    _textbox(s, Inches(1), Inches(2.0), Inches(8), Inches(1.5),
             "感谢参与", size=44, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    if info.get("organizer") and info["organizer"] != "待定":
        _textbox(s, Inches(1), Inches(4.0), Inches(8), Inches(0.6),
                 f"主办：{info['organizer']}", size=16, color=C_GRAY, align=PP_ALIGN.CENTER)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"活动现场展示_{ts}.pptx"
    path = PPT_DIR / filename
    prs.save(str(path))
    return str(path)


# ══════════════════════════════════════════════════════════════
# 入口
# ══════════════════════════════════════════════════════════════
def ppt_agent(state: ActivityState) -> ActivityState:
    """生成两份 PPT：主持人手卡 + 活动现场展示PPT。"""
    PPT_DIR.mkdir(exist_ok=True)

    # ── PPT-A：主持人手卡 ──
    print(f"[PPT] 正在生成主持人手卡...", flush=True)
    prs_a = Presentation()
    prs_a.slide_width = Inches(10)
    prs_a.slide_height = Inches(7.5)
    path_a = _build_host_card(prs_a, state)
    print(f"[PPT] 主持人手卡已生成：{path_a}", flush=True)

    # ── PPT-B：活动现场展示PPT ──
    print(f"[PPT] 正在生成活动现场展示PPT...", flush=True)
    prs_b = Presentation()
    prs_b.slide_width = Inches(10)
    prs_b.slide_height = Inches(7.5)
    path_b = _build_display_ppt(prs_b, state)

    # 合并路径信息
    state["ppt_path"] = f"{path_a}\n    🖥️  {path_b}"
    state["log"].append(f"【PPT】主持人手卡 + 活动现场展示PPT 已生成")
    print(f"[PPT] 活动现场展示PPT已生成：{path_b}", flush=True)

    return state