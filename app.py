import json

import requests
import streamlit as st
import pandas as pd
import pickle
import time
import numpy as np

st.title('Movie Recommendation App')
movies = pd.read_csv('NecessaryData/Preprocessed_Movie_Data.csv')
moviesAvailable = movies['title'].values
similarity = pickle.load(open('NecessaryData/similarities.pkl', 'rb'))

api_key = "xxxxxxxxxxxxxx"
root_path = "https://image.tmdb.org/t/p/original"


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key={api_key}&language=en-US".format(movie_id)
    # url="https://api.themoviedb.org/3/movie/19995?api_key=970bc089e3a26d22dd7a478ab38eb1ad&language=en-US"
    time.sleep(0.02)
    header = {
        "Connection": "Keep-Alive"
    }
    #header["Connection"] = "Keep-Alive"
    data = requests.get(url = url, headers=header).json()
    #data = data.json()
    # print(data)
    poster_path = data['poster_path']
    full_path = root_path + poster_path
    return full_path


# Main function for recommending movies
def recommendMovies(movieWatched):
    index = movies[movies['title'] == movieWatched].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie.append(i[0])

    return recommended_movie, recommended_movie_posters


movieWatched = st.selectbox('Select the movie that you have watched...', sorted(moviesAvailable))

if st.button("Recommend Movie"):
    data_load_state = st.text('Loading recommendations...')
    # Recommendation,url =
    movie, moviePath = recommendMovies(movieWatched)

    myColumns = st.columns(5)

    key = 0
    for i, data in enumerate(myColumns):
        with data:
            index=movie[i]
            st.subheader(movies.iloc[index].title)
            st.image(moviePath[i])
            st.write("Status : "+movies.iloc[index].status)
            st.write("Rating : "+str(movies.iloc[index].vote_average))
            st.write("Liked this recommendation?")

            st.write("Give feedback")
            st.button("Yes",key=key)
            key+=1
            st.button("No",key=key)
            key+=1

    data_load_state.text('Loading recommendations...Done!')
