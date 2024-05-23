import streamlit as st

# Initialize Streamlit session
session_state = st.session_state

# Create login page
if 'logged_in' not in session_state:
    session_state['logged_in'] = False

if not session_state['logged_in']:
    st.title('Login')

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        # Perform login validation here
        if username == 'admin' and password == 'admin':
            session_state['logged_in'] = True
            st.success('Logged in successfully!')
        else:
            st.error('Invalid username or password')

else:
    st.title('Home')
    st.write('Welcome to the home page!')