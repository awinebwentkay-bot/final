"""宣传节点：生成公众号推文 + 抽卡式海报生成（预置 SVG 模板）"""

import json
import random

from models import ActivityState
from config import llm
from tools import save_poster_svg
from poster_templates import TEMPLATES, render_poster
from prompts import PROMOTE_TWEET, REGULATION_APPROVAL


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

    # ── 读取确认信息 ────────────────────────────────────────
    confirmed = state.get("poster_info_confirmed", "{}")
    try:
        poster_info = json.loads(confirmed)
    except (json.JSONDecodeError, TypeError):
        poster_info = {
            "title": "校园活动",
            "subtitle": "",
            "date": "待定",
            "time": "待定",
            "venue": "待定",
            "organizer": "待定",
            "description": "",
            "target_audience": "全校师生",
        }

    # ── AI 推荐模板 ─────────────────────────────────────────
    template_names = [t["name"] for t in TEMPLATES]

    print(f"  [宣传] AI 正在分析活动类型，推荐最匹配的模板...", flush=True)
    rec_prompt = (
        "从以下模板中选出最匹配该活动的一张，只输出模板名称：\n\n"
        + "\n".join(f"{i+1}. {t['name']} — {t['desc']}" for i, t in enumerate(TEMPLATES))
        + f"\n\n活动策划案：\n{plan}\n\n最匹配的模板名称："
    )
    recommended = llm.invoke(rec_prompt).content.strip()

    if recommended in template_names:
        template_names.remove(recommended)
        random.shuffle(template_names)
        template_names.insert(0, recommended)
        print(f"  🎯 AI 推荐：{recommended}")
    else:
        random.shuffle(template_names)
        print(f"  (AI 推荐未能识别，随机抽取)")

    print(f"\n{'=' * 50}")
    print(f"  🎴 抽卡式海报生成（预置模板·即开即用）")
    print(f"  首张为 AI 推荐模板，不满意可 r 换模板或 e 重生成")
    print(f"{'=' * 50}")

    for i, tpl_name in enumerate(template_names):
        tpl = next(t for t in TEMPLATES if t["name"] == tpl_name)

        for attempt in range(5):
            print(f"\n  ── {tpl_name}（第 {attempt+1} 版）──")
            print(f"  {tpl['desc']}")
            print(f"  [生成中...]", flush=True)

            svg_code = render_poster(poster_info, tpl_name)
            filepath = save_poster_svg(svg_code, tpl_name)
            state["poster_image"] = filepath
            state["poster_copy"] = (
                f"海报模板：{tpl_name}\n"
                f"文件路径：{filepath}\n"
                f"活动标题：{poster_info.get('title', '')}\n"
                f"时间：{poster_info.get('date', '')} {poster_info.get('time', '')}\n"
                f"地点：{poster_info.get('venue', '')}\n"
                f"主办方：{poster_info.get('organizer', '')}"
            )
            print(f"  ✅ 已保存：{filepath}")

            prompt_text = (
                f"\n  💡 操作："
                f"输入 r 换模板 / e 重新生成 / Enter 确认"
            )
            if i == len(template_names) - 1:
                prompt_text = prompt_text.replace("r 换模板 / ", "")

            raw = input(prompt_text + "\n  > ").strip()
            choice = raw.lower()

            if choice == "":
                break
            elif choice == "r":
                if i == len(template_names) - 1:
                    print(f"  (已是最后一张模板，无法切换)")
                    continue
                break
            elif choice == "e":
                print(f"  [重新生成...]", flush=True)
                continue
            else:
                print(f"  (请输入 r / e / Enter)")
                continue

        if choice == "r":
            continue
        else:
            break

    state["log"].append(f"【宣传】海报生成完成（模板：{tpl_name}）")
    print(f"  ✅ 最终海报：{state['poster_image']}")

    return state