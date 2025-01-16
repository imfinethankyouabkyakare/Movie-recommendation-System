import streamlit as st
import requests

# TMDB API Key
API_KEY = "34dfe96619ed55f0bd1a752f54f18c8b"  # Replace with your TMDB API key

# Fetch popular movies
def fetch_popular_movies():
    url = f"https://api.themoviedb.org/3/movie/popular"
    params = {"api_key": API_KEY, "language": "en-US", "page": 1}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["results"]
    else:
        st.error(f"Failed to fetch popular movies: {response.status_code}")
        return []

# Fetch recommendations based on a movie ID
def fetch_recommendations(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["results"]
    else:
        st.error(f"Failed to fetch recommendations: {response.status_code}")
        return []

# Main Streamlit app
def main():
    st.title("Bkins Movie Recommendation System")
    st.write("Get movie recommendations.")

    # Fetch popular movies
    popular_movies = fetch_popular_movies()
    if not popular_movies:
        st.warning("No popular movies available. Please check the API connection.")
        return

    # Create a dropdown menu for movie selection
    movie_options = [(movie["id"], movie["title"]) for movie in popular_movies]
    selected_movie = st.selectbox(
        "Select a movie you like:", movie_options, format_func=lambda x: x[1]
    )

    if st.button("Recommend"):
        movie_id, movie_title = selected_movie
        recommendations = fetch_recommendations(movie_id)

        if recommendations:
            st.write(f"Recommendations based on **{movie_title}**:")
            for movie in recommendations:
                release_date = movie.get("release_date", "N/A")
                st.write(f"- **{movie['title']}** (Release Date: {release_date})")
        else:
            st.warning("No recommendations available for this movie.")

if __name__ == "__main__":
    main()
