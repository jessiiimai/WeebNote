import requests
import json
import random
import streamlit as st

def generate_season(year, season):
    payload = {"filter": "tv"}

    # to get a specific season
    season_url = "https://api.jikan.moe/v4/seasons/"
    date = str(year) + "/" + str(season)
    release = season_url + date

    # searches for titles that fulfill the user choice and transforms them into json
    r = requests.get(release, params=payload).text
    form1 = json.loads(r)

    # collects number of pages of chosen anime and randomly chooses 1
    pages = (form1["pagination"]["last_visible_page"]- 1)
    rand_page = random.randint(1, pages)
    payload["page"] = rand_page
    x = requests.get(release, params=payload).text
    form2 = json.loads(x)

    if "data" in form2.keys():
        num = random.randint(0, len(form2["data"]))
        title = form2["data"][num]["title"]
        syn = form2["data"][num]["synopsis"]
        img = form2["data"][num]["images"]["webp"]["image_url"]
        url = form2["data"][num]["trailer"]["url"]

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
        st.write("With your settings, there was no title available. Please choose other settings!")


# repeats previous functions but using "genre" filters
def generate_genre(*genre_choice):
    payload = {"type": "tv", "genres": genre_choice}
    anime_url = "https://api.jikan.moe/v4/anime"
    r = requests.get(anime_url, params=payload).text
    form = json.loads(r)


    pages = (form["pagination"]["last_visible_page"] - 1)
    rand_page = random.randint(1, pages)
    payload["page"] = rand_page
    x = requests.get(anime_url, params=payload).text
    form3 = json.loads(x)

    num = random.randint(0, 24)
    title = form3["data"][num]["title"]
    syn = form3["data"][num]["synopsis"]
    img = form3["data"][num]["images"]["webp"]["image_url"]
    url = form3["data"][num]["trailer"]["url"]

    current_anime = [title]
    st.session_state.current_anime = str(current_anime)
    current_anime_img = [img]
    st.session_state.img = str(current_anime_img)

    st.write(title)
    st.image(img)
    st.write(syn)
    if url is None:
        st.write("No trailer available")
    else:
        st.write(f"Link to  trailer: {url}")
