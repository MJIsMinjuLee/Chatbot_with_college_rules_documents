import _ingest_data
import os
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings


os.environ['OPENAI_API_KEY'] = '키입력'

embeddings = OpenAIEmbeddings()

#기존의 인덱스에 새로운 파일을 추가하고 싶을 경우, 실행
def add_index(old_storeName, new_storeName) :
    new_vectorstore = _ingest_data.ingest_data()

    old_filePath = "../docs/" + old_storeName
    old_vectorstore = FAISS.load_local(folder_path = old_filePath, embeddings = embeddings)

    old_vectorstore.merge_from(new_vectorstore)
    
    new_filePath = "../docs/" + new_storeName
    old_vectorstore.save_local(folder_path = new_filePath)

    print(f"Success to update FAISS index as {new_storeName}")