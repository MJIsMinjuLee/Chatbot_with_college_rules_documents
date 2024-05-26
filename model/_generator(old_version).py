###Notice!!
###This file is the oldest version of _generator.py
###This uses ConversationalRetrievalChain.from_llm which is REALLY different from Agent module
###I DO NOT RECOMMEND THIS AS  YOUR CHAT BOT MODULE !

import os
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.prompt import PromptTemplate


os.environ['OPENAI_API_KEY'] = '키입력'

#query 임베딩 모델
embeddings = OpenAIEmbeddings()

#gpt 모델 기본값 설정
model = ChatOpenAI(
    temperature = 0, model_name = 'gpt-3.5-turbo'
) #gpt-3.5-turbo(4,097 token)

chat_history = []

def old_generator(question) :
    #로컬에 저장해 놓은 vectorstore 불러오기
    filePath = "../docs/faiss_index_with_fifteen"
    vectorstore = FAISS.load_local(folder_path = filePath, embeddings = embeddings)
    retriever = vectorstore.as_retriever(search_type = 'similarity', search_kwargs = {'k': 8})

    #prompt engineering : prompt 설정 (+ 추가: 간결하게 대답하라)
    _template = """You must answer only in Korean. You must answer based on the given document. Answer as concisely as possible. If you don't understand a question, answer in Korean, 'I didn't understand.'"""
    question_template = _template + question

    #문서 검색을 통해 답변 얻기
    qa_database = ConversationalRetrievalChain.from_llm(llm = model,
                                                        retriever = retriever,
                                                        verbose = True,
                                                        return_source_documents = True,
                                                        )
    result = qa_database({'question' : question_template, 'chat_history' : chat_history})
    chat_history.append((question, result['answer']))

    #질문이 '아니오'일 경우, 메모리 및 history 초기화
    if question == '아니오' :
        chat_history.clear()

        return chat_history
    
    return print(result['answer'])

if __name__ == '__main__' :
    #old_generator('제적당했을 경우에 장학금을 받을 수 있는가?')
    #휴학 기간이 종료된 후 일정 기간 내에 복학하지 않을 경우, 제적 처리될 수 있으며, 이 경우 장학금 지급이 중지됩니다.
    #old_generator('장학금을 받을 수 있는 조건에는 무엇이 있는지 제가 물어본 적이 있나요?')
    #네.1~6까지
    #old_generator('제적되었을 경우에 장학금을 받을 수 있나요?')
    #old_generator('징계의 대상은 누구인가?')
    #old_generator('포상의 종류에는 무엇이 있는가?')
    #old_generator('생활관 종류는 무엇이 있는가?')
    #old_generator('장학금은 이중으로 받을 수 있나?')
    #old_generator('장학금의 수혜 기간은?')
    #old_generator('신입생은 휴학 가능한가?')
    #old_generator('정문의 주차장 운영 시간은?')
    old_generator('징계의 종류 중에서 유기정학 이상의 징계는 무엇이 있는가?') 