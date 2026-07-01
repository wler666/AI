import os
from dotenv import load_dotenv
from langchain_openai import OpenAI, ChatOpenAI

load_dotenv()
api_key = os.getenv("API_KEY")
if api_key is None:
    raise ValueError(
        "没有读取到有效的 API Key！请检查项目目录下是否有 .env 文件，"
    )
llm = ChatOpenAI(
    model="qwen3.7-max-2026-06-08",
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.7,
)
if __name__ == "__main__":
    print("向千问发送测试请求\n")
    response=llm.invoke("请用一句话介绍一下你自己。")
    print(response.content)