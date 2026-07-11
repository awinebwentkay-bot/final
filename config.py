"""全局配置：模型、数据库路径"""

from langchain_openai import ChatOpenAI

DB_PATH = "activity_memory.db"

llm = ChatOpenAI(
    api_key="sk-sp-D.LYDLY.6EOn.MEQCIHpNRoRQHs1/WP/nB55d/hoyxo18dW5WwGMxVNOkl2ZFAiA9T+mOdVbKCWWG+MR0R0nHLdfBgwIHRRcpUEK6QDbaTQ==",
    base_url="https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    model="deepseek-v4-flash",
    temperature=0.7,
    timeout=120,
)