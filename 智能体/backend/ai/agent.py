import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


from tools.email_tool import send_email
from tools.chart_tool import generate_sales_chart
from tools.rag_tool import search_company_knowledge

load_dotenv()
api_key = os.getenv("DASHSCOPE_API_KEY")

llm = ChatOpenAI(
    model="qwen-plus",
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.3,
)

tools = [send_email, generate_sales_chart, search_company_knowledge]

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "你是耀辰智能科技有限公司的智能助理，具备以下三项能力：\n\n"
     "1. 知识库查询：当用户询问关于公司介绍、9月营销情况、销售数据等问题时，"
     "必须先调用 search_company_knowledge 工具，从知识库中检索相关信息，"
     "再基于检索到的真实内容组织回答，禁止凭空编造数据或事实。\n\n"
     "2. 图表生成：当用户明确要求生成图表、可视化数据时，调用 generate_sales_chart 工具，"
     "工具会返回图片保存的文件路径。\n\n"
     "3. 邮件发送：当用户希望把分析结果、图表或其他内容发送到邮箱时，调用 send_email 工具。"
     "如果要发送的是刚生成的图表，把图表工具返回的文件路径，作为 attachment_path 参数传入。\n\n"
     "如果用户的需求信息不完整，先向用户确认清楚，而不要凭空猜测。"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True,
)

if __name__ == "__main__":
    while True:
        user_input = input("\n你：")
        if user_input.strip().lower() in ["退出", "exit", "quit"]:
            break

        result = agent_executor.invoke({"input": user_input})
        print("\n智能体：", result["output"])