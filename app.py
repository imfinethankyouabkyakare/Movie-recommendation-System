import streamlit as st
import requests
import pandas as pd

# TMDB API setup
API_KEY = "34dfe96619ed55f0bd1a752f54f18c8b"  # Replace with your actual TMDB API key

# Fetch popular movies
@st.cache_data
def fetch_popular_movies():
    url = f"movie/popular"
    params = {"api_key": API_KEY, "language": "en-US", "page": 1}
    response = requests.get(params=params)
    if response.status_code == 200:
        results = response.json()["results"]
        return pd.DataFrame(results)
    else:
        st.error("Failed to fetch popular movies.")
        return pd.DataFrame()

# Fetch recommendations based on a movie ID
def fetch_recommendations(movie_id):
    url = f"movie/{movie_id}/recommendations"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(params=params)
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

    # Display a dropdown for movie selection
    movie_list = movies[['id', 'title']].values
    selected_movie = st.selectbox(
        "Select a movie you like:",
        movie_list,
        format_func=lambda x: x[1]  # Display only the movie title
    )

    if st.button("Recommend"):
        movie_id, movie_title = selected_movie
        recommendations = fetch_recommendations(movie_id)
        if recommendations:
            st.write(f"Recommendations based on **{movie_title}**:")
            for movie in recommendations:
                st.write(f"- {movie['title']} ({movie['release_date'][:4] if 'release_date' in movie else 'N/A'})")
        else:
            st.warning("No recommendations available for this movie.")

if __name__ == "__main__":
    main()
