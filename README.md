智能助理系统（企业知识库智能体）

基于 LangChain + 通义千问（Qwen）打造的企业级 AI 智能体应用，具备知识库问答（RAG）、数据可视化、邮件自动化通知三项核心能力，并支持前端对话式交互界面。


项目为学习/演示性质，涉及的公司名称"耀辰智能科技有限公司"及相关业务数据均为虚构示例。




✨ 功能特性


🧠 RAG 知识库问答：基于公司简介、营销报告等真实文档构建向量知识库，回答问题时先检索、再生成，减少大模型幻觉
📊 数据可视化：一句话生成营销渠道投入分析图表，自动保存为图片
📧 邮件自动化：支持将文字分析结果、图表以邮件形式（含附件）发送到指定邮箱
🤖 智能体自主决策：基于 LangChain Tool Calling Agent，AI 自主判断该调用哪个工具、是否需要连续调用多个工具（如"生成图表 → 作为附件发邮件"）
💬 对话式前端界面：淡蓝色主题聊天界面，支持文本消息与图表图片内嵌显示



🖥️ 技术栈

分类技术大模型通义千问（Qwen，阿里云百炼，兼容 OpenAI 接口）智能体框架LangChain（Tool Calling Agent）向量数据库ChromaDB文本向量化DashScope Embedding (text-embedding-v2)后端服务FastAPI + Uvicorn数据可视化Matplotlib邮件发送Python smtplib（QQ邮箱 SMTP）前端HTML / CSS / JavaScript（原生，无框架依赖）


📁 项目结构

智能体/
├── front/                          # 前端聊天界面
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── backend/                        # 后端服务
    ├── main.py                     # FastAPI 入口，对外提供 /api/chat 接口
    ├── requirements.txt            # 依赖清单
    ├── .env.example                # 环境变量模板
    ├── build_knowledge_base.py     # 知识库构建脚本（一次性运行）
    │
    ├── ai/
    │   └── agent.py                # 智能体核心：整合大模型 + 工具 + 提示词
    │
    ├── tools/                      # 智能体可调用的工具集
    │   ├── email_tool.py           # 邮件发送工具（支持附件）
    │   ├── chart_tool.py           # 营销数据图表生成工具
    │   └── rag_tool.py             # 知识库检索工具
    │
    ├── data/                       # 知识库原始文档（.docx）
    ├── vector_store/               # 向量数据库存储目录（自动生成）
    └── outputs/charts/             # 图表生成输出目录（自动生成）


🚀 快速开始

1. 环境准备

需要 Python 3.10+，建议使用 conda 创建独立虚拟环境：

bashconda create -n agent_env python=3.10 -y
conda activate agent_env

2. 安装依赖

bashcd backend
pip install -r requirements.txt

3. 配置环境变量

复制 .env.example 为 .env，并填入以下信息：

DASHSCOPE_API_KEY=你的阿里云百炼API Key
QQ_EMAIL=你的QQ邮箱地址
QQ_AUTH_CODE=QQ邮箱SMTP授权码（非登录密码）


百炼 API Key 获取地址：https://bailian.console.aliyun.com



4. 构建知识库

将公司相关文档（.docx）放入 backend/data/ 目录，然后运行：

bashpython build_knowledge_base.py

5. 启动后端服务

bashuvicorn main:app --reload --port 8000

服务启动后访问 http://127.0.0.1:8000/docs 可查看接口文档并直接测试。

6. 打开前端界面

直接用浏览器打开 front/index.html 即可开始对话（默认请求本地 8000 端口的后端服务）。


💡 使用示例

在对话框中输入：


介绍一下耀辰智能科技有限公司 → 触发知识库检索，基于真实文档内容回答
9月营销总投入是多少，ROI怎么样 → 检索营销报告并总结关键数据
帮我生成一份9月销售分析图表 → 调用图表工具，在对话气泡中直接显示图片
生成9月销售图表，然后发到我邮箱 → 智能体依次调用图表工具与邮件工具，自动将图表作为附件发送



🧩 核心设计说明


图表数据使用结构化数据而非大模型解析文档：避免大模型在读取数字时出现"幻觉"，保证图表数字与源文档 100% 一致
RAG 检索工具只负责"找证据"，不负责"下结论"：检索结果原样返回给智能体，由大模型基于真实片段组织语言，降低编造风险
chunk_size=300, chunk_overlap=50：在保留语义完整性与检索精度之间取得平衡，重叠区间避免关键信息被切片边界打断
AgentExecutor(return_intermediate_steps=True)：用于在后端提取工具调用的中间结果（如图表文件路径），实现前端图片展示与邮件附件功能



⚠️ 免责声明

本项目所使用的公司名称、业务数据、财务数据均为虚构示例，仅用于 AI 智能体与 RAG 技术的学习和演示，不代表任何真实企业的经营情况。
