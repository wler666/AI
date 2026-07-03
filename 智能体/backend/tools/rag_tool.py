import os
from dotenv import load_dotenv
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
from langchain_core.tools import tool

load_dotenv()
api_key = os.getenv("API_KEY")

CURRENT_DIR = os.path.dirname(os.path.dirname(__file__))
DB_DIR = os.path.join(CURRENT_DIR, "vector_store")

embeddings = DashScopeEmbeddings(
    model="text-embedding-v2",
    dashscope_api_key=api_key,
)

vector_db = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embeddings,
)


@tool
def search_company_knowledge(query: str) -> str:
    """
    在公司知识库中检索相关信息，知识库包含公司简介和2025年9月营销情况报告。
    当用户询问公司相关信息、9月营销数据、销售情况等问题时，使用这个工具。

    参数：
    query: 要检索的问题或关键词

    返回：从知识库中找到的相关文本片段，如果没找到相关内容会说明这一点。
    """
    results = vector_db.similarity_search(query, k=4)
    print(f"这次搜索返回了 {len(results)} 个片段")
    if not results:
        return "知识库中没有找到相关信息。"

    combined = "\n\n---\n\n".join([doc.page_content for doc in results])
    return combined


if __name__ == "__main__":
    answer = search_company_knowledge.invoke({"query": "9月营销总投入是多少"})
    print(answer)