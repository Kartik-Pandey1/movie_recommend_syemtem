import streamlit as st
import pandas as pd
import pickle
import requests

API_KEY = "4616c6689910ad753ec9e2e241e2f1f5"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get("poster_path")
    if poster_path:
        return IMAGE_BASE_URL + poster_path
    return None


def recommend(movie):
    # get the index of the movie
    mov_indx = movies[movies['title'] == movie].index[0]

    # get similarity scores
    dis = similarity[mov_indx]

    # sort movies by similarity (excluding the first one which is the same movie)
    mov_list = sorted(list(enumerate(dis)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movie = []
    mov_recommend_poster = []
    for i in mov_list:
        movie_id = movies.iloc[i[0]].movie_id   # ✅ use the real TMDB movie_id
        recommend_movie.append(movies.iloc[i[0]].title)
        mov_recommend_poster.append(fetch_poster(movie_id))

    return recommend_movie, mov_recommend_poster


# Load data
mov_dict = pickle.load(open("mov_dict.pkl", "rb"))
movies = pd.DataFrame(mov_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

# Streamlit UI
st.title("🎬 Movie Recommender System")
selected_movie_name = st.selectbox(
    "Which movie do you want to recommend?",
    movies['title'].values
)
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    # Create 5 columns for recommendations
    cols = st.columns(5)

    for i, col in enumerate(cols):
        with col:
            st.image(posters[i], use_container_width=True)
            st.caption(names[i])   # movie name