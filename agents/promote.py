"""宣传节点：生成海报文案、公众号推文"""

from models import ActivityState
from config import llm
from prompts import PROMOTE_POSTER, PROMOTE_TWEET, REGULATION_APPROVAL


def promote_agent(state: ActivityState) -> ActivityState:
    plan = state["activity_plan"]
    regulations = REGULATION_APPROVAL
    print(f"[宣传] 正在生成海报文案...", flush=True)
    poster = llm.invoke(PROMOTE_POSTER.format(plan=plan, regulations=regulations)).content
    print(f"[宣传] 正在生成推文...", flush=True)
    tweet = llm.invoke(PROMOTE_TWEET.format(plan=plan, regulations=regulations)).content
    state["poster_copy"] = poster
    state["tweet_content"] = tweet
    state["log"].append("【宣传】海报、推文生成完成")
    return state