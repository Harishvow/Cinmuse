import streamlit as st
import requests

st.set_page_config(page_title="Cinemuse 🎬", layout="centered")
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1b1b2f, #162447, #1f4068);
        color: white;
    }
    .stButton > button {
        background-color: #e43f5a;
        color: white;
        border-radius: 10px;
        font-weight: bold;
    }
    .stSelectbox label, .stRadio label, h1, h2, h3 {
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)
st.title("🎬 Cinemuse")
API_KEY = "e18784041d39dc57252ad007f1e02d4d"
mood_genre_map = {
    "happy": [35, 10751],
    "sad": [18, 10749],
    "romance": [10749],
    "motivated": [12, 28],
    "angry": [27, 53],
    "relaxed": [10751, 16]
}
def get_movies_by_mood_or_genre(selected_option, selection):
    if selected_option == "Mood":
        genres = mood_genre_map.get(selection.lower(), [])
    else:
        genre_map = {
            "Action": 28, "Comedy": 35, "Drama": 18, "Fantasy": 14,
            "Horror": 27, "Romance": 10749, "Adventure": 12, "Family": 10751,
            "Animation": 16, "Thriller": 53
        }
        genres = [genre_map.get(selection)]

    movies = []
    for genre_id in genres:
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={genre_id}&sort_by=popularity.desc"
        res = requests.get(url).json()
        movies.extend(res.get("results", [])[:5])
    return movies
rec_type = st.radio("Choose Recommendation Type", ["Mood", "Genre"])
if rec_type == "Mood":
    mood = st.selectbox("How are you feeling?", ["happy", "sad", "romance", "motivated", "angry", "relaxed"])
else:
    genre = st.selectbox("Pick a Genre", ["Action", "Comedy", "Drama", "Fantasy", "Horror", "Romance",
                                          "Adventure", "Family", "Animation", "Thriller"])

if st.button("🎥 Recommend Movies"):
    recs = get_movies_by_mood_or_genre("Mood", mood) if rec_type == "Mood" else get_movies_by_mood_or_genre("Genre", genre)

    if recs:
        for movie in recs:
            st.subheader(f"{movie['title']} ({movie['release_date']})")
            if movie.get("poster_path"):
                st.image(f"https://image.tmdb.org/t/p/w200/{movie['poster_path']}", width=120)
    else:
        st.warning("No movies found. Try another mood or genre.")



