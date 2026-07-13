"""PPT 生成节点：生成主持人手卡式演示文稿，面向活动现场流程推进"""

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

# ── 配色方案 ──────────────────────────────────────────────────
C_PRIMARY = RGBColor(0x1A, 0x56, 0xDB)       # 主蓝
C_DARK = RGBColor(0x2D, 0x2D, 0x2D)           # 深灰
C_LIGHT = RGBColor(0xF5, 0xF7, 0xFA)          # 浅灰蓝
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C_ACCENT = RGBColor(0xE8, 0x3E, 0x8C)         # 粉色强调
C_SUBTLE = RGBColor(0x9C, 0xA3, 0xAF)         # 辅助灰
C_GREEN = RGBColor(0x10, 0xB9, 0x81)          # 绿色
C_ORANGE = RGBColor(0xF5, 0x9E, 0x0B)         # 橙色

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


def _multiline_textbox(slide, l, t, w, h, lines, size=16, color=C_DARK, spacing=0.4):
    """多行文本框，每行独立段落。"""
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.font.name = "Microsoft YaHei"
        p.space_after = Pt(spacing * 6)
    return tb


def _build_slide_header(slide, title, subtitle=""):
    """统一顶部标题栏。"""
    _rect(slide, Inches(0), Inches(0), Inches(10), Inches(1.0), C_PRIMARY)
    _textbox(slide, Inches(0.5), Inches(0.1), Inches(9), Inches(0.7),
             title, size=28, bold=True, color=C_WHITE)
    if subtitle:
        _textbox(slide, Inches(0.5), Inches(1.1), Inches(9), Inches(0.4),
                 subtitle, size=13, color=C_SUBTLE)
    _bg(slide, C_LIGHT)


def _parse_schedule_segments(schedule: str) -> list[dict]:
    """从日程文本中提取环节列表：[{time, activity, detail}]。"""
    segments = []
    for line in schedule.split("\n"):
        line = line.strip()
        if not line:
            continue
        # 匹配 "时间：内容" 或 "时间 内容" 或 "- 内容"
        m = re.match(r"^[-\d:：\s]*(\d{1,2}[:：]\d{2})[-~至到]?\s*(\d{1,2}[:：]\d{2})?", line)
        if m:
            time_str = m.group(0).strip("- ").strip()[:12]
            rest = line[m.end():].strip("- ").strip()
            segments.append({"time": time_str, "activity": rest or line, "detail": ""})
        else:
            # 无时间标记的行，追加到上一段的 detail
            if segments:
                segments[-1]["detail"] += " " + line
            else:
                segments.append({"time": "", "activity": line, "detail": ""})
    return segments


def _parse_task_roles(task_json: str) -> list[str]:
    """从任务拆解 JSON 中提取责任人分配。"""
    try:
        parsed = json.loads(task_json)
        roles = parsed.get("role_assignment", [])
        lines = []
        for r in roles:
            tasks = r.get("tasks", [])
            count = r.get("count", len(tasks))
            task_preview = "、".join(tasks[:2])
            if len(tasks) > 2:
                task_preview += f" 等{len(tasks)}项"
            lines.append(f"【{r['role']}】×{count}  —  {task_preview}")
        if not lines and parsed.get("tasks"):
            # 降级：从 tasks 提取
            seen_roles = {}
            for t in parsed["tasks"]:
                role = t.get("responsible_role", "待分配")
                name = t.get("task_name", "")
                seen_roles.setdefault(role, []).append(name)
            for role, tasks in seen_roles.items():
                lines.append(f"【{role}】—  {'、'.join(tasks[:3])}")
        return lines
    except (json.JSONDecodeError, TypeError):
        return []


def ppt_agent(state: ActivityState) -> ActivityState:
    """生成面向主持人现场推进流程的手卡式 PPT。"""
    if not state.get("need_ppt", True):
        state["ppt_path"] = None
        state["log"].append("【PPT】用户选择不生成 PPT，已跳过")
        print("[PPT] 用户选择不生成 PPT，已跳过", flush=True)
        return state

    plan = state.get("activity_plan", "")
    schedule = state.get("schedule", "")
    host_script = state.get("host_script", "")
    task_json = state.get("task_execution_plan", "")

    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # ── 提取标题 ─────────────────────────────────────────────
    title_text = "校园活动"
    for line in plan.split("\n"):
        line_s = line.strip("# ").strip()
        if "主题" in line_s and len(line_s) < 30:
            title_text = line_s.split("主题")[-1].strip(""""""' ')
            break
        if len(line_s) > 3 and len(line_s) < 25:
            title_text = line_s

    # ──────────────────────────────────────────────────────────
    # Slide 1: 封面
    # ──────────────────────────────────────────────────────────
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _bg(s, C_PRIMARY)
    _rect(s, Inches(0), Inches(3.2), Inches(10), Inches(0.04), C_ACCENT)
    _textbox(s, Inches(0.8), Inches(1.8), Inches(8.4), Inches(1.2),
             title_text, size=38, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    today = datetime.now().strftime("%Y-%m-%d")
    _textbox(s, Inches(0.8), Inches(3.6), Inches(8.4), Inches(0.6),
             f"主持人手卡  |  {today}", size=16, color=C_WHITE, align=PP_ALIGN.CENTER)
    _textbox(s, Inches(0.8), Inches(4.3), Inches(8.4), Inches(0.5),
             "按流程推进，每页对应一个环节", size=13, color=C_SUBTLE, align=PP_ALIGN.CENTER)

    # ──────────────────────────────────────────────────────────
    # Slide 2: 流程总览（时间线一览）
    # ──────────────────────────────────────────────────────────
    segments = _parse_schedule_segments(schedule)
    if not segments:
        segments = [{"time": "", "activity": "（日程待生成）", "detail": ""}]

    s = prs.slides.add_slide(prs.slide_layouts[6])
    _build_slide_header(s, "活动流程总览", "全程时间线一览")

    y = Inches(1.6)
    for i, seg in enumerate(segments[:7]):
        color = C_PRIMARY if i % 2 == 0 else C_GREEN
        # 时间标签
        _rect(s, Inches(0.5), y, Inches(1.6), Inches(0.45), color)
        _textbox(s, Inches(0.5), y + Inches(0.03), Inches(1.6), Inches(0.4),
                 seg["time"] or f"环节{i+1}", size=14, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
        # 活动名称
        _textbox(s, Inches(2.3), y + Inches(0.03), Inches(7.2), Inches(0.4),
                 seg["activity"][:40], size=15, color=C_DARK)
        y += Inches(0.6)

    if len(segments) > 7:
        _textbox(s, Inches(0.5), y, Inches(9), Inches(0.4),
                 f"... 共 {len(segments)} 个环节", size=13, color=C_SUBTLE)

    # ──────────────────────────────────────────────────────────
    # Slide 3+: 各环节详情（每环节一页）
    # ──────────────────────────────────────────────────────────
    for i, seg in enumerate(segments[:8]):
        s = prs.slides.add_slide(prs.slide_layouts[6])
        _build_slide_header(s, f"环节 {i+1}：{seg['activity'][:25]}", seg["time"])

        lines = []
        lines.append(f"⏱ 时间：{seg['time']}")
        lines.append(f"📋 内容：{seg['activity']}")
        if seg.get("detail"):
            lines.append(f"📌 说明：{seg['detail'][:80]}")

        # 从主持稿中提取相关话术
        if host_script and seg["time"]:
            # 找主持稿中对应时间附近的内容
            script_lines = [l.strip() for l in host_script.split("\n") if l.strip()]
            matched = [l for l in script_lines if seg["time"][:5] in l or seg["activity"][:6] in l]
            if matched:
                lines.append(f"🎤 主持提示：{matched[0][:60]}")
        if not lines:
            lines.append("（等待主持人根据现场情况灵活发挥）")

        _multiline_textbox(s, Inches(0.6), Inches(1.5), Inches(8.8), Inches(5),
                           lines, size=16, color=C_DARK, spacing=0.5)

        # 底部提示
        _textbox(s, Inches(0.6), Inches(6.5), Inches(8.8), Inches(0.5),
                 "💡 提示：可根据现场气氛适当调整环节时长", size=12, color=C_ORANGE)

    # ──────────────────────────────────────────────────────────
    # 人员分工页
    # ──────────────────────────────────────────────────────────
    task_lines = _parse_task_roles(task_json)
    if task_lines:
        s = prs.slides.add_slide(prs.slide_layouts[6])
        _build_slide_header(s, "现场人员分工", "各环节责任人一览")
        _multiline_textbox(s, Inches(0.6), Inches(1.5), Inches(8.8), Inches(5),
                           task_lines, size=16, color=C_DARK, spacing=0.5)

    # ──────────────────────────────────────────────────────────
    # 注意事项页
    # ──────────────────────────────────────────────────────────
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _build_slide_header(s, "现场注意事项", "主持人提醒")
    notes = [
        "✅ 提前到场检查设备（话筒、投影、音响）",
        "✅ 确认各环节责任人到位",
        "✅ 控制各环节时间，灵活调整",
        "✅ 突发情况及时与总负责人沟通",
        "✅ 活动结束后组织合影留念",
        "✅ 引导参与者填写反馈问卷",
    ]
    _multiline_textbox(s, Inches(0.6), Inches(1.5), Inches(8.8), Inches(5),
                       notes, size=16, color=C_DARK, spacing=0.5)

    # ── 保存 ─────────────────────────────────────────────────
    PPT_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"主持人手卡_{ts}.pptx"
    path = PPT_DIR / filename
    prs.save(str(path))
    state["ppt_path"] = str(path)
    state["log"].append(f"【PPT】主持人手卡已生成：{path}")
    print(f"[PPT] 主持人手卡已生成：{path}", flush=True)

    return state