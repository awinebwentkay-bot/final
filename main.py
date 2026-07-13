"""程序入口：解析用户输入 → 路由到子 Agent → 执行并输出"""

from datetime import datetime
from pathlib import Path

from langgraph.graph import StateGraph, END

from models import ActivityState
from config import llm
from db import save_case
from prompts import ROUTER, AMBIGUITY_CHECK
from agents import (
    command_center,
    plan_agent,
    finance_agent,
    execute_agent,
    promote_agent,
    risk_check_agent,
    feedback_agent,
    search_agent,
)

# ── Agent 注册表 ──────────────────────────────────────────────
AGENTS = {
    "command_center": command_center,
    "plan_agent": plan_agent,
    "finance_agent": finance_agent,
    "execute_agent": execute_agent,
    "promote_agent": promote_agent,
    "risk_check_agent": risk_check_agent,
    "feedback_agent": feedback_agent,
    "search_agent": search_agent,
}

# ── 路由表：意图 → 按序执行的 Agent 列表 ─────────────────────
ROUTES = {
    "full":     ["command_center", "search_agent", "plan_agent", "finance_agent",
                 "execute_agent", "promote_agent", "risk_check_agent", "feedback_agent"],
    "plan":     ["command_center", "search_agent", "plan_agent"],
    "budget":   ["command_center", "plan_agent", "finance_agent"],
    "execute":  ["command_center", "plan_agent", "finance_agent", "execute_agent"],
    "promote":  ["command_center", "plan_agent", "promote_agent"],
    "risk":     ["command_center", "plan_agent", "risk_check_agent"],
    "feedback": ["command_center", "plan_agent", "feedback_agent"],
}

# ── 输出字段配置 ──────────────────────────────────────────────
FIELD_LABELS = {
    "activity_plan":  "活动策划案",
    "total_budget":   "总预算",
    "schedule":       "活动日程",
    "host_script":    "主持稿",
    "notice_text":    "通知文案",
    "poster_copy":    "海报文案",
    "tweet_content":  "推文内容",
    "risk_report":    "风险评估报告",
    "eval_comment":   "师生评价反馈",
    "survey_template": "满意度问卷",
}

OUTPUT_FIELDS = {
    "full":     ["activity_plan", "total_budget", "schedule", "poster_copy",
                 "risk_report", "survey_template"],
    "plan":     ["activity_plan"],
    "budget":   ["activity_plan", "total_budget"],
    "execute":  ["activity_plan", "total_budget", "schedule", "host_script", "notice_text"],
    "promote":  ["activity_plan", "poster_copy", "tweet_content"],
    "risk":     ["activity_plan", "risk_report"],
    "feedback": ["activity_plan", "eval_comment", "survey_template"],
}


# ── 动态构建子图 ──────────────────────────────────────────────
def build_sub_graph(agent_names):
    """根据 Agent 名称列表动态构建 LangGraph 子图。"""
    builder = StateGraph(ActivityState)
    for name in agent_names:
        builder.add_node(name, AGENTS[name])

    builder.set_entry_point(agent_names[0])

    for i in range(len(agent_names) - 1):
        src, dst = agent_names[i], agent_names[i + 1]

        if src == "finance_agent":
            # 预算条件边：lack（超预算）或 surplus（有盈余）都退回 plan_agent
            def _budget_route(state, _dst=dst):
                if state["budget_feedback"] in ("lack", "surplus"):
                    return "plan_agent"
                return _dst

            builder.add_conditional_edges("finance_agent", _budget_route, {
                "plan_agent": "plan_agent",
                dst: dst,
            })
        else:
            builder.add_edge(src, dst)

    builder.add_edge(agent_names[-1], END)
    return builder.compile()


# ── 意图解析 ──────────────────────────────────────────────────
def parse_intent(user_input: str) -> str:
    """用 LLM 判断用户意图，返回 ROUTES 的 key。"""
    prompt = ROUTER.format(user_input=user_input)
    resp = llm.invoke(prompt)
    intent = resp.content.strip().lower()
    if intent not in ROUTES:
        print(f"[路由] 无法识别意图（{intent}），默认执行完整流程", flush=True)
        return "full"
    return intent


# ── 运行入口 ──────────────────────────────────────────────────
def run_graph(user_input: str, input_budget: int = 0, input_participants: int = 0, intent: str = None):
    if intent is None:
        print("[路由] 正在解析用户意图...", flush=True)
        intent = parse_intent(user_input)
    print(f"[路由] 意图={intent}，执行 Agent: {ROUTES[intent]}", flush=True)

    init_state = ActivityState(
        user_intent=user_input,
        input_budget=input_budget,
        input_participants=input_participants,
        short_memory={},
        history_cases=[],
        activity_plan=None,
        total_budget=None,
        budget_feedback=None,
        budget_retry=0,
        schedule=None,
        host_script=None,
        notice_text=None,
        poster_copy=None,
        tweet_content=None,
        risk_report=None,
        reference_cases=None,
        eval_comment=None,
        survey_template=None,
        task_execution_plan=None,
        log=[],
    )

    graph = build_sub_graph(ROUTES[intent])
    print("[进度] 开始执行 LangGraph 流程...", flush=True)
    final_state = graph.invoke(init_state)
    print("[进度] 流程执行完毕", flush=True)

    if intent == "full":
        save_case(final_state)

    return final_state, intent


# ── 输出结果 ──────────────────────────────────────────────────
def print_result(state: dict, intent: str):
    fields = OUTPUT_FIELDS.get(intent, ["activity_plan"])
    for key in fields:
        label = FIELD_LABELS.get(key, key)
        value = state.get(key)
        if value is None:
            continue

        if key == "activity_plan":
            # 策划案自动导出为文档，不在终端输出
            filepath = export_to_file(state, intent)
            print(f"✅ 策划案已生成：{filepath}")
        elif key == "total_budget":
            print(f"\n===== {label} ===== {value}")
        else:
            print(f"\n===== {label} =====")
            print(value)

    # 师生评价单独输出到终端（不写入文档）
    eval_val = state.get("eval_comment")
    if eval_val:
        print(f"\n===== 师生评价反馈（仅供终端查看）=====")
        print(eval_val)

    print("\n===== 运行日志 =====")
    for log in state.get("log", []):
        print(log)


# ── 交互入口 ──────────────────────────────────────────────────
def validate_activity_type(activity_type: str) -> str:
    """检查活动类型是否模糊，模糊则要求用户具体化。"""
    prompt = AMBIGUITY_CHECK.format(activity_type=activity_type)
    resp = llm.invoke(prompt)
    result = resp.content.strip()

    if result.startswith("模糊"):
        print(f"  ⚠️ 不太明确：{result}")
        return validate_activity_type(input("  请重新输入：").strip())

    # 明确则给出细化建议（不强制）
    hint = _refine_hint(activity_type)
    if hint:
        print(f"  💡 提示：{hint}")
    return activity_type


def _refine_hint(activity_type: str) -> str:
    """根据活动类型给出可选的细化建议。"""
    hints = {
        "班会": "可补充具体主题，如：防诈骗主题班会 / 心理健康班会 / 学风建设班会",
        "团建": "可补充具体形式，如：户外拓展团建 / 室内桌游团建 / 聚餐团建",
        "晚会": "可补充主题，如：中秋晚会 / 元旦晚会 / 毕业晚会",
        "比赛": "可补充比赛具体内容，如：朗诵比赛 / 歌唱比赛 / 知识竞赛",
        "分享会": "可补充分享主题，如：考研经验分享会 / 读书分享会 / 实习分享会",
        "讲座": "可补充讲座主题，如：职业规划讲座 / 心理健康讲座 / 学术讲座",
    }
    for key, msg in hints.items():
        if key in activity_type:
            return msg
    return ""


def collect_input() -> tuple:
    """分步收集用户输入，返回 (需求描述, 预算金额, 参与人数)。"""
    while True:
        print("=" * 50)
        print("  校园活动策划助手")
        print("  支持：策划 / 预算 / 执行 / 宣传 / 风险 / 反馈")
        print("=" * 50)

        print("\n请依次填写以下信息：")

        activity_type = input("  活动类型（如：读书分享会 / 迎新晚会 / 辩论赛）：").strip()
        while not activity_type:
            activity_type = input("  活动类型不能为空，请重新输入：").strip()
        activity_type = validate_activity_type(activity_type)

        participants = input("  预计参与人数：").strip()
        while not participants.isdigit() or int(participants) <= 0:
            participants = input("  请输入有效的正整数人数：").strip()

        # ── 活动规模判断 ──
        participants_int = int(participants)
        if participants_int > 50:
            print(f"\n  ⚠️ 参与人数 {participants_int} 人超过 50 人，属于中大型活动。")
            print("  📌 本助手仅适用于小型活动（50人以下）的策划。")
            print("  " + "=" * 46)
            print("  请选择：")
            print("  1. 重新开始（从活动类型重新填写）")
            print("  2. 退出程序")
            choice = input("  请输入选项（1 或 2）：").strip()
            while choice not in ("1", "2"):
                choice = input("  请输入有效选项（1 或 2）：").strip()
            if choice == "2":
                print("  已退出程序。")
                exit(0)
            # choice == "1": 重新开始
            print()
            continue

        budget = input("  预算金额（元，没有可填 0）：").strip()
        while not budget.isdigit() or int(budget) < 0:
            budget = input("  请输入有效的预算金额（非负整数）：").strip()

        user_intent = (
            f"举办一场{activity_type}，参与人数{participants}人，"
            f"预算{budget}元，需要完整活动方案及相关物料"
        )
        return user_intent, int(budget), int(participants)


# ── 导出文档 ──────────────────────────────────────────────────
EXPORT_DIR = Path("策划案输出")


def ensure_export_dir():
    EXPORT_DIR.mkdir(exist_ok=True)


def export_to_file(state: dict, intent: str) -> str:
    """将输出结果导出为 Markdown 文档。"""
    ensure_export_dir()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = EXPORT_DIR / f"活动策划案_{now}.md"

    lines = [f"# 校园活动策划方案", f"**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]
    fields = OUTPUT_FIELDS.get(intent, ["activity_plan"])

    for key in fields:
        label = FIELD_LABELS.get(key, key)
        value = state.get(key)
        if value is None:
            continue
        if key == "total_budget":
            lines.append(f"## {label}\n\n{value}\n")
            break  # 输出到总预算即止，后续内容不导出
        else:
            lines.append(f"## {label}\n\n{value}\n")

    lines.append("---\n*由校园活动策划助手自动生成*")
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)


if __name__ == "__main__":
    user_input, input_budget, input_participants = collect_input()

    print()
    result, intent = run_graph(user_input, input_budget=input_budget, input_participants=input_participants)
    print()
    print_result(result, intent)