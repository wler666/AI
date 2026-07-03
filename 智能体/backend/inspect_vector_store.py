import os
from dotenv import load_dotenv
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma

load_dotenv()
api_key = os.getenv("DASHSCOPE_API_KEY")

CURRENT_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(CURRENT_DIR, "vector_store")

embeddings = DashScopeEmbeddings(
    model="text-embedding-v2",
    dashscope_api_key=api_key,
)

vector_db = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embeddings,
)

result = vector_db.get()

print(f"数据库里一共存了 {len(result['ids'])} 个文本片段\n")

for i in range(len(result["ids"])):
    doc_id = result["ids"][i]
    content = result["documents"][i]
    print(f"--- 第{i + 1}个片段（id: {doc_id}） ---")
    print(content)
    print()