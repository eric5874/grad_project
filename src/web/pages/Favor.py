import streamlit as st
import requests
import time
import os
import var

HOST = os.getenv('HOST', 'localhost:8000')

def get_all_favoured():
    response = requests.get(f'http://{HOST}/favor?username={st.session_state["username"]}')
    if response.status_code == 200:
        return response.json()['favours']
    return []

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.warning('You need to login to access this page')
else:
    st.title('蒐藏')
    
    favours = get_all_favoured()

    for favour in favours:
        temp_card = st.container(border=True)
        temp_card.markdown(f"### {favour}")
        temp_card.markdown(f"[Link]({var.RESOURCE[favour]})")