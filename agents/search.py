"""搜索节点：从互联网搜索优秀活动策划案例作为参考"""

import re
import urllib.parse
from models import ActivityState
from config import llm
from prompts import SEARCH_REFERENCE


def _baidu_search(query: str, max_results: int = 5) -> list[dict]:
    """使用百度 HTML 搜索获取结果（国内网络环境可用）。"""
    import requests

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    url = "https://www.baidu.com/s"
    params = {"wd": query, "ie": "utf-8"}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"  [搜索] 百度搜索失败: {e}", flush=True)
        return []

    # 从 HTML 中提取搜索结果
    results = []
    # 百度搜索结果的结构：<h3 class="t">...<a href="...">标题</a>...</h3>
    # 摘要在 <span class="content-right_8Zs40">... 或 <div class="c-abstract">...
    texts = re.findall(
        r'<h3[^>]*>.*?<a[^>]*href="(.*?)"[^>]*>(.*?)</a>.*?</h3>',
        resp.text,
        re.DOTALL,
    )
    for href, title in texts[:max_results]:
        title_clean = re.sub(r"<[^>]+>", "", title).strip()
        if not title_clean:
            continue
        results.append({
            "title": title_clean,
            "url": href if href.startswith("http") else f"https://www.baidu.com{href}",
            "snippet": "",
        })

    return results


def _search_web(query: str, max_results: int = 5) -> list[dict]:
    """依次尝试多个搜索引擎，返回第一个成功的结果。"""
    engines = [
        ("百度", _baidu_search),
    ]
    for name, func in engines:
        try:
            results = func(query, max_results)
            if results:
                print(f"  [搜索] {name} 搜索成功，找到 {len(results)} 条结果", flush=True)
                return results
        except Exception as e:
            print(f"  [搜索] {name} 搜索异常: {e}", flush=True)
    return []


def _format_search_results(results: list[dict]) -> str:
    """将搜索结果格式化为文本。"""
    if not results:
        return "（未搜索到相关结果）"
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r['title']}")
        lines.append(f"    链接：{r['url']}")
        lines.append(f"    摘要：{r['snippet']}")
        lines.append("")
    return "\n".join(lines)


def search_agent(state: ActivityState) -> ActivityState:
    """从互联网搜索优秀活动策划案例，供策划节点参考。"""
    user_intent = state["user_intent"]
    print(f"[搜索] 正在从互联网搜索优秀活动策划案例...", flush=True)

    # 构造搜索关键词：从用户需求中提取活动类型关键词
    # 先让 LLM 提取关键词，更精准
    extract_prompt = (
        f"从以下用户需求中提取搜索关键词（2-4个词，用于搜索优秀活动策划案例），"
        f"只输出关键词，不要多余文字：\n{user_intent}"
    )
    try:
        keywords = llm.invoke(extract_prompt).content.strip()
    except Exception:
        # 降级：直接截取前 30 个字作为关键词
        keywords = user_intent[:30]

    print(f"  [搜索] 关键词: {keywords}", flush=True)

    # 搜索中文校园活动案例
    all_results = []
    for query in [
        f"优秀校园活动策划案例 {keywords}",
        f"大学活动策划方案 范文 {keywords}",
    ]:
        results = _search_web(query, max_results=3)
        all_results.extend(results)

    # 去重
    seen_urls = set()
    unique_results = []
    for r in all_results:
        if r["url"] not in seen_urls:
            seen_urls.add(r["url"])
            unique_results.append(r)

    if unique_results:
        print(f"  [搜索] 找到 {len(unique_results)} 条相关结果", flush=True)
    else:
        print(f"  [搜索] 未搜索到相关结果", flush=True)

    formatted = _format_search_results(unique_results)

    # 用 LLM 提炼参考要点
    try:
        ref_prompt = SEARCH_REFERENCE.format(
            search_results=formatted, user_intent=user_intent
        )
        reference = llm.invoke(ref_prompt).content.strip()
    except Exception as e:
        print(f"  [搜索] LLM 提炼失败: {e}", flush=True)
        reference = "（搜索成功但未能提炼出参考要点）"

    state["reference_cases"] = reference
    state["log"].append(f"【搜索】从互联网搜索到 {len(unique_results)} 条策划案例参考")
    print(f"[搜索] 参考要点提炼完成", flush=True)
    return state