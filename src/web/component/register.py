'''
Author: hibana2077 hibana2077@gmail.com
Date: 2024-06-26 09:51:31
LastEditors: hibana2077 hibana2077@gmail.com
LastEditTime: 2024-06-27 10:29:47
FilePath: \grad_project\src\web\component\register.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import streamlit as st
import requests
import os

HOST = os.getenv('HOST', 'http://localhost:8000')

def Register():
    st.title('Register')
    with st.form(key='register_form'):
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        confirm_password = st.text_input('Confirm Password', type='password')
        
        if st.form_submit_button('Register'):
            if password != confirm_password:
                st.error('Passwords do not match')
            else:
                response = requests.post(f'{HOST}/register', json={'username': username, 'password': password})
                if response.status_code == 200:
                    st.success('Registered successfully!')
                else:
                    st.error('Username already exists')