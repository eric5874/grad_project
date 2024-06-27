import streamlit as st

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.warning('You need to login to access this page')
else:
    st.title('蒐藏')
    st.write('Welcome to the favor page!')