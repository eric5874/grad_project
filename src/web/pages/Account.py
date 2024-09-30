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

    # Self-introduction section
    st.subheader('自我介紹')
    intro_response = requests.get(f'http://{HOST}/introduction', params={'username': st.session_state['username']}).json()
    introduction = intro_response.get('introduction', '')

    introduction_input = st.text_area('更新自我介紹', value=introduction)
    if st.button('更新自我介紹'):
        requests.post(f'http://{HOST}/introduction', json={'username': st.session_state['username'], 'introduction': introduction_input})
        st.success('自我介紹更新成功')
        time.sleep(0.4)
        st.rerun()
