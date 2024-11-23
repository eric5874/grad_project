from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage
from langchain_groq.chat_models import ChatGroq
from langchain_openai.chat_models import ChatOpenAI
import streamlit as st
import requests
import os

OLLAMA_SERVER = os.getenv("OLLAMA_SERVER", "http://localhost:11434")
BACKEND_SERVER = os.getenv("BACKEND_SERVER", "http://localhost:8081")
OPEN_API_KEY = os.getenv("OPENAI_API_KEY", "sk_test_1234567890")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "gsk_test_1234567890")
CONVERT_PROMPT = ChatPromptTemplate.from_template(
    "You are an Top algorithm, you need to according to user input convert school name that user input to school name in database. user input: {user_input}, reference: {reference}"
)
REFERENCE = "NTU : 台灣大學, NYCU : 陽明交通, NCKU : 成功大學, NCU : 中央大學"

if 'chat_model' not in st.session_state:
    st.session_state['chat_model'] = "llama-3.2-90b-text-preview-groq"

def embeddings_search(user_input: str, embedding_name: str) -> dict:
    # user_input = ts.translate_text(user_input, translator=TRANSLATOR_PROVIDER, to_language="en")
    response = requests.post(f"{BACKEND_SERVER}/embed_query", json={"user_input": user_input, "embedding_name": embedding_name})
    if response.status_code == 200:
        return response.json()
    else:
        return {"embeddings": [], "time": 0}

def news_search(universities: list[str]) -> dict[str, list[str]]:
    return_data = {}
    for university in universities:
        response = requests.get(f"{BACKEND_SERVER}/news/{university}")
        if response.status_code == 200:
            return_data[university] = response.json()['news'][0:3]
    return return_data

def init_chat_history() -> ChatPromptTemplate:
    if 'chat_history' not in st.session_state:
        template = ChatPromptTemplate.from_messages([
            ('system', "You are an AI Infomation Assistant, you need to help users with their questions based on the content of database."),
        ])
        st.session_state['chat_history'] = template
    else:
        template = st.session_state['chat_history']
    return template

header_col, embeddings_select_col = st.columns([0.7,0.3])

with header_col:
    st.header("Chat")
    
st.divider()

chat_tmp = init_chat_history()
# llm = ChatOllama(model=st.session_state['chat_model'], base_url=OLLAMA_SERVER)
if st.session_state['chat_model'][-4:] == "groq":
    llm = ChatGroq(model=st.session_state['chat_model'][0:-5], api_key=GROQ_API_KEY)
elif st.session_state['chat_model'][-6:] == "openai":
    llm = ChatOpenAI(model=st.session_state['chat_model'][0:-7], api_key=OPEN_API_KEY)
else:
    llm = ChatOllama(model=st.session_state['chat_model'], base_url=OLLAMA_SERVER)
user_input = st.chat_input("You can start a conversation with the AI Teaching Assistant here.")
chain = chat_tmp | llm | StrOutputParser()

if user_input:
    schools = []
    with st.status("Extracting information..."):
        # for embedding in embeddings_search_result["results"]:
        #     extract_template = EXTRACT_PROMPT
        #     extract_chain = extract_template | llm | StrOutputParser()
        #     extract_response = extract_chain.invoke({"user_input": user_input, "content": embedding["page_content"]})
        #     extracted_info += f"Page {embedding['metadata']['page']}: {extract_response}\n"
        convert_prompt = CONVERT_PROMPT
        convert_chain = convert_prompt | llm | StrOutputParser()
        convert_response = convert_chain.invoke({"user_input": user_input, "reference": REFERENCE})
        schools = convert_response.split(", ")

    with st.status("Searching for Database..."):
        news_search_result = news_search(schools)
        news_search_result_str = ""
        for school, news in news_search_result.items():
            news_search_result_str += f"{school}: {news}\n"
        extracted_info = news_search_result_str

    with st.status("Digital Assistant Thinking..."):
        chat_tmp.append(SystemMessage(f"Database infomation sort by schools: {extracted_info}"))
        chat_tmp.append(HumanMessage(user_input))
        response = chain.invoke({})
        chat_tmp.append(AIMessage(response))
        st.session_state['chat_history'] = chat_tmp

for message in st.session_state['chat_history'].messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            # if enable_translation:
            #     st.write(ts.translate_text(message.content, translator=TRANSLATOR_PROVIDER, to_language="zh-TW"))
            # else:
            st.write(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            # if enable_translation:
            #     st.write(ts.translate_text(message.content, translator=TRANSLATOR_PROVIDER, to_language="zh-TW"))
            # else:
            st.write(message.content)