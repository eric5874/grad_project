import streamlit as st
import requests
import time
import os
import base64
from io import BytesIO
from PIL import Image
from datetime import datetime

HOST = os.getenv('HOST', 'localhost:8000')

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.warning('請先登入')
    
elif st.session_state['logged_in']:
    col1, col2 = st.columns([3, 7])
    with col1:
        st.title('我的帳戶')
        st.markdown(f'### {st.session_state["username"]}')
    avatar_base64 = requests.get(f'http://{HOST}/avatar', params={'username': st.session_state['username']}).json()['avatar']
    avatar = Image.open(BytesIO(base64.b64decode(avatar_base64)))
    with col2:
        left_co, cent_co, last_co = st.columns(3)
        with cent_co:
            st.image(avatar, width=200)

        # Avatar upload
        img_file_buffer = st.file_uploader('Upload a JPG image', type=['jpg'])
        if img_file_buffer is not None:
            if st.button('Upload'):
                img = Image.open(img_file_buffer)
                img_base64 = base64.b64encode(img_file_buffer.getvalue()).decode()
                requests.post(f'http://{HOST}/avatar', json={'username': st.session_state['username'], 'avatar': img_base64})
                st.success('Avatar uploaded successfully')
                time.sleep(0.4)
                st.rerun()

    # Mood diary section
    st.subheader('心情日記')
    diary_response = requests.get(f'http://{HOST}/diary', params={'username': st.session_state['username']}).json()
    diary = diary_response.get('diary', '')

    diary_input = st.text_area('撰寫或更新心情日記', value=diary)
    if st.button('更新心情日記'):
        current_date = datetime.now().strftime('%Y/%m/%d')
        updated_diary = f"{diary_input} ({current_date})"
        requests.post(f'http://{HOST}/diary', json={'username': st.session_state['username'], 'diary': updated_diary})
        st.success('心情日記更新成功')
        time.sleep(0.4)
        st.rerun()
