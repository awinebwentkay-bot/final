"""Streamlit 图形界面 — 校园活动策划助手"""

import streamlit as st
import sys
import os
import json
from pathlib import Path
from datetime import datetime

# 将项目根目录加入路径，复用现有模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import llm
from prompts import AMBIGUITY_CHECK, ROUTER, POSTER_EXTRACT_INFO
import main
from main import (
    run_graph, print_result, export_to_file, export_schedule,
    export_eval, export_survey, export_risk, export_script, export_notice,
    OUTPUT_FIELDS, EXPORT_DIR,
)

# ── 页面配置 ──
st.set_page_config(
    page_title="校园活动策划助手",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── 自定义样式 ──
st.markdown("""
<style>
    .stApp { max-width: 800px; margin: 0 auto; }
    .main-title { text-align: center; font-size: 2rem; font-weight: 700; margin-bottom: 0.3rem; }
    .sub-title { text-align: center; color: #666; margin-bottom: 2rem; }
    .step-header { font-size: 1.1rem; font-weight: 600; margin: 1.5rem 0 0.5rem 0; }
    .output-box { background: #f0f2f6; border-radius: 8px; padding: 1rem; margin: 0.5rem 0; }
    .file-link { padding: 0.3rem 0; }
    .stProgress > div > div > div > div { background-color: #1A56DB; }
</style>
""", unsafe_allow_html=True)

# ── 初始化会话状态 ──
if "step" not in st.session_state:
    st.session_state.step = "input"
    st.session_state.activity_type = ""
    st.session_state.participants = 0
    st.session_state.venue_type = "室内"
    st.session_state.budget_reimbursable = 0
    st.session_state.budget_non_reimbursable = 0
    st.session_state.details = ""
    st.session_state.user_intent = ""
    st.session_state.result = None
    st.session_state.intent = None
    st.session_state.running = False
    st.session_state.done = False
    st.session_state.need_host = True
    st.session_state.need_ppt = True

# ── 辅助函数 ──
def _validate_activity_type(atype):
    prompt = AMBIGUITY_CHECK.format(activity_type=atype)
    resp = llm.invoke(prompt)
    result = resp.content.strip()
    if result.startswith("模糊"):
        return False, result
    return True, ""


def _hint(atype):
    hints = {
        "班会": "可补充具体主题，如：防诈骗主题班会 / 心理健康班会 / 学风建设班会",
        "团建": "可补充具体形式，如：户外拓展团建 / 室内桌游团建 / 聚餐团建",
        "晚会": "可补充主题，如：中秋晚会 / 元旦晚会 / 毕业晚会",
        "比赛": "可补充比赛具体内容，如：朗诵比赛 / 歌唱比赛 / 知识竞赛",
        "分享会": "可补充分享主题，如：考研经验分享会 / 读书分享会 / 实习分享会",
        "讲座": "可补充讲座主题，如：职业规划讲座 / 心理健康讲座 / 学术讲座",
    }
    for key, msg in hints.items():
        if key in atype:
            return msg
    return ""


# ── 标题 ──
st.markdown('<p class="main-title">🎯 校园活动策划助手</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">策划 · 预算 · 执行 · 宣传 · 风险 · 反馈</p>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 信息输入页（所有输入在同一页）
# ══════════════════════════════════════════════════════════════
if st.session_state.step in ("input", "activity_type", "participants", "venue_type", "budget", "details"):
    st.markdown('<p class="step-header">📝 填写活动信息</p>', unsafe_allow_html=True)

    with st.form("input_form"):
        atype = st.text_input("活动类型", placeholder="如：读书分享会 / 迎新晚会 / 辩论赛",
                              value=st.session_state.activity_type)

        participants = st.number_input("预计参与人数", min_value=1, step=1, value=30)

        venue_type = st.radio("活动场地类型", ["室内", "室外"], horizontal=True)

        col1, col2 = st.columns(2)
        with col1:
            budget_reimb = st.number_input("可报销经费（元）", min_value=0, step=50, value=0)
        with col2:
            budget_non = st.number_input("不可报销经费/班费（元）", min_value=0, step=50, value=0)

        hint = _hint(atype)
        if hint:
            st.info(f"💡 {hint}")

        details = st.text_area("补充说明（可选）", placeholder="活动主题、特殊要求、形式细节、目标人群等\n例如：主题是'AI赋能未来'，希望有互动环节，面向计算机系学生")

        submitted = st.form_submit_button("✅ 下一步", type="primary", use_container_width=True)

    if submitted:
        if not atype.strip():
            st.error("活动类型不能为空")
        else:
            if participants > 50:
                st.error(f"⚠️ 参与人数 {participants} 人超过 50 人，属于中大型活动。本助手仅适用于小型活动（50人以下）的策划。")
            else:
                with st.spinner("正在校验活动类型..."):
                    ok, msg = _validate_activity_type(atype.strip())
                if not ok:
                    st.warning(f"不太明确：{msg}")
                else:
                    st.session_state.activity_type = atype.strip()
                    st.session_state.participants = participants
                    st.session_state.venue_type = venue_type
                    st.session_state.budget_reimbursable = budget_reimb
                    st.session_state.budget_non_reimbursable = budget_non
                    st.session_state.details = details.strip()
                    st.session_state.step = "confirm"
                    st.rerun()

# ══════════════════════════════════════════════════════════════
# 步骤 6: 确认
# ══════════════════════════════════════════════════════════════
elif st.session_state.step == "confirm":
    st.markdown(f'<p class="step-header">📋 确认信息</p>', unsafe_allow_html=True)
    total_budget = st.session_state.budget_reimbursable + st.session_state.budget_non_reimbursable

    # 组装 user_intent
    user_intent = (
        f"举办一场{st.session_state.activity_type}，参与人数{st.session_state.participants}人，"
        f"可报销预算{st.session_state.budget_reimbursable}元，不可报销预算（班费）{st.session_state.budget_non_reimbursable}元，"
        f"场地类型：{st.session_state.venue_type}，需要完整活动方案及相关物料"
    )
    if st.session_state.details:
        user_intent += f"。\n补充说明：{st.session_state.details}"
    st.session_state.user_intent = user_intent

    info = {
        "活动类型": st.session_state.activity_type,
        "参与人数": f"{st.session_state.participants}人",
        "场地类型": st.session_state.venue_type,
        "可报销经费": f"{st.session_state.budget_reimbursable}元",
        "不可报销经费（班费）": f"{st.session_state.budget_non_reimbursable}元",
        "总预算": f"{total_budget}元",
    }
    if st.session_state.details:
        info["补充说明"] = st.session_state.details

    for k, v in info.items():
        st.markdown(f"**{k}：** {v}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 修改", use_container_width=True):
            st.session_state.step = "input"
            st.rerun()
    with col2:
        if st.button("✅ 确认并开始生成", type="primary", use_container_width=True):
            st.session_state.step = "options"
            st.rerun()

# ══════════════════════════════════════════════════════════════
# 步骤 6.5: 生成选项（主持稿 / PPT）
# ══════════════════════════════════════════════════════════════
elif st.session_state.step == "options":
    st.markdown(f'<p class="step-header">⚙️ 选择要生成的内容</p>', unsafe_allow_html=True)

    st.markdown("请选择需要自动生成的项目：")

    need_host = st.checkbox("🎤 主持稿 / 主持串场词", value=st.session_state.need_host,
                            help="勾选后将为活动生成完整的主持人手卡")
    need_ppt = st.checkbox("📊 PPT 演示文稿", value=st.session_state.need_ppt,
                           help="勾选后将生成 PPT 演示文稿（含主持人手卡和活动现场展示）")

    st.info("📌 活动策划案、预算、海报、通知、风险评估等为必选项，将自动生成。")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 返回修改", use_container_width=True):
            st.session_state.step = "confirm"
            st.rerun()
    with col2:
        if st.button("✅ 确认并继续", type="primary", use_container_width=True):
            st.session_state.need_host = need_host
            st.session_state.need_ppt = need_ppt
            st.session_state.step = "poster_confirm"
            st.rerun()

# ══════════════════════════════════════════════════════════════
# 步骤 6.6: 海报信息确认
# ══════════════════════════════════════════════════════════════
elif st.session_state.step == "poster_confirm":
    st.markdown(f'<p class="step-header">🖼️ 确认海报信息</p>', unsafe_allow_html=True)

    # 先跑一轮 LLM 提取策划案信息（只跑策划流程，不跑其他agent）
    if "poster_info" not in st.session_state:
        with st.spinner("正在从策划案中提取信息..."):
            total_budget = st.session_state.budget_reimbursable + st.session_state.budget_non_reimbursable
            result, intent = run_graph(
                st.session_state.user_intent,
                input_budget=total_budget,
                input_budget_reimbursable=st.session_state.budget_reimbursable,
                input_budget_non_reimbursable=st.session_state.budget_non_reimbursable,
                input_participants=st.session_state.participants,
                venue_type=st.session_state.venue_type,
                intent="plan",  # 只跑策划流程，不跑其他 agent
                poster_info_confirmed="__skip__",
                skip_interactive=True,
            )
            plan = result.get("activity_plan", "")
            st.session_state.plan = plan
            prompt = POSTER_EXTRACT_INFO.format(plan=plan)
            resp = llm.invoke(prompt).content.strip()
            if resp.startswith("```"):
                resp = resp.strip("`").strip()
                if resp.startswith("json"):
                    resp = resp[4:].strip()
            try:
                info = json.loads(resp)
            except Exception:
                info = {"title": "校园活动", "subtitle": "", "date": "待定", "time": "待定",
                        "venue": "待定", "organizer": "待定", "description": "", "target_audience": "全校师生"}
            st.session_state.poster_info = info

    info = st.session_state.poster_info
    st.markdown("以下信息将从策划案中提取，用于海报和PPT生成。可按需修改：")

    fields = [
        ("title", "活动标题"),
        ("subtitle", "副标题/标语"),
        ("date", "活动日期"),
        ("time", "活动时间"),
        ("venue", "活动地点"),
        ("organizer", "主办单位"),
        ("description", "一句话亮点"),
        ("target_audience", "面向人群"),
    ]

    new_info = {}
    for key, label in fields:
        val = st.text_input(label, value=info.get(key, "待定"))
        new_info[key] = val

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 跳过", use_container_width=True):
            st.session_state.poster_info_confirmed = json.dumps(info, ensure_ascii=False)
            st.session_state.step = "running"
            st.rerun()
    with col2:
        if st.button("✅ 确认并继续", type="primary", use_container_width=True):
            st.session_state.poster_info_confirmed = json.dumps(new_info, ensure_ascii=False)
            st.session_state.step = "running"
            st.rerun()

# ══════════════════════════════════════════════════════════════
# 步骤 7: 执行中
# ══════════════════════════════════════════════════════════════
elif st.session_state.step == "running":
    st.markdown(f'<p class="step-header">⏳ 正在生成...</p>', unsafe_allow_html=True)

    progress_bar = st.progress(0, text="正在解析用户意图...")
    status_text = st.empty()

    try:
        total_budget = st.session_state.budget_reimbursable + st.session_state.budget_non_reimbursable

        # 按活动主题+时间创建本次会话的输出目录
        activity_name = st.session_state.activity_type
        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = Path("output") / f"{activity_name}_{now_str}"
        session_dir.mkdir(parents=True, exist_ok=True)
        main.SESSION_DIR = session_dir

        progress_bar.progress(10, text="正在生成活动方案...")
        result, intent = run_graph(
            st.session_state.user_intent,
            input_budget=total_budget,
            input_budget_reimbursable=st.session_state.budget_reimbursable,
            input_budget_non_reimbursable=st.session_state.budget_non_reimbursable,
            input_participants=st.session_state.participants,
            venue_type=st.session_state.venue_type,
            poster_info_confirmed=st.session_state.get("poster_info_confirmed", ""),
            skip_interactive=True,
            need_host=st.session_state.need_host,
            need_ppt=st.session_state.need_ppt,
        )

        progress_bar.progress(80, text="正在导出文档...")
        st.session_state.result = result
        st.session_state.intent = intent
        st.session_state.done = True

        # 导出策划案
        plan_path = export_to_file(result, intent)
        progress_bar.progress(90, text="正在生成文件...")

        # 收集所有输出文件
        files = []
        fields = OUTPUT_FIELDS.get(intent, ["activity_plan"])
        for key in fields:
            label = {
                "activity_plan": "活动策划案", "total_budget": "总预算", "schedule": "活动日程",
                "host_script": "主持稿", "notice_text": "通知文案", "poster_copy": "海报文案",
                "poster_image": "海报图片", "risk_report": "风险评估报告",
                "survey_template": "满意度问卷", "ppt_path": "PPT演示文稿",
                "html_path": "公众号推文",
            }.get(key, key)
            value = result.get(key)
            if not value:
                continue
            if key == "activity_plan":
                files.append(("📄 活动策划案", plan_path, "markdown"))
            elif key == "schedule":
                p = export_schedule(value)
                files.append(("📋 活动日程", p, "markdown"))
            elif key == "host_script":
                p = export_script(value)
                files.append(("🎤 主持稿", p, "markdown"))
            elif key == "notice_text":
                p = export_notice(value)
                files.append(("📢 通知文案", p, "markdown"))
            elif key == "risk_report":
                p = export_risk(value)
                files.append(("⚠️ 风险评估报告", p, "markdown"))
            elif key == "survey_template":
                p = export_survey(value)
                files.append(("📝 满意度问卷", p, "markdown"))
            elif key == "poster_image":
                files.append(("🖼️ 海报图片", value, "image"))
            elif key == "ppt_path":
                lines = value.strip().split("\n")
                labels = ["📊 主持人手卡", "📊 活动现场展示"]
                for i, ppt in enumerate(lines):
                    ppt = ppt.strip()
                    if ppt:
                        label = labels[i] if i < len(labels) else "📊 PPT"
                        files.append((label, ppt, "pptx"))
            elif key == "html_path":
                files.append(("🌐 公众号推文", value, "html"))

        progress_bar.progress(100, text="✅ 完成！")
        st.session_state.generated_files = files
        st.session_state.step = "results"

    except Exception as e:
        progress_bar.empty()
        st.error(f"生成失败：{e}")
        st.session_state.step = "confirm"

    if st.session_state.step != "results":
        st.rerun()
    else:
        st.rerun()

# ══════════════════════════════════════════════════════════════
# 步骤 8: 结果展示
# ══════════════════════════════════════════════════════════════
elif st.session_state.step == "results":
    st.markdown(f'<p class="step-header">✅ 生成完成</p>', unsafe_allow_html=True)
    st.success("所有内容已生成完毕！")

    result = st.session_state.result
    intent = st.session_state.intent

    # 展示策划案
    plan_path = export_to_file(result, intent)
    try:
        plan_text = Path(plan_path).read_text(encoding="utf-8")
        with st.expander("📄 活动策划案", expanded=True):
            st.markdown(plan_text)
            with open(plan_path, "rb") as f:
                st.download_button("📥 下载策划案", f, file_name=Path(plan_path).name, use_container_width=True)
    except Exception:
        pass

    # 其他文件
    if "generated_files" in st.session_state:
        st.markdown("---")
        st.markdown("#### 📂 生成的文件")
        for label, path, ftype in st.session_state.generated_files:
            if not path or not Path(path).exists():
                continue
            if ftype == "markdown":
                with st.expander(label):
                    text = Path(path).read_text(encoding="utf-8")
                    st.markdown(text)
                    with open(path, "rb") as f:
                        st.download_button(f"📥 下载", f, file_name=Path(path).name)
            elif ftype == "image":
                st.image(path, caption=label)
            elif ftype in ("pptx", "html"):
                st.markdown(f"- {label}：[{path}]({path})")
                with open(path, "rb") as f:
                    st.download_button(f"📥 下载 {label}", f, file_name=Path(path).name)

    # 运行日志
    logs = result.get("log", [])
    if logs:
        with st.expander("📋 运行日志"):
            for log in logs:
                st.text(log)

    if st.button("🔄 重新开始", type="primary", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()