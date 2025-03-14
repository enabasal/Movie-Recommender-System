import pickle
import pandas as pd
import streamlit as st
import requests


# Function to fetch poster URL from the TMDB API
def fetch_poster(movie_title):
    api_key = "5b095f47"  # Replace with your actual TMDb API key
    url = f"https://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        data = response.json()

        return data.get("Poster", "https://via.placeholder.com/500x750?text=No+Image")

    except requests.exceptions.RequestException as e:
     st.error(f"Error fetching poster: {e}")
    return "https://via.placeholder.com/500x750?text=No+Image"


# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    movie_titles = []
    movie_posters = []
    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        movie_posters.append(fetch_poster(movie_title))
        movie_titles.append(movie_title)
    return movie_titles, movie_posters


# Streamlit UI
st.header('Movie Recommender System')

# Load necessary pickle files
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Dropdown menu for selecting a movie
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Show recommendations when button is clicked
if st.button('Show Recommendation'):
    movie_titles, movie_posters = recommend(selected_movie)

    cols = st.columns(5)  # Create 5 columns dynamically
    for col, movie_title, poster in zip(cols, movie_titles, movie_posters):
        with col:
            st.image(poster, caption=movie_title, use_column_width=True)