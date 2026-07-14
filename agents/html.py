"""HTML 生成节点：生成微信公众号风格的活动总结推文"""

import json
from datetime import datetime
from pathlib import Path

from models import ActivityState
from config import llm

HTML_DIR = Path("公众号推文")


def _css() -> str:
    return """
*{margin:0;padding:0;box-sizing:border-box}
body{background:#F5F5F5;font-family:-apple-system,'Microsoft YaHei','PingFang SC',sans-serif;padding:20px 0}
.article{max-width:640px;margin:0 auto;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.06)}
.banner{width:100%;height:auto;display:block}
.header{padding:30px 24px 20px;text-align:center}
.header h1{font-size:22px;font-weight:700;color:#1a1a1a;line-height:1.5;margin-bottom:12px}
.header .meta{font-size:13px;color:#999}
.header .meta span{margin:0 8px}
.section{padding:10px 24px 20px}
.section h2{font-size:17px;font-weight:700;color:#1a1a1a;margin-bottom:12px;padding-left:12px;border-left:3px solid #1A56DB}
.section p{font-size:15px;color:#333;line-height:1.8;margin-bottom:10px;text-align:justify}
.section .highlight{background:#F0F4FF;padding:16px;border-radius:8px;margin:12px 0}
.section .highlight p{font-size:14px;color:#555;margin-bottom:4px}
.timeline{padding:0 24px 20px}
.timeline-item{display:flex;margin-bottom:16px;align-items:flex-start}
.timeline-time{min-width:80px;font-size:14px;font-weight:600;color:#1A56DB;padding-top:2px}
.timeline-dot{width:10px;height:10px;border-radius:50%;background:#1A56DB;margin:6px 16px 0 0;flex-shrink:0}
.timeline-content{font-size:14px;color:#333;line-height:1.6}
.poster-box{padding:0 24px 20px;text-align:center}
.poster-box img{max-width:100%;border-radius:8px;box-shadow:0 4px 16px rgba(0,0,0,0.1)}
.poster-box .caption{font-size:12px;color:#999;margin-top:8px}
.footer{padding:24px;text-align:center;background:#FAFAFA;border-top:1px solid #EEE}
.footer p{font-size:13px;color:#999;line-height:1.8}
.footer .org{font-size:14px;font-weight:600;color:#333;margin-bottom:4px}
.divider{height:1px;background:linear-gradient(90deg,transparent,#E0E0E0,transparent);margin:0 24px}
"""


def _build_html(state: dict) -> str:
    plan = state.get("activity_plan", "")
    schedule = state.get("schedule", "")
    notice = state.get("notice_text", "")
    poster_path = state.get("poster_image", "")
    tweet = state.get("tweet_content", "")

    # 获取确认信息
    confirmed = state.get("poster_info_confirmed", "{}")
    try:
        info = json.loads(confirmed)
    except (json.JSONDecodeError, TypeError):
        info = {}

    title = info.get("title", "校园活动")
    subtitle = info.get("subtitle", "")
    organizer = info.get("organizer", "")
    date_str = info.get("date", "")
    time_str = info.get("time", "")
    venue = info.get("venue", "")
    audience = info.get("target_audience", "")

    # 从策划案提取概述段落
    plan_lines = [l.strip("- ").strip() for l in plan.split("\n") if l.strip() and not l.startswith("#")]
    summary = ""
    for line in plan_lines:
        if len(line) > 10 and not line.startswith("##"):
            summary = line
            break

    # 解析日程为时间线
    import re
    timeline_items = []
    for line in schedule.split("\n"):
        line = line.strip("- ").strip()
        if not line:
            continue
        m = re.match(r"^[-\d:：\s]*(\d{1,2}[:：]\d{2})[-~至到]?\s*(\d{1,2}[:：]\d{2})?", line)
        if m:
            t = m.group(0).strip("- ").strip()[:10]
            rest = line[m.end():].strip("- ").strip()
            timeline_items.append((t, rest))

    # 推文内容作为正文
    body_paragraphs = []
    if tweet:
        for line in tweet.split("\n"):
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("```"):
                body_paragraphs.append(line)

    # 提取通知关键信息
    notice_lines = [l for l in notice.split("\n") if l.strip() and "注意" not in l[:6]][:3]

    # 海报图片（相对路径转可显示路径）
    poster_img_tag = ""
    if poster_path:
        # 尝试找 SVG 文件
        poster_img_tag = f'<div class="poster-box"><img src="../{poster_path}" alt="活动海报" loading="lazy"><p class="caption">📌 活动海报</p></div>'

    # ── 组装 HTML ──
    meta_parts = []
    if date_str:
        meta_parts.append(date_str)
    if organizer:
        meta_parts.append(organizer)
    meta_str = " ｜ ".join(meta_parts)

    # 时间线 HTML
    timeline_html = ""
    if timeline_items:
        timeline_html = '<div class="section"><h2>📋 活动流程</h2><div class="timeline">'
        for t, desc in timeline_items:
            timeline_html += f"""
        <div class="timeline-item">
            <div class="timeline-time">{t}</div>
            <div class="timeline-dot"></div>
            <div class="timeline-content">{desc}</div>
        </div>"""
        timeline_html += "</div></div>"

    # 正文段落
    body_html = ""
    if body_paragraphs:
        body_html = '<div class="section"><h2>📝 活动回顾</h2>'
        for p in body_paragraphs[:8]:
            body_html += f"<p>{p}</p>"
        body_html += "</div>"

    # 活动信息高亮
    info_lines = []
    if date_str and time_str:
        info_lines.append(f"📅 时间：{date_str} {time_str}")
    if venue:
        info_lines.append(f"📍 地点：{venue}")
    if audience:
        info_lines.append(f"👥 对象：{audience}")
    if organizer:
        info_lines.append(f"🏢 主办：{organizer}")

    info_html = ""
    if info_lines:
        info_html = '<div class="section"><div class="highlight">'
        for line in info_lines:
            info_html += f"<p>{line}</p>"
        info_html += "</div></div>"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>{title} - 活动回顾</title>
<style>{_css()}</style>
</head>
<body>
<div class="article">
    <div class="header">
        <h1>{title}</h1>
        {f'<p style="font-size:15px;color:#666;margin-bottom:10px">{subtitle}</p>' if subtitle else ''}
        <div class="meta">{meta_str}</div>
    </div>

    {info_html}

    {f'<div class="section"><h2>📖 活动简介</h2><p>{summary}</p></div>' if summary else ''}

    {body_html}

    {timeline_html}

    {poster_img_tag}

    <div class="divider"></div>

    <div class="footer">
        <p class="org">{organizer or '校园活动组委会'}</p>
        <p>感谢所有参与者的支持与付出</p>
        <p style="margin-top:6px;font-size:12px;color:#bbb">本文由校园活动策划助手自动生成 · {datetime.now().strftime('%Y-%m-%d')}</p>
    </div>
</div>
</body>
</html>"""

    return html


def html_agent(state: ActivityState) -> ActivityState:
    """生成微信公众号风格的 HTML 活动总结推文。"""
    HTML_DIR.mkdir(exist_ok=True)
    print(f"[HTML] 正在生成公众号推文...", flush=True)

    html = _build_html(state)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"活动回顾_{ts}.html"
    path = HTML_DIR / filename
    path.write_text(html, encoding="utf-8")

    state["html_path"] = str(path)
    state["log"].append(f"【HTML】公众号推文已生成：{path}")
    print(f"[HTML] 公众号推文已生成：{path}", flush=True)

    return state