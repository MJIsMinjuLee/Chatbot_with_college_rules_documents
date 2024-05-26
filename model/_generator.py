import os
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import AgentTokenBufferMemory
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder
from langchain.agents import AgentExecutor


os.environ['OPENAI_API_KEY'] = '키입력'

#query 임베딩 모델
embeddings = OpenAIEmbeddings()

#gpt 모델 기본값 설정
model = ChatOpenAI(
    temperature = 0, model_name = 'gpt-3.5-turbo'
) #gpt-3.5-turbo(4,097 token)

#메모리
memory_key = 'history'
memory = AgentTokenBufferMemory(llm = model, memory_key = memory_key, max_token_limit = 2000)

def generator(question) :
    #로컬에 저장해 놓은 vectorstore 불러오기
    filePath = "../docs/faiss_index_with_fifteen"
    vectorstore = FAISS.load_local(folder_path = filePath, embeddings = embeddings)
    retriever = vectorstore.as_retriever(search_type = 'similarity', search_kwargs = {'k': 4})

    #검색용 도구 설정
    tool = create_retriever_tool(
        retriever,
        "school_rules",
        "Searches and returns documents regarding the School rules of Seoul national university of science and technology."
    )
    tools = [tool]

    #prompt engineering : prompt 설정 (+ 추가: 간결하게 대답하라)
    system_message = SystemMessage(
        content = (
            "You must answer only in Korean."
            "You must answer based on the given document."
            "Answer as concisely as possible."
            "If you don't understand a question, answer in Korean, 'I didn't understand.'"
        )
    )
    prompt = OpenAIFunctionsAgent.create_prompt(
        system_message = system_message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name = memory_key)]
    )
    
    #문서 검색을 통해 답변 얻기
    agent = OpenAIFunctionsAgent(llm = model, tools = tools, prompt = prompt)
    agent_executor = AgentExecutor(
        agent = agent,
        tools = tools,
        memory = memory,
        verbose = True,
        return_intermediate_steps = True,
        max_iterations = 2, #Agent Observation-Thought 과정 횟수 제한
        )

    result = agent_executor({'input' : question})

    #질문이 '아니오'일 경우, 메모리 및 history 초기화
    if question == '아니오' :
        memory.clear()

        return memory
    
    return result['output']

#실험 진행
if __name__ == '__main__' :
    #generator('공로상은 누구에게 수여하는가?')
    #generator('포상의 종류에는 무엇이 있는가?')
    #generator('생활관 종류는 무엇이 있는가?')
    #generator('장학금은 이중으로 받을 수 있나?')
    #generator('장학금의 수혜 기간은?')
    #generator('신입생은 휴학 가능한가?')
    #generator('정문의 주차장 운영 시간은?')
    generator('징계의 종류 중에서 유기정학 이상의 징계는 무엇이 있는가?') 