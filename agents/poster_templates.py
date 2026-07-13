"""预置 5 套 SVG 海报模板，手写高质量设计，仅替换文字占位符"""

import random
from datetime import datetime

# ── 占位符 ────────────────────────────────────────────────────
PH = {
    "title": "{{TITLE}}",
    "subtitle": "{{SUBTITLE}}",
    "date": "{{DATE}}",
    "time": "{{TIME}}",
    "venue": "{{VENUE}}",
    "organizer": "{{ORGANIZER}}",
    "desc": "{{DESCRIPTION}}",
    "audience": "{{AUDIENCE}}",
}


def _h(html: str) -> str:
    """转义 HTML 特殊字符。"""
    return html.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ══════════════════════════════════════════════════════════════
# 模板 1：清新简洁
# ══════════════════════════════════════════════════════════════
TEMPLATE_FRESH = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1200" width="800" height="1200">
  <defs>
    <linearGradient id="f1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2563EB"/>
      <stop offset="100%" stop-color="#7C3AED"/>
    </linearGradient>
    <filter id="f_shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-opacity="0.10"/>
    </filter>
  </defs>
  <!-- 背景 -->
  <rect width="800" height="1200" fill="#F8FAFC"/>
  <!-- 顶部装饰条 -->
  <rect width="800" height="6" fill="url(#f1)"/>
  <!-- 标题区 -->
  <rect x="60" y="80" width="680" height="280" rx="16" fill="#FFFFFF" filter="url(#f_shadow)"/>
  <rect x="60" y="80" width="8" height="280" rx="4" fill="url(#f1)"/>
  <text x="400" y="160" text-anchor="middle" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="42" font-weight="bold" fill="#1E293B">{title}</text>
  <text x="400" y="210" text-anchor="middle" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="20" fill="#64748B">{subtitle}</text>
  <text x="400" y="290" text-anchor="middle" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="16" fill="#94A3B8">{desc}</text>
  <!-- 信息卡片 -->
  <rect x="60" y="400" width="320" height="110" rx="12" fill="#FFFFFF" filter="url(#f_shadow)"/>
  <circle cx="100" cy="455" r="18" fill="#EFF6FF"/>
  <text x="100" y="461" text-anchor="middle" font-size="16" fill="#2563EB">📅</text>
  <text x="130" y="445" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="14" fill="#64748B">日期</text>
  <text x="130" y="475" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="18" font-weight="bold" fill="#1E293B">{date}</text>
  <text x="130" y="495" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="14" fill="#1E293B">{time}</text>

  <rect x="420" y="400" width="320" height="110" rx="12" fill="#FFFFFF" filter="url(#f_shadow)"/>
  <circle cx="460" cy="455" r="18" fill="#F0FDF4"/>
  <text x="460" y="461" text-anchor="middle" font-size="16" fill="#16A34A">📍</text>
  <text x="490" y="445" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="14" fill="#64748B">地点</text>
  <text x="490" y="475" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="18" font-weight="bold" fill="#1E293B">{venue}</text>
  <text x="490" y="495" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="14" fill="#1E293B">{audience}</text>

  <!-- 主办方 -->
  <rect x="60" y="540" width="680" height="60" rx="12" fill="#FFFFFF" filter="url(#f_shadow)"/>
  <text x="80" y="578" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="16" fill="#64748B">主办</text>
  <text x="130" y="578" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="16" font-weight="bold" fill="#1E293B">{organizer}</text>

  <!-- 底部装饰 -->
  <rect x="0" y="1140" width="800" height="60" fill="url(#f1)"/>
  <text x="400" y="1175" text-anchor="middle" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="13" fill="#FFFFFF" opacity="0.8">期待你的参与</text>
</svg>"""


# ══════════════════════════════════════════════════════════════
# 模板 2：热血活力
# ══════════════════════════════════════════════════════════════
TEMPLATE_DYNAMIC = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1200" width="800" height="1200">
  <defs>
    <linearGradient id="d1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#EF4444"/>
      <stop offset="50%" stop-color="#F97316"/>
      <stop offset="100%" stop-color="#EAB308"/>
    </linearGradient>
    <linearGradient id="d2" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#DC2626" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#EA580C" stop-opacity="0.95"/>
    </linearGradient>
    <filter id="d_glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <!-- 背景渐变 -->
  <rect width="800" height="1200" fill="url(#d2)"/>
  <!-- 斜切装饰条 -->
  <polygon points="0,200 800,100 800,160 0,260" fill="#FFFFFF" opacity="0.06"/>
  <polygon points="0,350 800,250 800,310 0,410" fill="#FFFFFF" opacity="0.04"/>
  <polygon points="0,500 800,400 800,460 0,560" fill="#FFFFFF" opacity="0.03"/>
  <!-- 圆形装饰 -->
  <circle cx="700" cy="150" r="120" fill="#FFFFFF" opacity="0.05"/>
  <circle cx="650" cy="180" r="60" fill="#FFFFFF" opacity="0.08"/>
  <circle cx="100" cy="1000" r="80" fill="#FFFFFF" opacity="0.05"/>
  <!-- 标题 -->
  <text x="400" y="200" text-anchor="middle" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="52" font-weight="bold" fill="#FFFFFF" filter="url(#d_glow)">{title}</text>
  <text x="400" y="260" text-anchor="middle" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="24" fill="#FED7AA">{subtitle}</text>
  <!-- 分隔线 -->
  <line x1="200" y1="300" x2="600" y2="300" stroke="#FCA5A5" stroke-width="2" opacity="0.6"/>
  <!-- 信息区 -->
  <rect x="100" y="380" width="600" height="60" rx="30" fill="#FFFFFF" opacity="0.12"/>
  <text x="400" y="418" text-anchor="middle" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="18" fill="#FFFFFF">{desc}</text>
  <!-- 时间地点卡片 -->
  <rect x="80" y="500" width="640" height="300" rx="20" fill="#FFFFFF" opacity="0.10"/>
  <text x="120" y="560" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="16" fill="#FED7AA">⏰ 时间</text>
  <text x="120" y="595" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="28" font-weight="bold" fill="#FFFFFF">{date}</text>
  <text x="120" y="630" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="20" fill="#FED7AA">{time}</text>
  <line x1="120" y1="660" x2="680" y2="660" stroke="#FFFFFF" stroke-width="1" opacity="0.15"/>
  <text x="120" y="700" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="16" fill="#FED7AA">📍 地点</text>
  <text x="120" y="735" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="26" font-weight="bold" fill="#FFFFFF">{venue}</text>
  <text x="120" y="770" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="16" fill="#FED7AA">{audience}</text>
  <!-- 底部 -->
  <rect x="0" y="1100" width="800" height="100" fill="#FFFFFF" opacity="0.06"/>
  <text x="400" y="1155" text-anchor="middle" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="15" fill="#FED7AA">主办：{organizer}</text>
</svg>"""


# ══════════════════════════════════════════════════════════════
# 模板 3：典雅文艺
# ══════════════════════════════════════════════════════════════
TEMPLATE_ELEGANT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1200" width="800" height="1200">
  <defs>
    <linearGradient id="e1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FEF3C7"/>
      <stop offset="100%" stop-color="#FDE68A"/>
    </linearGradient>
    <filter id="e_shadow">
      <feDropShadow dx="0" dy="3" stdDeviation="6" flood-opacity="0.08"/>
    </filter>
  </defs>
  <!-- 背景 -->
  <rect width="800" height="1200" fill="#FFFBEB"/>
  <rect width="800" height="1200" fill="url(#e1)" opacity="0.3"/>
  <!-- 装饰边框 -->
  <rect x="20" y="20" width="760" height="1160" rx="8" fill="none" stroke="#D4A574" stroke-width="1.5" opacity="0.5"/>
  <rect x="30" y="30" width="740" height="1140" rx="6" fill="none" stroke="#D4A574" stroke-width="0.5" opacity="0.3"/>
  <!-- 角落花纹 -->
  <path d="M50,50 Q200,50 200,200" fill="none" stroke="#D4A574" stroke-width="1.5" opacity="0.4"/>
  <path d="M750,50 Q600,50 600,200" fill="none" stroke="#D4A574" stroke-width="1.5" opacity="0.4"/>
  <path d="M50,1150 Q200,1150 200,1000" fill="none" stroke="#D4A574" stroke-width="1.5" opacity="0.4"/>
  <path d="M750,1150 Q600,1150 600,1000" fill="none" stroke="#D4A574" stroke-width="1.5" opacity="0.4"/>
  <!-- 标题区 -->
  <rect x="100" y="120" width="600" height="200" rx="16" fill="#FFFFFF" opacity="0.85" filter="url(#e_shadow)"/>
  <text x="400" y="200" text-anchor="middle" font-family="'STSong','SimSun','Noto Serif CJK SC',serif" font-size="44" font-weight="bold" fill="#78350F">{title}</text>
  <text x="400" y="250" text-anchor="middle" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="18" fill="#92400E">{subtitle}</text>
  <text x="400" y="295" text-anchor="middle" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="14" fill="#A16207">{desc}</text>
  <!-- 装饰线 -->
  <line x1="200" y1="350" x2="600" y2="350" stroke="#D4A574" stroke-width="1" opacity="0.5"/>
  <circle cx="400" cy="350" r="4" fill="#D4A574" opacity="0.6"/>
  <!-- 信息区 -->
  <rect x="120" y="400" width="560" height="280" rx="12" fill="#FFFFFF" opacity="0.7" filter="url(#e_shadow)"/>
  <text x="160" y="460" font-family="'STSong','SimSun',serif" font-size="18" fill="#78350F">时　间</text>
  <text x="260" y="460" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="22" font-weight="bold" fill="#1C1917">{date}  {time}</text>
  <line x1="160" y1="490" x2="640" y2="490" stroke="#D4A574" stroke-width="0.5" opacity="0.3"/>
  <text x="160" y="530" font-family="'STSong','SimSun',serif" font-size="18" fill="#78350F">地　点</text>
  <text x="260" y="530" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="22" font-weight="bold" fill="#1C1917">{venue}</text>
  <line x1="160" y1="560" x2="640" y2="560" stroke="#D4A574" stroke-width="0.5" opacity="0.3"/>
  <text x="160" y="600" font-family="'STSong','SimSun',serif" font-size="18" fill="#78350F">对　象</text>
  <text x="260" y="600" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="20" fill="#1C1917">{audience}</text>
  <!-- 底部 -->
  <text x="400" y="1100" text-anchor="middle" font-family="'STSong','SimSun',serif" font-size="16" fill="#92400E">主办：{organizer}</text>
  <!-- 印章 -->
  <circle cx="680" cy="1060" r="35" fill="none" stroke="#DC2626" stroke-width="2" opacity="0.7"/>
  <text x="680" y="1068" text-anchor="middle" font-family="'STSong','SimSun',serif" font-size="14" fill="#DC2626" opacity="0.7">邀 请</text>
</svg>"""


# ══════════════════════════════════════════════════════════════
# 模板 4：科技未来
# ══════════════════════════════════════════════════════════════
TEMPLATE_TECH = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1200" width="800" height="1200">
  <defs>
    <linearGradient id="t1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="50%" stop-color="#1E1B4B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <linearGradient id="t2" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#06B6D4"/>
      <stop offset="50%" stop-color="#8B5CF6"/>
      <stop offset="100%" stop-color="#EC4899"/>
    </linearGradient>
    <linearGradient id="t3" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#22D3EE"/>
      <stop offset="100%" stop-color="#A78BFA"/>
    </linearGradient>
    <filter id="t_glow">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1E293B" stroke-width="0.5" opacity="0.5"/>
    </pattern>
  </defs>
  <!-- 背景 -->
  <rect width="800" height="1200" fill="url(#t1)"/>
  <rect width="800" height="1200" fill="url(#grid)"/>
  <!-- 发光圆 -->
  <circle cx="400" cy="300" r="200" fill="#8B5CF6" opacity="0.06"/>
  <circle cx="600" cy="800" r="150" fill="#06B6D4" opacity="0.04"/>
  <!-- 装饰线条 -->
  <polyline points="0,100 200,100 250,50 400,50" fill="none" stroke="#06B6D4" stroke-width="1.5" opacity="0.3"/>
  <polyline points="800,200 600,200 550,250 450,250" fill="none" stroke="#8B5CF6" stroke-width="1.5" opacity="0.3"/>
  <polyline points="0,1000 300,1000 350,1050 500,1050" fill="none" stroke="#EC4899" stroke-width="1.5" opacity="0.3"/>
  <!-- 标题 -->
  <text x="400" y="180" text-anchor="middle" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="48" font-weight="bold" fill="url(#t3)" filter="url(#t_glow)">{title}</text>
  <text x="400" y="230" text-anchor="middle" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="20" fill="#94A3B8">{subtitle}</text>
  <!-- 中央信息框 -->
  <rect x="100" y="320" width="600" height="420" rx="16" fill="#1E293B" opacity="0.6"/>
  <rect x="100" y="320" width="600" height="420" rx="16" fill="none" stroke="#8B5CF6" stroke-width="1" opacity="0.4"/>
  <rect x="100" y="320" width="600" height="4" rx="2" fill="url(#t2)"/>
  <!-- 信息行 -->
  <text x="140" y="390" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="15" fill="#64748B">DATE</text>
  <text x="140" y="425" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="24" font-weight="bold" fill="#E2E8F0">{date}</text>
  <text x="420" y="425" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="20" fill="#94A3B8">{time}</text>
  <line x1="140" y1="450" x2="660" y2="450" stroke="#334155" stroke-width="1"/>
  <text x="140" y="500" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="15" fill="#64748B">VENUE</text>
  <text x="140" y="535" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="24" font-weight="bold" fill="#E2E8F0">{venue}</text>
  <line x1="140" y1="560" x2="660" y2="560" stroke="#334155" stroke-width="1"/>
  <text x="140" y="610" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="15" fill="#64748B">AUDIENCE</text>
  <text x="140" y="645" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="20" fill="#E2E8F0">{audience}</text>
  <line x1="140" y1="670" x2="660" y2="670" stroke="#334155" stroke-width="1"/>
  <text x="140" y="705" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="15" fill="#64748B">{desc}</text>
  <!-- 底部 -->
  <rect x="0" y="1100" width="800" height="100" fill="#1E293B" opacity="0.5"/>
  <text x="400" y="1155" text-anchor="middle" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="14" fill="#64748B">ORGANIZED BY {organizer}</text>
</svg>"""


# ══════════════════════════════════════════════════════════════
# 模板 5：国风古典
# ══════════════════════════════════════════════════════════════
TEMPLATE_CHINESE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1200" width="800" height="1200">
  <defs>
    <radialGradient id="c1" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#FFF8E7"/>
      <stop offset="100%" stop-color="#F5E6CC"/>
    </radialGradient>
    <filter id="c_ink">
      <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="4" result="noise"/>
      <feColorMatrix type="saturate" values="0" in="noise" result="gray"/>
      <feBlend in="SourceGraphic" in2="gray" mode="multiply" result="ink"/>
    </filter>
  </defs>
  <!-- 宣纸背景 -->
  <rect width="800" height="1200" fill="url(#c1)"/>
  <!-- 水墨山峦 -->
  <path d="M0,350 Q100,280 180,320 Q250,280 320,300 Q380,260 450,290 Q520,250 600,280 Q680,260 800,300 L800,500 L0,500 Z" fill="#D4C5A9" opacity="0.3"/>
  <path d="M0,400 Q150,340 250,380 Q350,340 450,370 Q550,330 650,360 Q750,340 800,370 L800,550 L0,550 Z" fill="#C4B49A" opacity="0.2"/>
  <!-- 梅花枝 -->
  <path d="M120,900 Q200,750 300,680 Q350,640 380,600" fill="none" stroke="#8B7355" stroke-width="2.5" opacity="0.5"/>
  <circle cx="210" cy="730" r="5" fill="#DC2626" opacity="0.6"/>
  <circle cx="240" cy="700" r="4" fill="#DC2626" opacity="0.5"/>
  <circle cx="310" cy="660" r="5" fill="#DC2626" opacity="0.6"/>
  <circle cx="340" cy="630" r="3" fill="#DC2626" opacity="0.5"/>
  <!-- 右侧竖排标题 -->
  <text x="640" y="200" font-family="'STSong','SimSun','Noto Serif CJK SC',serif" font-size="52" font-weight="bold" fill="#3E2723" writing-mode="vertical-rl">{title}</text>
  <text x="580" y="200" font-family="'STSong','SimSun',serif" font-size="22" fill="#6D4C41" writing-mode="vertical-rl">{subtitle}</text>
  <!-- 印章 -->
  <rect x="660" y="380" width="70" height="70" rx="4" fill="none" stroke="#DC2626" stroke-width="2" opacity="0.7"/>
  <text x="695" y="415" text-anchor="middle" font-family="'STSong','SimSun',serif" font-size="18" fill="#DC2626" opacity="0.7">雅</text>
  <text x="695" y="435" text-anchor="middle" font-family="'STSong','SimSun',serif" font-size="18" fill="#DC2626" opacity="0.7">集</text>
  <!-- 左侧信息区 -->
  <text x="120" y="480" font-family="'STSong','SimSun',serif" font-size="18" fill="#6D4C41">时　间</text>
  <text x="210" y="480" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="24" font-weight="bold" fill="#3E2723">{date}</text>
  <text x="210" y="515" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="18" fill="#6D4C41">{time}</text>
  <line x1="120" y1="540" x2="450" y2="540" stroke="#C4B49A" stroke-width="0.5"/>
  <text x="120" y="580" font-family="'STSong','SimSun',serif" font-size="18" fill="#6D4C41">地　点</text>
  <text x="210" y="580" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="24" font-weight="bold" fill="#3E2723">{venue}</text>
  <line x1="120" y1="610" x2="450" y2="610" stroke="#C4B49A" stroke-width="0.5"/>
  <text x="120" y="650" font-family="'STSong','SimSun',serif" font-size="18" fill="#6D4C41">对　象</text>
  <text x="210" y="650" font-family="'Microsoft YaHei','PingFang SC',sans-serif" font-size="20" fill="#3E2723">{audience}</text>
  <line x1="120" y1="680" x2="450" y2="680" stroke="#C4B49A" stroke-width="0.5"/>
  <text x="120" y="720" font-family="'STSong','SimSun',serif" font-size="16" fill="#6D4C41">{desc}</text>
  <!-- 底部 -->
  <text x="400" y="1100" text-anchor="middle" font-family="'STSong','SimSun',serif" font-size="16" fill="#6D4C41">主办：{organizer}</text>
  <!-- 底部装饰线 -->
  <rect x="200" y="1120" width="400" height="1" fill="#C4B49A" opacity="0.5"/>
</svg>"""


# ══════════════════════════════════════════════════════════════
# 模板注册表
# ══════════════════════════════════════════════════════════════

TEMPLATES = [
    {
        "name": "清新简洁",
        "id": "fresh",
        "desc": "白底蓝紫渐变标题，卡片式信息布局，干净清晰。适合读书会、班会等安静活动。",
        "svg": TEMPLATE_FRESH,
    },
    {
        "name": "热血活力",
        "id": "dynamic",
        "desc": "橙红渐变背景，大字标题发光效果，斜切装饰动感十足。适合晚会、比赛等热闹活动。",
        "svg": TEMPLATE_DYNAMIC,
    },
    {
        "name": "典雅文艺",
        "id": "elegant",
        "desc": "暖黄底色，宋体书法标题，藤蔓花纹边框，印章点缀。适合讲座、艺术类活动。",
        "svg": TEMPLATE_ELEGANT,
    },
    {
        "name": "科技未来",
        "id": "tech",
        "desc": "深色背景，霓虹渐变文字，网格线、发光效果。适合技术讲座、创新比赛。",
        "svg": TEMPLATE_TECH,
    },
    {
        "name": "国风古典",
        "id": "chinese",
        "desc": "宣纸底色，水墨山峦，梅花枝，竖排文字，红色印章。适合传统文化活动。",
        "svg": TEMPLATE_CHINESE,
    },
]


def render_poster(info: dict, template_name: str) -> str:
    """用预置 SVG 模板 + 信息字典渲染海报，返回 SVG 代码。"""
    tpl = None
    for t in TEMPLATES:
        if t["name"] == template_name:
            tpl = t
            break
    if not tpl:
        tpl = TEMPLATES[0]

    svg = tpl["svg"]
    svg = svg.replace("{{TITLE}}", _h(info.get("title", "校园活动")))
    svg = svg.replace("{{SUBTITLE}}", _h(info.get("subtitle", "")))
    svg = svg.replace("{{DATE}}", _h(info.get("date", "待定")))
    svg = svg.replace("{{TIME}}", _h(info.get("time", "待定")))
    svg = svg.replace("{{VENUE}}", _h(info.get("venue", "待定")))
    svg = svg.replace("{{ORGANIZER}}", _h(info.get("organizer", "待定")))
    svg = svg.replace("{{DESCRIPTION}}", _h(info.get("description", "")))
    svg = svg.replace("{{AUDIENCE}}", _h(info.get("target_audience", "全校师生")))
    return svg