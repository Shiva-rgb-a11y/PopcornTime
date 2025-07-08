import streamlit as st
import pickle
import pandas as pd
import requests

# ⬅️ Apply custom CSS for background and style
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #0f2027, #203a43, #2c5364);
        color: white;
    }
    .movie-title {
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        color: #FFD700;
        margin-bottom: 10px;
    }
    img {
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(255, 255, 255, 0.2);
        transition: transform 0.2s;
    }
    img:hover {
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# ✅ Function to fetch movie poster and TMDb URL
def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=82db3aea2888fba62260302b98755f36&language=en-US'
        response = requests.get(url, timeout=10)
        data = response.json()

        poster_path = data.get('poster_path')
        tmdb_url = f'https://www.themoviedb.org/movie/{movie_id}'
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path, tmdb_url
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster", tmdb_url

    except Exception as e:
        print(f"[ERROR] fetch_poster failed for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/300x450?text=Error", "#"

# ✅ Recommendation logic
def recommended(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    tmdb_links = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        movie_title = movies.iloc[i[0]].title

        poster_url, tmdb_url = fetch_poster(movie_id)

        recommended_movies.append(movie_title)
        recommended_movies_posters.append(poster_url)
        tmdb_links.append(tmdb_url)

    return recommended_movies, recommended_movies_posters, tmdb_links

# ✅ Load model & data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# ✅ UI Header
st.markdown("<h1 style='text-align: center; color: gold;'>🎬 Movie Recommendation System 🍿</h1>", unsafe_allow_html=True)
st.markdown("---")

# ✅ Movie selector
select_movie_name = st.selectbox(
    'Choose a movie you like 🎥',
    movies['title'].values
)

if st.button('🔍 Recommend Movies'):
    names, posters, links = recommended(select_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]

    for i in range(5):
        with columns[i]:
            st.markdown(f"### 🎬 {names[i]}")
            st.image(posters[i])
            st.markdown(f"[🔗 View on TMDb]({links[i]})")


# ✅ Show user's selected movie at bottom
st.markdown(f"<p style='text-align:center; margin-top:40px;'>You selected: <b>{select_movie_name}</b></p>", unsafe_allow_html=True)
