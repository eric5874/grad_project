import streamlit as st
import requests
import time
import os
import var

HOST = os.getenv('HOST', 'localhost:8000')

# Create login page
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login_tab, register_tab = st.tabs(['Login', 'Register'])

    with login_tab:
        with st.form(key='login_form'):
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            submit = st.form_submit_button('Login')

            if submit:
                response = requests.post(f'http://{HOST}/login', json={'username': username, 'password': password})
                if response.status_code == 200:
                    if response.json()['logged_in']:
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = username
                        st.success('Logged in successfully')
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error('Invalid username or password')
                else:
                    st.error('Error logging in')

    with register_tab:
        with st.form(key='register_form'):
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            submit = st.form_submit_button('Register')

            if submit:
                response = requests.post(f'http://{HOST}/register', json={'username': username, 'password': password})
                if response.status_code == 200:
                    st.success('Registered successfully')
                else:
                    st.error('Username already exists')

else:
    st.title('資工所資源網站')
    col1, col2 = st.columns([1, 4])


    with col2:
        st.write(f'### {st.session_state["username"]}，歡迎回來！')
        ntu = st.expander('台大資工所')
        nthu = st.expander('清大資工所')
        nycu = st.expander('交大資訊聯招')
        ncku = st.expander('成大資訊聯招')
        ncu = st.expander('中央資工所')
        nsysu = st.expander('中山資工所甲組')
        nchu = st.expander('中興資工所')
        ccu = st.expander('中正資工所')
        
        ntu.write("""
        1. [黑底三角np理論](https://www.academia.edu/44422461/Computers_and_intractability_a_guide_to_the_theory_of_np_completeness_garey_amp_johnson)
        2. [台灣大學ocw](https://ocw.aca.ntu.edu.tw/ntu-ocw/category/3)
        """)

        nthu.write("""
        1. [清大資工所考古題](https://www.lib.nthu.edu.tw/library/department/ref/exam/eecs/cs.html)
        2. [清華大學ocw](https://ocw.nthu.edu.tw/ocw/)
        """)

        nycu.write("""
        1. [陽明交通ocw](https://ocw.nycu.edu.tw/)
        """)

        ncku.write("""
        1. [成功大學ocw](https://i-ocw.ctld.ncku.edu.tw/)
        2. [成功大學資工所考古](https://exam.lib.ncku.edu.tw/master_subject.php?department_code=OD12)
        """)

        ncu.write("""
        1. [中央大學ocw](https://ocw.ncu.edu.tw/)
        2. [中央資工所考古](https://rapid.lib.ncu.edu.tw/cexamn/EC02.html)
        """)

        nsysu.write("""
        1. [中山大學ocw](https://digital.nsysu.edu.tw/611-2/)
        2. [中山大學考古](https://lis.nsysu.edu.tw/p/412-1001-6014.php?Lang=zh-tw)
        """)

        nchu.write("""
        1. [中興大學ocw](https://cdtl.video.nchu.edu.tw/dir/1206)
        """)

        ccu.write("""
        1. [中正大學ocw](https://ocw.ccu.edu.tw/)
        2. [中正大學資工所考古](https://cs.ccu.edu.tw/p/404-1094-6488.php?Lang=zh-tw)
        """)

        st.write('### 新增收藏')
        with st.form(key='favor_form'):
            book = st.selectbox('書籍', list(var.RESOURCE.keys()), key='book', index=0)
            submit = st.form_submit_button('新增')

            if submit:
                response = requests.post(f'http://{HOST}/favor', json={'username': st.session_state['username'], 'bookname': book})
                if response.status_code == 200:
                    st.success('新增成功')
                else:
                    st.error('新增失敗')