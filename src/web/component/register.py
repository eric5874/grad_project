import streamlit as st
import requests
import os

HOST = os.getenv('HOST', 'http://localhost:8000')

def Register():
    st.title('Register')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')
    if st.button('Register'):
        if password != confirm_password:
            st.error('Passwords do not match')
        else:
            response = requests.post(f'{HOST}/register', json={'username': username, 'password': password})
            if response.status_code == 200:
                st.success('Registered successfully!')
            else:
                st.error('Username already exists')