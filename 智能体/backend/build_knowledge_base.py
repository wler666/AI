import os
from dotenv import load_dotenv
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
load_dotenv()
api_key = os.getenv("API_KEY")
CURRENT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(CURRENT_DIR, "data")
DB_DIR = os.path.join(CURRENT_DIR, "vector_store")
embeddings = DashScopeEmbeddings(
    model="text-embedding-v2",
    dashscope_api_key=api_key,
)
def build_knowledge_base():
    all_chunks=[]

    for file_name in os.listdir(DATA_DIR):
        if not file_name.endswith(".docx"):
            continue

        file_path = os.path.join(DATA_DIR, file_name)
        print(f'正在读取{file_name}')
        loader = Docx2txtLoader(file_path)
        documents=loader.load()
        splitter=RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50
        )
        chunk=splitter.split_documents(documents)
        all_chunks.extend(chunk)
        print(f"分出{len(all_chunks)}个文本片段")
        Chroma.from_documents(
            documents=all_chunks,
            embedding=embeddings,
            persist_directory=DB_DIR,
        )
        print("知识库构建完成！")
if __name__ == "__main__":
    build_knowledge_base()