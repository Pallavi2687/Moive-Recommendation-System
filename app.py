import pickle
import streamlit as st
import requests
import os
import requests

def fetch_poster(movie_id):
    local_path = f"posters/{movie_id}.jpg"
    
    # If poster is already downloaded locally
    if os.path.exists(local_path):
        return local_path
    
    # Try to fetch from TMDB (when VPN is on)
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=5).json()
        poster_path = response.get('poster_path')
        
        if poster_path:
            full_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            img_data = requests.get(full_url).content
            
            # Save locally for future use
            os.makedirs("posters", exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(img_data)
                
            return local_path
    except:
        pass

    # Fallback: show "poster not available"
    return None


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommendation System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
      st.text(recommended_movie_names[0])
      if recommended_movie_posters[0]:
        st.image(recommended_movie_posters[0])
      else:
        st.write("📌 Poster not available")

    with col2:
      st.text(recommended_movie_names[1])
      if recommended_movie_posters[1]:
        st.image(recommended_movie_posters[1])
      else:
        st.write("📌 Poster not available")

    with col3:
        st.text(recommended_movie_names[2])
        if recommended_movie_posters[2]:
          st.image(recommended_movie_posters[2])
        else:
           st.write("📌 Poster not available")

    with col4:
     st.text(recommended_movie_names[3])
     if recommended_movie_posters[3]:
        st.image(recommended_movie_posters[3])
     else:
        st.write("📌 Poster not available")

    with col5:
     st.text(recommended_movie_names[4])
     if recommended_movie_posters[4]:
        st.image(recommended_movie_posters[4])
     else:
        st.write("📌 Poster not available")





