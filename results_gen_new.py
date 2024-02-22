import requests
import json
import random
import streamlit as st

""" GENRE LIST
1 = Action
2 = Adventure
28 = Boys Love
4 = Comedy
8 = Drama 
14 = Horror
22 = Romance
"""


def generate_season(year, season):
    payload = {"filter": "tv"}   # decides what genres should be picked

    # to get a specific season
    season_url = "https://api.jikan.moe/v4/seasons/"
    date = str(year) + "/" + str(season)
    release = season_url + date

    r = requests.get(release, params=payload).text   # searches for titles that fulfill the user choice
    sex = json.loads(r)  # transforms into json

    # collects number of pages of chosen anime and randomly choose 1
    pages = (sex["pagination"]["last_visible_page"])
    rand_page = random.randint(1, pages)
    payload["page"] = rand_page
    x = requests.get(release, params=payload).text
    sex3 = json.loads(x)

    if "data" in sex3.keys():
        num = random.randint(0, len(sex3["data"])-1)
        title = sex3["data"][num]["title"]
        syn = sex3["data"][num]["synopsis"]
        img = sex3["data"][num]["images"]["webp"]["image_url"]
        url = sex3["data"][num]["trailer"]["url"]

        st.session_state.current_anime = title
        st.session_state.img = img

        st.write(title)
        st.image(img)
        st.write(syn)
        if url is None:
            st.write("No trailer available")
        else:
            st.write(f"Link to  trailer: {url}")
    else:
        st.write("Oops! Something went wrong there! Please generate again or choose other settings.")


def generate_genre(*genre_choice):
    payload = {"type": "tv", "genres": genre_choice}   # decides what genres should be picked
    anime_url = "https://api.jikan.moe/v4/anime"
    r = requests.get(anime_url, params=payload).text   # searches for titles that fulfill the user choice
    sex = json.loads(r)  # transforms into json

    # collects number of pages of chosen anime and randomly chooses 1
    pages = (sex["pagination"]["last_visible_page"])
    rand_page = random.randint(1, pages)
    payload["page"] = rand_page
    x = requests.get(anime_url, params=payload).text
    sex3 = json.loads(x)

    num = random.randint(0, 24)
    title = sex3["data"][num]["title"]
    syn = sex3["data"][num]["synopsis"]
    img = sex3["data"][num]["images"]["webp"]["image_url"]
    url = sex3["data"][num]["trailer"]["url"]

    st.session_state.current_anime = title
    st.session_state.img = img

    st.write(title)
    st.image(img)
    st.write(syn)
    if url is None:
        st.write("No trailer available")
    else:
        st.write(f"Link to  trailer: {url}")
