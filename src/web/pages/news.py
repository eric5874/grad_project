import streamlit as st
from news_utl.ntu_csie import fetch_ntu_csie_news
from news_utl.nycu_csie import fetch_nycu_admissions_info

def display_news():
    st.write('### 最新消息')
    
    # Create Markdown table header with date column for NTU
    md_template_ntu = """| NTU 標題 | 日期 | 連結 |\n| ---- | ---- | ---- |\n"""
    md_template_nycu = """| NYCU 標題 | 連結 |\n| ---- | ---- |\n"""
    
    # Fetch NTU news and include date
    ntu_news_df = fetch_ntu_csie_news()
    for i, row in ntu_news_df.iterrows():
        full_link = f"https://www.csie.ntu.edu.tw/{row['link']}"
        md_template_ntu += f"| {row['title']} | {row['date']} | [Link]({full_link}) |\n"
    
    # Fetch NYCU news and exclude date
    nycu_news_df = fetch_nycu_admissions_info()
    for i, row in nycu_news_df.iterrows():
        full_link = f"https://www.cs.nycu.edu.tw/admission/graduate/{row['link']}"
        md_template_nycu += f"| {row['title']} | [Link]({full_link}) |\n"
    
    # Display both NTU and NYCU news tables
    st.markdown("### NTU 最新消息")
    st.markdown(md_template_ntu)
    
    st.markdown("### NYCU 最新消息")
    st.markdown(md_template_nycu)
display_news()