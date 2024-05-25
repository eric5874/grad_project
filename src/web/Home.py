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
    st.title('Home')
    st.write('Welcome to the home page!')