###Notice!!
###This file is the same one with _generator.py
###The only difference is whether it show intermediate steps or not!

import os
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.tools import format_tool_to_openai_function #which is only difference from _generator.py
from langchain.chat_models import ChatOpenAI
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import AgentTokenBufferMemory
from langchain.schema.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder
from langchain.agents import AgentExecutor


os.environ['OPENAI_API_KEY'] = '키입력'

#Query Embedding Model
embeddings = OpenAIEmbeddings()

model = ChatOpenAI(temperature = 0, model_name = 'gpt-3.5-turbo')
#gpt-3.5-turbo(4,097 token)

#Memory
memory_key = 'history'
memory = AgentTokenBufferMemory(llm = model, memory_key = memory_key, max_token_limit = 2000)

filePath = "../docs/faiss_index_with_fifteen"
vectorstore = FAISS.load_local(folder_path = filePath, embeddings = embeddings)
retriever = vectorstore.as_retriever(search_type = 'similarity', search_kwargs = {'k': 4})

#retrieved_docs = retriever.invoke("장학금")
#print(retrieved_docs)

tool = create_retriever_tool(
    retriever,
    "school_rules",
    "Searches and returns documents regarding the School rules of Seoul national university of science and technology."
    )
tools = [tool]

system_message = SystemMessage(
    content = (
        "You must answer only in Korean."
        "You must answer based on the given document."
        "Answer as concisely as possible."
        "If you don't understand a question, answer in Korean, 'I didn't understand.'"
        ))

prompt = OpenAIFunctionsAgent.create_prompt(
    system_message = system_message,
    extra_prompt_messages=[MessagesPlaceholder(variable_name = memory_key)])

functions = [format_tool_to_openai_function(t) for t in tools] #This part will show you, Observation-Thought steps

agent = OpenAIFunctionsAgent(llm = model, tools = tools, prompt = prompt, functions = functions)

agent_executor = AgentExecutor(
        agent = agent,
        tools = tools,
        memory = memory,
        verbose = True,
        return_intermediate_steps = True,
        max_iterations = 2
        )

result = agent_executor({'input' : '제적되었을 경우 장학금을 받을 수 있는가?'})

print(agent)