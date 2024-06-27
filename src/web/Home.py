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

    with col1:
        st.write('### 目錄')
        st.write('1. [首頁](#目錄)')
        st.write('2. [資源](#resources)')
        st.write('3. [關於](#about)')

    with col2:
        st.write(f'### {st.session_state["username"]}，歡迎回來！')
        data_structure = st.expander('資料結構')
        algorithm = st.expander('演算法')
        linear_algebra = st.expander('線性代數')
        discrete_math = st.expander('離散數學')
        operating_system = st.expander('作業系統')
        computer_architecture = st.expander('計算機結構')
        
        data_structure.write("""
        1. [資料結構可視化](https://visualgo.net/en)
        2. [Fundamentals-of-Data-Structures-in-C](https://caucse.club/wp-content/uploads/2022/05/Fundamentals-of-Data-Structures-in-C-Ellis-Horowitz-Sartaj-Sahni-etc.-.pdf)
        3. [交大彭文志教授ocw](https://ocw.nycu.edu.tw/?course_page=all-course%2Fcollege-of-computer-science%2F%E8%B3%87%E6%96%99%E7%B5%90%E6%A7%8B-data-structure-101%E5%AD%B8%E5%B9%B4%E5%BA%A6-%E8%B3%87%E8%A8%8A%E5%B7%A5%E7%A8%8B%E5%AD%B8%E7%B3%BB-%E5%BD%AD%E6%96%87%E5%BF%97%E8%80%81%E5%B8%AB)""")

        algorithm.write("""
        1. [原文書:楓葉本](https://pd.daffodilvarsity.edu.bd/course/material/book-430/pdf_content)""")

        linear_algebra.write("""
        1. [清大趙啟超教授線性代數ocw](https://ocw.nthu.edu.tw/ocw/index.php?page=course&cid=89)
        2. [黃子嘉線性代數套書](https://www.pcstore.com.tw/tingmao/M20698856.htm)
        3. [線代啟示錄](https://ccjou.wordpress.com/)""")

        discrete_math.write("""
        1. [清大趙啟超教授離散ocw](https://ocw.nthu.edu.tw/ocw/index.php?page=course&cid=288)
        2. [黃子嘉離散數學套書](https://books.dasoedu.com.tw/book/content?book_id=2667)""")

        operating_system.write("""
        1. [清大周志遠教授ocw](https://ocw.nthu.edu.tw/ocw/index.php?page=course&cid=141)
        2. [原文書:恐龍本](https://os.ecci.ucr.ac.cr/slides/Abraham-Silberschatz-Operating-System-Concepts-10th-2018.pdf)""")

        computer_architecture.write("""
        1. [交大黃婷婷教授ocw](https://ocw.nthu.edu.tw/ocw/index.php?page=course&cid=76)
        2. [原文書:白算盤](https://theswissbay.ch/pdf/Books/Computer%20science/Computer%20Organization%20and%20Design-%20The%20HW_SW%20Inteface%205th%20edition%20-%20David%20A.%20Patterson%20%26%20John%20L.%20Hennessy.pdf)
        3. [交大李毅郎教授ocw](https://ocw.nycu.edu.tw/?course_page=all-course%2Fcollege-of-computer-science%2F%E8%A8%88%E7%AE%97%E6%A9%9F%E7%B5%84%E7%B9%94-computer-organization-100%E5%AD%B8%E5%B9%B4%E5%BA%A6-%E8%B3%87%E8%A8%8A%E5%B7%A5%E7%A8%8B%E5%AD%B8%E7%B3%BB-%E6%9D%8E%E6%AF%85%E9%83%8E%E8%80%81)""")

        st.write('### 新增收藏')
        with st.form(key='favor_form'):
            book = st.selectbox('書籍', list(var.RESOURCE.keys()), key='book', index=0)
            submit = st.form_submit_button('新增')

            if submit:
                response = requests.post(f'http://{HOST}/favor', json={'username': st.session_state['username'], 'book': book})
                if response.status_code == 200:
                    st.success('新增成功')
                else:
                    st.error('新增失敗')