import streamlit as st
from helpers import connect_to_deta, fetch_data
from filter_sliders_new import seasons_tab, genre_tab

# create a new database for the anime stored together with the username
base_name = "user_animelist"
db = connect_to_deta(base_name)
# if db is empty and does not work: db.insert({"user": "", "anime_title": "", "image": ""})


# show anime list in anime list tab
def show_mylist():
    # not sure if we still need this part
    if "current_anime" in st.session_state:
        del st.session_state["current_anime"]

    # fetch all the stored anime in the db
    fetch_animelist = fetch_data(db)
    if "anime_title" in fetch_animelist.columns:
        # make a list of images corresponding to the user
        imagelist = list(fetch_animelist[fetch_animelist.user == st.session_state.current_user].image)

        st.subheader("These are your chosen anime:")
        # order the pictures in the column
        col_left, col_right = st.columns(2)
        # every second image has its own for loop so that the images are in 2 different columns
        left_images = imagelist[0::2]  # column left
        right_images = imagelist[1::2]  # column right
        for i in left_images:
            st.session_state.current_image = i
            # get a list for the titles corresponding to the images corresponding to the current user
            title_imagelist = list(fetch_animelist[fetch_animelist.image == st.session_state.current_image][fetch_animelist.user == st.session_state.current_user].anime_title)
            with col_left:
                st.image(i, caption=title_imagelist, width=300)  # width so that the pictures are the same size
        for r in right_images:
            st.session_state.current_image = r
            title_imagelist = list(fetch_animelist[fetch_animelist.image == st.session_state.current_image][fetch_animelist.user == st.session_state.current_user].anime_title)
            with col_right:
                st.image(r, caption=title_imagelist, width=300)
                # experiment with clicking images: click_image(y, title_imagelist)


# show matches with friends
def match_friends():
    # not sure if we still need this part
    # if "chosen_anime" in st.session_state:
    # del st.session_state["chosen_anime"]

    # input and button
    friend = st.text_input("Type in a friend's name!")
    friend_request = st.button("Try to get a match!")

    # click on button
    if friend_request:
        # fetch a list of all the usernames
        data = fetch_data(db)
        user_names = list(data.user)
        # if you type in your own name
        if friend == st.session_state.current_user:
            st.write("Isn't that you? Where are your friends?")
            quit()
        # if you type in a username that exists in the database
        if friend in user_names:
            # fetches two anime lists, one for you and one for your friend
            animelist_currentuser = list(data[data.user == st.session_state.current_user].anime_title)
            animelist_friend = list(data[data.user == friend].anime_title)

            # stores all corresponding matches in one lists
            matches = list(set(animelist_friend) & set(animelist_currentuser))
            # checks if there is something stored in the list
            if len(matches) == 0:
                st.write("OH NO NO MATCHES oH nO OH NO OH NOOOOOOO")  # we need to change this
            else:
                st.write("You have matched for these anime:")
                # this code shows the anime in bullet points
                code = []
                font_colour = "#9c9d9f"
                font_size = "20"
                for i in matches:
                    code.append(f'<li style="font-size: {font_size}px; color:{font_colour}" align="justify">{i}</li>')
                complete_code = "".join(code)
                st.write(f'<ul>{complete_code}</ul>', unsafe_allow_html=True)
        # if you type in a username that does not exist in the db
        else:
            st.write("This friend does not exist unfortunately.")


# definition to launch the app after login
def open_app():
    # not sure if we still need this
    # if "chosen_anime" in st.session_state:
    # del st.session_state["chosen_anime"]
    menu = ["Welcome Page", "Generate Anime", "My Anime", "My Friends", "Logout"]
    choice = st.sidebar.radio("Menu", menu)

    if choice == "Welcome Page":
        # not sure if we still need this code
        if "chosen_anime" in st.session_state:
            del st.session_state["chosen_anime"]
        # create a header with the capitalized current username
        st.header(f"Welcome, {st.session_state.current_user.capitalize()}!")
    elif choice == "Generate Anime":
        # variables from filter sliders
        genres = ()
        genre_choice = ()
        tab1, tab2 = st.tabs(["Seasons", "Genre"])
        with tab1:
            seasons_tab()  # creates the seasons filters
            if "current_anime" in st.session_state:  # if an anime got generated, create a button
                add_to_animelist = st.button("Add to your Watching List!", key=2)
                if add_to_animelist:  # click on button, anime gets added to database
                    current_user = st.session_state.current_user
                    db.insert({"user": current_user, "anime_title": st.session_state.current_anime,
                               "image": st.session_state.img})
                    del st.session_state["current_anime"]
                    st.rerun()  # everything disappears again
        with tab2:
            genre_tab(genres, genre_choice)  # creates the genre filters
            if "current_anime" in st.session_state:  # if an anime got generated, create a button
                add_to_animelist = st.button("Add to your Watching List!", key=1)  # different key for each button
                if add_to_animelist:  # anime gets added to database
                    current_user = st.session_state.current_user
                    db.insert({"user": current_user, "anime_title": st.session_state.current_anime, "image": st.session_state.img})
                    del st.session_state["current_anime"]
                    st.rerun()  # everything disappears
    elif choice == "My Anime":
        st.header("My Anime List!")
        show_mylist()
    elif choice == "My Friends":
        st.header("My Friends")
        match_friends()
    elif choice == "Logout":
        # not sure if we still need this
        if "current_anime" in st.session_state:
            del st.session_state["current_anime"]
        logout = st.button("Logout")
        if logout:  # change all the settings to how they were in the beginning
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.chosen_anime = None
            st.rerun()


