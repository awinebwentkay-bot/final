"""宣传节点：生成公众号推文 + 抽卡式海报生成（SVG）"""

import json
import random

from models import ActivityState
from config import llm
from tools import save_poster_svg, _clean_svg
from prompts import (
    PROMOTE_POSTER,
    PROMOTE_TWEET,
    REGULATION_APPROVAL,
    POSTER_TEMPLATES,
    POSTER_EXTRACT_INFO,
    POSTER_RECOMMEND_TEMPLATE,
    POSTER_GENERATE_SVG,
)


def _extract_poster_info(plan: str) -> dict:
    """LLM 从策划案提取海报关键信息。"""
    prompt = POSTER_EXTRACT_INFO.format(plan=plan)
    resp = llm.invoke(prompt).content.strip()
    # 去掉可能的外包装
    if resp.startswith("```"):
        resp = resp.strip("`").strip()
        if resp.startswith("json"):
            resp = resp[4:].strip()
    try:
        return json.loads(resp)
    except json.JSONDecodeError:
        # 兜底返回基本信息
        return {
            "title": "校园活动",
            "subtitle": "",
            "date": "待定",
            "time": "待定",
            "venue": "待定",
            "organizer": "主办方",
            "description": "",
            "target_audience": "全校师生",
        }


def _generate_svg_poster(info: dict, template_name: str, template_desc: str,
                          modification_hint: str = "") -> str:
    """LLM 生成 SVG 海报代码，可选修改建议。"""
    hint_section = ""
    if modification_hint:
        hint_section = (
            f"## 修改建议\n"
            f"用户要求修改：{modification_hint}\n"
            f"请根据以上建议调整海报设计，其他内容保持不变。\n"
        )
    prompt = POSTER_GENERATE_SVG.format(
        template_name=template_name,
        template_desc=template_desc,
        title=info.get("title", "校园活动"),
        subtitle=info.get("subtitle", ""),
        date=info.get("date", "待定"),
        time=info.get("time", "待定"),
        venue=info.get("venue", "待定"),
        organizer=info.get("organizer", "主办方"),
        description=info.get("description", ""),
        target_audience=info.get("target_audience", "全校师生"),
        modification_hint=hint_section,
    )
    resp = llm.invoke(prompt).content
    return _clean_svg(resp)


def promote_agent(state: ActivityState) -> ActivityState:
    plan = state["activity_plan"]
    regulations = REGULATION_APPROVAL

    # ── 推文（保持原有逻辑） ────────────────────────────────
    print(f"[宣传] 正在生成推文...", flush=True)
    tweet = llm.invoke(PROMOTE_TWEET.format(plan=plan, regulations=regulations)).content
    state["tweet_content"] = tweet
    state["poster_copy"] = ""
    state["poster_image"] = ""
    state["log"].append("【宣传】推文生成完成")

    # ── 抽卡式海报生成 ──────────────────────────────────────
    poster_info = _extract_poster_info(plan)

    # LLM 推荐最匹配的模板作为首抽
    print(f"  [宣传] AI 正在分析活动类型，推荐最匹配的模板...", flush=True)
    rec_prompt = POSTER_RECOMMEND_TEMPLATE.format(plan=plan)
    recommended = llm.invoke(rec_prompt).content.strip()

    # 从模板列表中找出推荐模板，置顶；其余随机排序
    template_names = list(POSTER_TEMPLATES.keys())
    if recommended in template_names:
        template_names.remove(recommended)
        random.shuffle(template_names)
        template_names.insert(0, recommended)
        print(f"  🎯 AI 推荐：{recommended}")
    else:
        random.shuffle(template_names)
        print(f"  (AI 推荐未能识别，随机抽取)")

    print(f"\n{'=' * 50}")
    print(f"  🎴 抽卡式海报生成")
    print(f"  首张为 AI 推荐模板，不满意可修改或重抽")
    print(f"{'=' * 50}")

    for i, tpl_name in enumerate(template_names):
        tpl = POSTER_TEMPLATES[tpl_name]

        modification_hint = ""
        choice = ""

        for attempt in range(5):  # 无硬限制，用户可反复修改
            print(f"\n  ── {tpl_name}（第 {attempt+1} 版）──")
            if modification_hint:
                print(f"  📝 修改建议：{modification_hint}")
            print(f"  {tpl['desc']}")
            print(f"  [生成中...]", flush=True)

            svg_code = _generate_svg_poster(
                poster_info, tpl_name, tpl["desc"], modification_hint
            )
            filepath = save_poster_svg(svg_code, tpl_name)
            state["poster_image"] = filepath
            state["poster_copy"] = (
                f"海报模板：{tpl_name}\n"
                f"文件路径：{filepath}\n"
                f"修改建议：{modification_hint or '无'}\n"
                f"活动标题：{poster_info.get('title', '')}\n"
                f"时间：{poster_info.get('date', '')} {poster_info.get('time', '')}\n"
                f"地点：{poster_info.get('venue', '')}\n"
                f"主办方：{poster_info.get('organizer', '')}"
            )

            print(f"  ✅ 已保存：{filepath}")

            prompt_text = (
                f"\n  💡 操作："
                f"输入 r 换模板 / e 重新生成 / 直接写修改建议 / Enter 确认"
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
                    modification_hint = ""
                    continue
                break
            elif choice == "e":
                print(f"  [重新生成当前模板...]", flush=True)
                modification_hint = ""
                continue
            else:
                # 自由文本 → 作为修改建议
                modification_hint = raw
                print(f"  [应用修改建议...]", flush=True)
                continue

        if choice == "r":
            continue
        else:
            break

    state["log"].append(f"【宣传】海报生成完成（模板：{tpl_name}）")
    print(f"  ✅ 最终海报：{state['poster_image']}")

    return state