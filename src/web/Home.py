import streamlit as st

# Create login page
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title('Login')

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        # Perform login validation here
        if username == 'admin' and password == 'admin':
            st.session_state['logged_in'] = True
            st.success('Logged in successfully!')
            st.rerun()
        else:
            st.error('Invalid username or password')

else:
    st.title('資工所資源網站')
    col1, col2 = st.columns([1, 4])

    with col1:
        st.write('### 目錄')
        st.write('1. [首頁](/)')
        st.write('2. [資源](/resources)')
        st.write('3. [關於](/about)')

    with col2:
        st.write('### 歡迎來到資工所資源網站')
        st.write('這是一個為資工所學生設計的資源網站')
        st.write('你可以在這裡找到許多資源，例如：')
        st.write('- 課程筆記')
        st.write('- 考古題')
        st.write('- 程式範例')
        st.write('- 等等')