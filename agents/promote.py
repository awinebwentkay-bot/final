"""宣传节点：生成公众号推文 + qwen-image-2.0 海报生成"""

import json

from models import ActivityState
from config import llm
from tools import generate_poster_image
from prompts import PROMOTE_TWEET, POSTER_IMAGE_PROMPT, REGULATION_APPROVAL


def promote_agent(state: ActivityState) -> ActivityState:
    plan = state["activity_plan"]
    regulations = REGULATION_APPROVAL

    # ── 推文 ─────────────────────────────────────────────────
    print(f"[宣传] 正在生成推文...", flush=True)
    tweet = llm.invoke(PROMOTE_TWEET.format(plan=plan, regulations=regulations)).content
    state["tweet_content"] = tweet
    state["poster_copy"] = ""
    state["poster_image"] = ""
    state["log"].append("【宣传】推文生成完成")

    # ── 是否需要海报 ────────────────────────────────────────
    if state.get("skip_interactive"):
        state["need_poster"] = True
    else:
        need_poster = input("\n  🖼️ 是否需要生成海报？（y/n，默认 y）：").strip().lower()
        if need_poster in ("n", "no", "否"):
            state["need_poster"] = False
            state["log"].append("【宣传】用户选择不生成海报，已跳过")
            print("[宣传] 跳过海报生成", flush=True)
            return state
        state["need_poster"] = True

    # ── 读取已确认信息 ──────────────────────────────────────
    confirmed = state.get("poster_info_confirmed", "{}")
    try:
        info = json.loads(confirmed)
    except (json.JSONDecodeError, TypeError):
        info = {
            "title": "校园活动",
            "subtitle": "",
            "date": "待定",
            "time": "待定",
            "venue": "待定",
            "organizer": "待定",
            "description": "",
            "target_audience": "全校师生",
        }

    # ── 征求风格意见 ────────────────────────────────────────
    if state.get("skip_interactive"):
        chosen_style = "清新简洁"
    else:
        print(f"\n  🎨 请选择海报风格：")
        print(f"     1. 清新简洁 — 白色/浅灰背景，彩色标题，卡片式排列")
        print(f"     2. 热血活力 — 渐变背景，粗体大字，动感元素")
        print(f"     3. 典雅文艺 — 暖棕底色，柔和光影，文艺元素")
        print(f"     4. 科技未来 — 深色背景，霓虹渐变，科技感")
        print(f"     5. 国风古典 — 水墨/宣纸底，书法标题，传统纹样")
        style_choice = input("  请输入编号（1-5，默认 1）：").strip()
        style_map = {"1": "清新简洁", "2": "热血活力", "3": "典雅文艺", "4": "科技未来", "5": "国风古典"}
        chosen_style = style_map.get(style_choice, "清新简洁")

    # ── 生成海报图片 ────────────────────────────────────────
    print(f"  [宣传] AI 正在生成海报描述（风格：{chosen_style}）...", flush=True)
    image_prompt = llm.invoke(POSTER_IMAGE_PROMPT.format(style=chosen_style, **info)).content.strip()

    print(f"  [宣传] 正在调用 qwen-image-2.0 生成海报图片...", flush=True)
    print(f"  prompt: {image_prompt[:80]}...", flush=True)

    try:
        filepath = generate_poster_image(image_prompt)
        state["poster_image"] = filepath
        state["poster_copy"] = (
            f"海报文件：{filepath}\n"
            f"生成模型：qwen-image-2.0\n"
        )
        state["log"].append(f"【宣传】海报图片生成完成：{filepath}")
        print(f"  ✅ 海报已生成：{filepath}")
    except Exception as e:
        error_msg = f"海报生成失败：{e}"
        state["poster_image"] = None
        state["log"].append(f"【宣传】{error_msg}")
        print(f"  ❌ {error_msg}")

    return state