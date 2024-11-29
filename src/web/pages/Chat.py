from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage
from langchain_groq.chat_models import ChatGroq
from langchain_openai.chat_models import ChatOpenAI
from read_news.ntu import read_news_content as ntu_read_news_content
from read_news.ncku import read_news_content as ncku_read_news_content
from read_news.nycu import read_news_content as nycu_read_news_content
from read_news.ncu import read_news_content as ncu_read_news_content
import streamlit as st
import requests
import os

OLLAMA_SERVER = os.getenv("OLLAMA_SERVER", "http://localhost:11434")
BACKEND_SERVER = os.getenv("BACKEND_SERVER", "http://localhost:8081")
OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CONVERT_PROMPT = ChatPromptTemplate.from_template(
    "你是一個高級演算法 可以把用戶提到的大學 轉換成英文縮寫 你可以參考 reference, return format: NTU, (no need futer responds.) user input: {user_input}, reference: {reference}"
)
GET_NEWS_PROMPT = ChatPromptTemplate.from_template(
    "請你判斷用戶是否提到要查詢的新聞標題, 若是沒有明確標題 留空即可 return format: 大學名稱, 新聞標題, (no need futer responds.) user input: {user_input}"
)
REFERENCE = "NTU : 台灣大學, NYCU : 陽明交通, NCKU : 成功大學, NCU : 中央大學"

if 'chat_model' not in st.session_state:
    st.session_state['chat_model'] = "llama-3.2-90b-vision-preview llama-3.1-70b-versatile-groq"

def news_search(universities: list[str]) -> dict[str, list[str]]:
    return_data = {}
    for university in universities:
        response = requests.get(f"http://{BACKEND_SERVER}/news/{university}")
        if response.status_code == 200:
            return_data[university] = response.json()['news'][0:5]
    return return_data

def get_news_detail(university: str, news: str) -> str:
    response = requests.get(f"http://{BACKEND_SERVER}/news_link/{university}/{news}")
    if response.status_code == 200:
        temp = response.json()['link']
        if university == "NTU":
            return ntu_read_news_content(temp)
        elif university == "NCKU":
            return ncku_read_news_content(temp)
        elif university == "NYCU":
            return nycu_read_news_content(temp)
        elif university == "NCU":
            return ncu_read_news_content(temp)
    return ""

def init_chat_history() -> ChatPromptTemplate:
    if 'chat_history' not in st.session_state:
        template = ChatPromptTemplate.from_messages([
            ('system', "你是個推甄資訊助理，可以幫助用戶查詢大學或是研究所的最新消息。"),
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
        st.write(f"Schools: {schools}")

    with st.status("Searching for Database..."):
        news_search_result = news_search(schools)
        news_search_result_str = ""
        for school, news in news_search_result.items():
            news_search_result_str += f"{school}: {news}\n"
        extracted_info = news_search_result_str
        specific_news_name = ""
        if len(schools) == 1:
            specific_news_name = schools[0]
        get_news_prompt = GET_NEWS_PROMPT
        get_news_chain = get_news_prompt | llm | StrOutputParser()
        get_news_response = get_news_chain.invoke({"user_input": user_input})
        if get_news_response:
            try:
                specific_news_name = get_news_response.split(", ")[1]
            except:
                pass
        st.write(f"Specific news name: {specific_news_name}")
        if specific_news_name:
            extracted_info += get_news_detail(schools[0], specific_news_name)

    with st.status("Digital Assistant Thinking..."):
        st.write(f"Database infomation: {extracted_info}")
        chat_tmp.append(SystemMessage(f"Database infomation (you can describe data's abstract and provide link in markdown): {extracted_info}"))
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