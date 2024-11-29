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

# 環境變數初始化
OLLAMA_SERVER = os.getenv("OLLAMA_SERVER", "http://localhost:11434")
BACKEND_SERVER = os.getenv("BACKEND_SERVER", "http://localhost:8081")
OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# check if chat_model is in session state
if "chat_model" not in st.session_state:
    st.session_state["chat_model"] = "llama-3.2-90b-vision-preview-groq"
    # st.session_state["chat_model"] = "gemma2-9b-it-groq"
    # st.session_state["chat_model"] = "gpt-3.5-turbo-openai"

# Prompt 模版
CONVERT_PROMPT = ChatPromptTemplate.from_template(
    "你是一個高級演算法，可以把用戶提到的大學轉換成英文縮寫。"
    "你可以參考 reference，return format: NTU, (no need further responds.) user input: {user_input}, reference: {reference}"
)
GET_NEWS_PROMPT = ChatPromptTemplate.from_template(
    "請你判斷用戶是否提到要查詢的新聞標題，若是沒有明確標題，留空即可。"
    "return format: 大學名稱, 新聞標題, (no need further responds.) user input: {user_input}"
)
REFERENCE = "NTU : 台灣大學, NYCU : 陽明交通, NCKU : 成功大學, NCU : 中央大學"

# 初始化聊天歷史
def init_chat_history() -> ChatPromptTemplate:
    if "chat_history" not in st.session_state:
        template = ChatPromptTemplate.from_messages([
            ("system", "你是個推甄資訊助理，可以幫助用戶查詢大學或研究所的最新消息。"),
        ])
        st.session_state["chat_history"] = template
    return st.session_state["chat_history"]

# 查詢新聞列表
def news_search(universities: list[str]) -> dict[str, list[str]]:
    return_data = {}
    for university in universities:
        try:
            response = requests.get(f"http://{BACKEND_SERVER}/news/{university}")
            response.raise_for_status()  # 確保 HTTP 狀態碼為 200
            return_data[university] = response.json().get("news", [])[:5]  # 最多返回 5 條新聞
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching news for {university}: {e}")
    return return_data

# 獲取新聞詳細內容
def get_news_detail(university: str, news: str) -> str:
    try:
        response = requests.get(f"http://{BACKEND_SERVER}/news_link/{university}/{news}")
        response.raise_for_status()
        link = response.json().get("link", "")
        if university == "NTU":
            return ntu_read_news_content(link)
        elif university == "NCKU":
            return ncku_read_news_content(link)
        elif university == "NYCU":
            return nycu_read_news_content(link)
        elif university == "NCU":
            return ncu_read_news_content(link)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching news detail: {e}")
    return "無法獲取新聞內容。"

# 主介面
header_col, embeddings_select_col = st.columns([0.7, 0.3])

with header_col:
    st.header("Chat Assistant")

st.divider()

# 初始化聊天歷史
chat_tmp = init_chat_history()

# 確定聊天模型
if st.session_state["chat_model"].endswith("groq"):
    llm = ChatGroq(model=st.session_state["chat_model"][:-5], api_key=GROQ_API_KEY)
elif st.session_state["chat_model"].endswith("openai"):
    llm = ChatOpenAI(model=st.session_state["chat_model"][:-7], api_key=OPEN_API_KEY)
else:
    llm = ChatOllama(model=st.session_state["chat_model"], base_url=OLLAMA_SERVER)

user_input = st.chat_input("You can start a conversation with the AI Teaching Assistant here.")
chain = chat_tmp | llm | StrOutputParser()

if user_input:
    schools = []
    with st.status("Extracting information..."):
        convert_chain = CONVERT_PROMPT | llm | StrOutputParser()
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
        get_news_chain = GET_NEWS_PROMPT | llm | StrOutputParser()
        get_news_response = get_news_chain.invoke({"user_input": user_input})
        if get_news_response:
            try:
                specific_news_name = get_news_response.split(", ")[1]
            except IndexError:
                pass
        st.write(f"Specific news name: {specific_news_name}")
        if specific_news_name:
            extracted_info += get_news_detail(schools[0], specific_news_name)

    with st.status("Digital Assistant Thinking..."):
        st.write(f"Database information: {extracted_info}")
        chat_tmp.append(SystemMessage(f"Database information: {extracted_info}"))
        chat_tmp.append(HumanMessage(user_input))
        response = chain.invoke({})
        chat_tmp.append(AIMessage(response))
        st.session_state["chat_history"] = chat_tmp

# 顯示聊天歷史
for message in st.session_state["chat_history"].messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.write(message.content)
