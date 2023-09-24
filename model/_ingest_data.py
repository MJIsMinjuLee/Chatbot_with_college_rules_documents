import os
import re
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS


def ingest_data() :
    try :
        os.environ['OPENAI_API_KEY'] = '키입력'

        filePath = "../docs"
        files = [f for f in os.listdir(filePath) if re.match('.*[.]pdf', f)]

        new_documents = [''] * len(files)
        for file in range(len(files)) :
            loader = PyPDFLoader('../docs/{name}'.format(name = files[file]))
            documents = loader.load()
            for i in range(len(documents)) :
                documents[i] = documents[i].page_content.replace('\n', ' ')
                i += 1
            new_documents[file] = (' ').join(documents)
            file += 1

        new_documents = (' ').join(new_documents)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 450,
            chunk_overlap = 30,
            length_function = len
        )
        #chunk_size=450, chunk_overlap = 30
        
        texts = text_splitter.split_text(new_documents)
        
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_texts(texts, embeddings, distance_strategy = "MAX_INNER_PRODUCT")

        return vectorstore

    except Exception as e :
        print(f'Error : {e}')
        raise ValueError("Failed to load documents")