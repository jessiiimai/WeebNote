import streamlit as st
from results_gen_new import generate_season, generate_genre


def seasons_tab():
    # create the tab with the header and sliders etc.
    st.subheader("| Seasons")
    year = st.slider("Select a year", min_value=1965, max_value=2023)
    season = st.selectbox('What season are you interested in?', ('Spring', 'Summer', 'Fall', 'Winter'))
    st.write("You selected:", season, year)

    # click the button and generate a random anime
    if st.button("Generate"):
        generate_season(year, season)


def genre_tab(genres, genre_choice):
    # create a select widget for the genres
    options = st.multiselect('Pick your genres', ['Action', 'Adventure', 'Comedy', 'Drama', "Romance"])

    # this is for excluding genres
    genre_ex = st.checkbox("Exclude some genres")
    if genre_ex:
        options_ex = st.multiselect('What genres do you want to exclude', ['Action', 'Adventure', 'Comedy', 'Drama', "Romance"])

        if options_ex:  # mapping number keys to options
            for n, g in enumerate(options_ex):
                # replace the green, yellow etc. with anime categories and corresponding
                if options_ex[n] == "Action":
                    options_ex[n] = "1"
                if options_ex[n] == "Adventure":
                    options_ex[n] = "2"
                if options_ex[n] == "Comedy":
                    options_ex[n] = "4"
                if options_ex[n] == "Drama":
                    options_ex[n] = "8"
                if options_ex[n] == "Horror":
                    options_ex[n] = "14"
                if options_ex[n] == "Romance":
                    options_ex[n] = "22"

    if options:  # mapping number keys to options
        for n, g in enumerate(options):
            # replace the green, yellow etc. with anime categories and corresponding
            if options[n] == "Action":
                options[n] = "1"
            if options[n] == "Adventure":
                options[n] = "2"
            if options[n] == "Comedy":
                options[n] = "4"
            if options[n] == "Drama":
                options[n] = "8"
            if options[n] == "Horror":
                options[n] = "14"
            if options[n] == "Romance":
                options[n] = "22"

    genre_choice = tuple(options)

    if genre_ex and options_ex:
        genre_choice = tuple(set(options) - set(options_ex))

    # click the button and get a random anime
    if st.button("Get results", disabled=not genre_choice):
        generate_genre(*genre_choice)


