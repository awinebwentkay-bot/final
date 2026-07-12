"""搜索节点：从互联网搜索优秀活动策划案例作为参考"""

import re
from models import ActivityState
from config import llm
from prompts import SEARCH_REFERENCE


def _so_search(query: str, max_results: int = 5) -> list[dict]:
    """使用 360 搜索获取结果（国内网络环境可用，拦截少）。"""
    import requests

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    }
    url = "https://www.so.com/s"
    params = {"q": query}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"  [搜索] 360搜索失败: {e}", flush=True)
        return []

    html = resp.text
    results = []

    # 360 结果结构：<h3 class="..."><a href="...">标题</a></h3>
    for m in re.finditer(r'<h3[^>]*>(.*?)</h3>', html, re.DOTALL):
        link_match = re.search(r'<a[^>]*href="(.*?)"[^>]*>(.*?)</a>', m.group(1), re.DOTALL)
        if not link_match:
            continue
        href = link_match.group(1).strip()
        title_raw = link_match.group(2)
        title = re.sub(r"<[^>]+>", "", title_raw).strip()
        if not title or href.startswith("javascript"):
            continue
        full_url = href if href.startswith("http") else f"https://www.so.com{href}"
        results.append({"title": title, "url": full_url, "snippet": ""})
        if len(results) >= max_results:
            break

    return results


def _bing_search(query: str, max_results: int = 5) -> list[dict]:
    """使用 Bing 搜索获取结果（兜底）。"""
    import requests

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    url = "https://cn.bing.com/search"
    params = {"q": query, "setlang": "zh-cn"}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"  [搜索] Bing 搜索失败: {e}", flush=True)
        return []

    html = resp.text
    results = []

    for m in re.finditer(r'<h2[^>]*><a[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a></h2>', html, re.DOTALL):
        href = m.group(1)
        title_raw = m.group(2)
        title = re.sub(r"<[^>]+>", "", title_raw).strip()
        if not title:
            continue
        results.append({"title": title, "url": href, "snippet": ""})
        if len(results) >= max_results:
            break

    return results


def _search_web(query: str, max_results: int = 5) -> list[dict]:
    """依次尝试多个搜索引擎，返回第一个成功的结果。"""
    engines = [
        ("360搜索", _so_search),
        ("Bing", _bing_search),
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


def _generate_llm_reference(user_intent: str) -> str:
    """当网络搜索不可用时，让大模型根据自身知识生成参考案例。"""
    print(f"  [搜索] 网络搜索不可用，由大模型生成参考案例...", flush=True)
    prompt = (
        f"你是一位校园活动策划专家。请根据用户的需求，从你的知识中提供2-3个"
        f"相关的优秀校园活动策划案例参考要点。\n\n"
        f"用户需求：{user_intent}\n\n"
        f"请列出2-3个参考案例，每个包含：活动名称、核心创意亮点、流程设计特色。"
        f"如果用户需求有具体活动类型，优先给出同类型的案例。"
        f"输出格式简洁，每个案例3-5行。"
    )
    try:
        resp = llm.invoke(prompt)
        return resp.content.strip()
    except Exception as e:
        print(f"  [搜索] LLM 生成参考案例失败: {e}", flush=True)
        return ""


def search_agent(state: ActivityState) -> ActivityState:
    """从互联网搜索优秀活动策划案例，供策划节点参考。
    如果网络搜索不可用，则用大模型自身知识生成参考案例。"""
    user_intent = state["user_intent"]
    print(f"[搜索] 正在搜索优秀活动策划案例参考...", flush=True)

    # 提取搜索关键词
    extract_prompt = (
        f"从以下用户需求中提取搜索关键词（2-4个词，用于搜索优秀活动策划案例），"
        f"只输出关键词，不要多余文字：\n{user_intent}"
    )
    try:
        keywords = llm.invoke(extract_prompt).content.strip()
    except Exception:
        keywords = user_intent[:30]

    print(f"  [搜索] 关键词: {keywords}", flush=True)

    # 尝试网络搜索
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
        print(f"  [搜索] 找到 {len(unique_results)} 条网络搜索结果", flush=True)
        formatted = _format_search_results(unique_results)
        try:
            ref_prompt = SEARCH_REFERENCE.format(
                search_results=formatted, user_intent=user_intent
            )
            reference = llm.invoke(ref_prompt).content.strip()
        except Exception as e:
            print(f"  [搜索] LLM 提炼失败: {e}", flush=True)
            reference = "（搜索成功但未能提炼出参考要点）"
        state["log"].append(f"【搜索】从互联网搜索到 {len(unique_results)} 条策划案例参考")
    else:
        # 网络搜索失败，用 LLM 自身知识生成参考案例
        print(f"  [搜索] 网络搜索不可用，改为由大模型生成参考案例", flush=True)
        reference = _generate_llm_reference(user_intent)
        state["log"].append("【搜索】网络搜索不可用，由大模型生成参考案例")

    if reference:
        state["reference_cases"] = reference
        print(f"[搜索] 参考案例准备完成", flush=True)
    else:
        state["reference_cases"] = None
        print(f"[搜索] 未能获取参考案例，继续执行", flush=True)

    return state