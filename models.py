"""类型定义：全局状态 State"""

from typing import TypedDict, List, Optional


class ActivityState(TypedDict):
    user_intent: str
    short_memory: dict
    history_cases: List[dict]
    activity_plan: Optional[str]
    total_budget: Optional[int]
    budget_feedback: Optional[str]
    budget_retry: int
    schedule: Optional[str]
    host_script: Optional[str]
    notice_text: Optional[str]
    poster_copy: Optional[str]
    tweet_content: Optional[str]
    risk_report: Optional[str]
    eval_comment: Optional[str]
    survey_template: Optional[str]
    log: List[str]