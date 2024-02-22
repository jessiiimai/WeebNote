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
        st.image("images/headerwithtitle.png", use_column_width=True, width=10)
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
    # show some info text
    st.markdown('<p style="font-weight: bold; font-size: 15px;'
                '">3 reasons why you should get a Weebnote account now:</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 15px;">1. When you are feeling empty after finishing another great show, '
                'you have a place to turn to.</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 15px;">2. You can bond with friends through our "matching" system.</p>',
                unsafe_allow_html=True)
    st.markdown('<p style="font-size: 15px;">3. We are not only an ANIME GENERATOR, we are a community. </p>',
                unsafe_allow_html=True)
