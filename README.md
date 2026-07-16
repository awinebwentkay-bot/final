# 🎯 校园活动策划助手

基于 LangGraph 的多 Agent 校园活动策划系统，支持活动策划、预算评估、执行方案、宣传物料、PPT 生成、风险审查、反馈评价的全流程自动生成。

## 功能

| 模块 | 说明 |
|------|------|
| **策划案生成** | 根据活动类型、人数、预算生成完整策划方案，引用具体场地资源 |
| **预算评估** | 区分可报销/不可报销经费，自动估算并迭代优化 |
| **日程安排** | 生成活动当天面向参与者的完整流程 |
| **主持稿** | 以主持人身份撰写正式串场词，覆盖开场到结束 |
| **通知文案** | 生成活动通知，时间地点与海报信息保持一致 |
| **海报生成** | 调用 `qwen-image-2.0` 生成海报图片，支持 5 种风格选择 |
| **公众号推文** | 生成微信公众号风格的 HTML 活动回顾（含活动流程） |
| **PPT 演示文稿** | 生成主持人手卡 + 现场展示两份 PPT，支持自定义模板 |
| **风险评估** | 依据学校规章进行合规审查，AI 生成仅供参考 |
| **师生评价** | 模拟学生、辅导员视角评价方案并生成满意度问卷 |

## 快速开始

### 环境要求

- Python 3.11+
- 一个兼容 OpenAI API 的 LLM 服务

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行

**Web 界面（推荐）：**
```bash
streamlit run app.py
```

浏览器访问 `http://localhost:8501`

**命令行模式：**
```bash
python main.py
```

## 输入流程

Web 界面分步引导：

1. **填写活动信息** — 活动类型（LLM 自动校验模糊性）、参与人数（限 50 人以下）、场地类型、预算（可报销/不可报销）、补充说明
2. **确认信息** — 汇总展示所有输入
3. **确认海报信息** — LLM 从策划案提取标题、时间、地点等信息，可编辑修改
4. **执行生成** — 进度条展示运行状态
5. **结果展示** — 所有文件可在线预览和下载

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
│   ├── plan.py          # 策划案生成（含场地推荐）
│   ├── finance.py       # 预算评估（可报销/不可报销）
│   ├── execute.py       # 日程、主持稿、通知
│   ├── promote.py       # 海报生成（qwen-image-2.0）、推文
│   ├── risk.py          # 风险评估
│   ├── feedback.py      # 评价反馈
│   ├── confirm.py       # 信息确认
│   ├── search.py        # 案例搜索
│   ├── ppt.py           # PPT 生成（主持人手卡 + 现场展示）
│   └── html.py          # 公众号推文 HTML
└── output/              # 所有输出文件（自动生成，.gitignore）
    ├── {活动1}/         # 每次运行按活动名+时间戳建会话目录
    │   ├── 活动策划案_*.md
    │   ├── 活动日程_*.md
    │   ├── 主持稿_*.md
    │   ├── 通知文案_*.md
    │   ├── 师生评价反馈_*.md
    │   ├── 满意度问卷_*.md
    │   ├── 风险评估报告_*.md
    │   ├── 主持人手卡_*.pptx
    │   ├── 活动现场展示_*.pptx
    │   ├── 活动回顾_*.html
    │   └── 海报_*.png
    ├── {活动2}/
    └── ...
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

所有生成的文件统一保存在 `output/` 目录下。每次运行按活动名和时间戳创建独立的会话目录（如 `output/读书分享会_20260716_120000/`），所有文件生成在同一目录中：

| 文件 | 内容 | 格式 |
|------|------|------|
| `活动策划案_*.md` | 活动策划方案 | Markdown |
| `活动日程_*.md` | 活动日程 | Markdown |
| `主持稿_*.md` | 主持串场词 | Markdown |
| `通知文案_*.md` | 活动通知 | Markdown |
| `海报_*.png` | 海报图片 | PNG |
| `活动回顾_*.html` | 公众号推文 | HTML |
| `主持人手卡_*.pptx` | 主持人手卡 PPT | PPTX |
| `活动现场展示_*.pptx` | 现场展示 PPT | PPTX |
| `师生评价反馈_*.md` | 师生评价反馈 | Markdown |
| `满意度问卷_*.md` | 满意度问卷 | Markdown |
| `风险评估报告_*.md` | 风险评估报告 | Markdown |

## 技术栈

- **LangGraph** — 多 Agent 编排与状态管理
- **LangChain** — LLM 调用封装
- **Streamlit** — Web 交互界面
- **python-pptx** — PowerPoint 生成
- **qwen-image-2.0** — AI 海报生成
- **SQLite** — 长期记忆存储