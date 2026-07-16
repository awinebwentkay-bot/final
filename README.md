# 🎯 校园活动策划助手

基于 LangGraph 的多 Agent 校园活动策划系统，支持活动策划、预算评估、执行方案、宣传物料、风险审查、反馈评价的全流程自动生成。

## 功能

| 模块 | 说明 |
|------|------|
| **策划案生成** | 根据活动类型、人数、预算生成完整策划方案 |
| **预算评估** | 区分可报销/不可报销经费，自动估算并迭代优化 |
| **日程安排** | 生成活动当天流程 + 前期准备时间线 |
| **主持稿** | 以主持人身份撰写正式串场词 |
| **通知文案** | 生成活动通知，时间地点与海报信息保持一致 |
| **海报生成** | 调用 `qwen-image-2.0` 生成海报图片，支持 5 种风格 |
| **公众号推文** | 生成微信公众号风格的 HTML 活动回顾 |
| **PPT 演示文稿** | 生成主持人手卡 + 现场展示两份 PPT，支持自定义模板 |
| **风险评估** | 依据学校规章进行合规审查 |
| **师生评价** | 模拟学生、辅导员视角评价方案并生成满意度问卷 |

## 快速开始

### 环境要求

- Python 3.11+
- 一个兼容 OpenAI API 的 LLM 服务（已配置 token-plan 代理）

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行

**命令行模式：**
```bash
python main.py
```

**Web 界面（推荐）：**
```bash
streamlit run app.py
```

浏览器访问 `http://localhost:8501`

或`https://thus-kinship-pelvis.ngrok-free.dev`，点击`visit site`即可进入

## 项目结构

```
├── main.py              # CLI 入口，交互输入 + LangGraph 流程
├── app.py               # Streamlit Web 界面
├── config.py            # LLM 配置（模型、API key、超时）
├── models.py            # ActivityState 类型定义
├── prompts.py           # 所有 Agent 的 prompt 模板 + 学校规章
├── tools.py             # 工具函数（场地推荐、海报生成）
├── venues.py            # 场地资源数据库（来自《场地资源.pdf》）
├── db.py                # SQLite 长期记忆
├── seed_cases.py        # 历史案例种子数据
├── agents/
│   ├── command.py       # 指挥中心
│   ├── plan.py          # 策划案生成
│   ├── finance.py       # 预算评估
│   ├── execute.py       # 日程、主持稿、通知
│   ├── promote.py       # 海报、推文
│   ├── risk.py          # 风险评估
│   ├── feedback.py      # 评价反馈
│   ├── confirm.py       # 信息确认
│   ├── search.py        # 案例搜索
│   ├── ppt.py           # PPT 生成
│   └── html.py          # 公众号推文 HTML
├── PPT模板/             # PPT 自定义模板
├── 策划案输出/          # 生成的各类文档
├── 日程输出/
├── 主持稿输出/
├── 通知输出/
├── 海报输出/
├── 公众号推文/
├── 评价输出/
├── 问卷输出/
├── 风险评估输出/
└── PPT演示文稿/
```

## 配置

编辑 `config.py` 修改 LLM 设置：

```python
llm = ChatOpenAI(
    api_key="你的 API key",
    base_url="https://your-api-endpoint/compatible-mode/v1",
    model="your-model",
    temperature=0.7,
    timeout=300,
)
```

## 输出文档

所有生成的文件按类型分别存放在对应目录中：

- `策划案输出/` — 活动策划方案 Markdown
- `日程输出/` — 活动日程 Markdown
- `主持稿输出/` — 主持串场词 Markdown
- `通知输出/` — 活动通知 Markdown
- `海报输出/` — 海报图片 PNG
- `公众号推文/` — 活动回顾 HTML
- `PPT演示文稿/` — 主持人手卡和活动现场演示PowerPoint 文件
- `评价输出/` — 师生评价反馈 Markdown
- `问卷输出/` — 满意度问卷 Markdown
- `风险评估输出/` — 风险评估报告 Markdown

## 技术栈

- **LangGraph** — 多 Agent 编排与状态管理
- **LangChain** — LLM 调用封装
- **Streamlit** — Web 交互界面
- **python-pptx** — PowerPoint 生成
- **Pillow** — 图片处理
- **SQLite** — 长期记忆存储