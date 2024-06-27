import streamlit as st
import requests
import time
import os

HOST = os.getenv('HOST', 'localhost:8000')

@st.experimental_dialog('新增討論')
def new_discussion():
    with st.form(key='new_discussion_form'):
        title = st.text_input('標題')
        content = st.text_area('內容')
        submit = st.form_submit_button('新增')

        if submit:
            response = requests.post(f'http://{HOST}/discussion', json={'title': title, 'content': content, 'username': st.session_state['username']})
            if response.status_code == 200:
                st.success('新增成功')
                time.sleep(1)
                st.rerun()
            else:
                st.error('新增失敗')

def get_all_discussions():
    response = requests.get(f'http://{HOST}/discussion')
    if response.status_code == 200:
        return response.json()['discussions']
    return []

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.warning('請先登入')

elif st.session_state['logged_in']:
    dis_left_col, dis_right_col = st.columns([7,3])
    
    with dis_left_col:
        st.title('討論區')
    
    with dis_right_col:
        if st.button('新增討論'):
            new_discussion()

    st.divider()

    discussions = get_all_discussions()
    for discussion in discussions:
        info_card = st.container(border=True)
        info_card.title(f'{discussion["title"]}')
        info_card.write(discussion['content'])
        info_card.write(f'發布者: {discussion["username"]}')

