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