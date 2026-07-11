"""所有 Agent 的 prompt 模板，集中管理便于后续修改 / i18n"""


PLAN_MAIN = """
根据用户需求生成校园活动完整策划案，参考历史案例：{cases}
用户需求：{user_intent}{budget_hint}
输出完整活动主题、流程、参与人数、场地需求。
"""

FINANCE_EXTRACT = "从策划案提取预计参与人数，只输出数字：{plan}"

EXECUTE_SCHEDULE = "根据策划案生成活动日程：{plan}"
EXECUTE_SCRIPT = "生成活动主持稿：{plan}"
EXECUTE_NOTICE = "生成活动通知文案：{plan}"

PROMOTE_POSTER = "生成活动海报宣传文案：{plan}"
PROMOTE_TWEET = "生成校园公众号推文：{plan}"

RISK_CHECK = "校园活动风险评估，输出合规检查报告：{plan}"

FEEDBACK_EVAL = "模拟学生、辅导员视角评价本次活动方案：{plan}"
FEEDBACK_SURVEY = "生成活动满意度问卷模板"

ROUTER = """分析用户关于校园活动的需求，只输出一个词表示意图分类：
- full    → 需要完整活动策划（策划案+预算+执行+宣传+风险+反馈）
- plan    → 只需要策划案
- budget  → 只需要预算评估
- execute → 只需要执行物料（日程、主持稿、通知）
- promote → 只需要宣传物料（海报、推文）
- risk    → 只需要风险评估
- feedback → 只需要反馈评价和问卷

用户输入：{user_input}
分类结果："""