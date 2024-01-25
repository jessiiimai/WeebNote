import streamlit as st
from weebnote_application import open_app
from helpers import connect_to_deta, fetch_data

st.set_page_config(page_title="WeebNote")
# so we can save login information in session state later
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# create a deta db for login info to store and work with the data
base_name = "userinfo_weebnote"
db = connect_to_deta(base_name)


# create the login form
def login_form():
    with st.form("Login"):
        st.markdown("Welcome! Please enter your login info.")
        username = st.text_input("Username", placeholder="Please enter your user name").lower()
        password = st.text_input("Password", placeholder="Please enter your password", type="password")
        login_button = st.form_submit_button("Login")

        # fetch the user data to carry out validations
        user_data = fetch_data(db)  # fetching all the data I have stored on my user
        user_names = list(user_data.username)  # identifying a list of all the existing users

        # logging into the app if the username is already existing in deta
        if login_button:
            if username in user_names:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.rerun()
            else:
                st.error("The username is not correct.")
    return username


# when you are logged in, the app opens
if st.session_state.logged_in:
    open_app()
else:
    login_form()
