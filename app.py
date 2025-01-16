import streamlit as st
import requests
import pandas as pd

# TMDB API setup
API_KEY = "34dfe96619ed55f0bd1a752f54f18c8b"  # Replace with your actual TMDB API key
BASE_URL = "https://api.themoviedb.org/3"

# Fetch popular movies
@st.cache_data
def fetch_popular_movies():
    url = f"{BASE_URL}/movie/popular"
    params = {"api_key": API_KEY, "language": "en-US", "page": 1}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json()["results"]
        return pd.DataFrame(results)
    else:
        st.error("Failed to fetch popular movies.")
        return pd.DataFrame()

# Fetch recommendations based on a movie ID
def fetch_recommendations(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/recommendations"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json()["results"]
        return results
    else:
        st.error("Failed to fetch recommendations.")
        return []

# Main Streamlit app
def main():
    st.title("TMDB Movie Recommendation System")
    st.write("Get movie recommendations using the TMDB API.")

    # Fetch popular movies
    movies = fetch_popular_movies()
    if movies.empty:
        st.warning("No movies available. Please check the API connection.")
        return

    # Display a 
