import streamlit as st
import requests
import os
from news_utl.ntu_csie import fetch_ntu_csie_news
from news_utl.nycu_csie import fetch_nycu_admissions_info
from news_utl.nckunews import fetch_announcements
from news_utl.ncu_csie import fetch_ncu_news

BACKEND_HOST = os.getenv("HOST", "http://localhost:8081")

def save_news(news:str, university:str):
    url = f"http://{BACKEND_HOST}/news"
    response = requests.post(url, json={"news": news, "university": university})
    return response.json()

def display_news():
    st.write('### 最新消息')
    
    # Markdown table headers
    md_template_ntu = """| NTU 標題 | 日期 | 連結 |\n| ---- | ---- | ---- |\n"""
    md_template_nycu = """| NYCU 標題 | 連結 |\n| ---- | ---- |\n"""
    md_template_ncku = """| NCKU 標題 | 日期 | 連結 |\n| ---- | ---- | ---- |\n"""
    md_template_ncu = """| NCU 標題 | 日期 | 連結 | 單位 |\n| ---- | ---- | ---- | ---- |\n"""
    
    # Fetch NTU news and include date
    ntu_news_df = fetch_ntu_csie_news()
    for i, row in ntu_news_df.iterrows():
        full_link = f"{row['link']}"
        md_template_ntu += f"| {row['title']} | {row['date']} | [Link]({full_link}) |\n"
        _ = save_news(row['title'], "NTU")
    
    # Fetch NYCU news and exclude date
    nycu_news_df = fetch_nycu_admissions_info()
    for i, row in nycu_news_df.iterrows():
        full_link = f"{row['link']}"
        md_template_nycu += f"| {row['title']} | [Link]({full_link}) |\n"
        _ = save_news(row['title'], "NYCU")

    # Fetch NCKU news and include date
    ncku_news_df = fetch_announcements()
    for i, row in ncku_news_df.iterrows():
        full_link = f"{row['link']}"
        md_template_ncku += f"| {row['title']} | {row['date']} | [Link]({full_link}) |\n"
        _ = save_news(row['title'], "NCKU")

    # Fetch NCU news and include date and unit
    ncu_news_df = fetch_ncu_news()
    for i, row in ncu_news_df.iterrows():
        full_link = f"{row['link']}"
        md_template_ncu += f"| {row['title']} | {row['date']} | [Link]({full_link}) | {row['unit']} |\n"
        _ = save_news(row['title'], "NCU")
    
    # Tabs for universities
    ntu_tab, nycu_tab, ncku_tab, ncu_tab = st.tabs(['NTU', 'NYCU', 'NCKU', 'NCU'])

    # Display NTU news
    with ntu_tab:
        st.markdown("### 台大 最新消息")
        st.markdown(md_template_ntu)
    
    # Display NYCU news
    with nycu_tab:
        st.markdown("### 陽明交大 最新消息")
        st.markdown(md_template_nycu)
    
    # Display NCKU news
    with ncku_tab:
        st.markdown("### 成功大學 最新消息")
        st.markdown(md_template_ncku)

    # Display NCU news
    with ncu_tab:
        st.markdown("### 中央大學 最新消息")
        st.markdown(md_template_ncu)

# Call the function to display news
display_news()
