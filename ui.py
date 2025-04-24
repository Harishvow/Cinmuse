import streamlit as ln
import requests

ln.set_page_config(page_title="Cinemuse 🎬", layout="centered")
ln.markdown("""
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
ln.title("🎬 Cinemuse")
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

rec_type = ln.radio("Choose Recommendation Type", ["Mood", "Genre"])
if rec_type == "Mood":
    mood = ln.selectbox("How are you feeling?", ["happy", "sad", "romance", "motivated", "angry", "relaxed"])
else:
    genre = ln.selectbox("Pick a Genre", ["Action", "Comedy", "Drama", "Fantasy", "Horror", "Romance",
                                          "Adventure", "Family", "Animation", "Thriller"])

if ln.button("🎥 Recommend Movies"):
    recs = get_movies_by_mood_or_genre("Mood", mood) if rec_type == "Mood" else get_movies_by_mood_or_genre("Genre", genre)

    if recs:
        for movie in recs:
            ln.subheader(f"{movie['title']} ({movie['release_date']})")
            if movie.get("poster_path"):
                ln.image(f"https://image.tmdb.org/t/p/w200/{movie['poster_path']}", width=120)
    else:
        ln.warning("No movies found. Try another mood or genre.")




