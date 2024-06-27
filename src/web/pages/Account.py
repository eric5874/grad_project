import streamlit as st
import requests
import time
import os
import base64
from io import BytesIO
from PIL import Image

HOST = os.getenv('HOST', 'localhost:8000')

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.warning('請先登入')
    
elif st.session_state['logged_in']:
    col1, col2 = st.columns([5,5])
    with col1:
        st.title('我的帳戶')
        st.markdown(f'### {st.session_state["username"]}')
    avatar_base64 = requests.get(f'http://{HOST}/avatar', params={'username': st.session_state['username']}).json()['avatar']
    avatar = Image.open(BytesIO(base64.b64decode(avatar_base64)))
    with col2:
        st.image(avatar, width=200)