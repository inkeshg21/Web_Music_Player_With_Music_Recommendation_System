import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import sqlite3

# Connect to the database
conn = sqlite3.connect('db.sqlite3')

# Read the data from the database table
query = "SELECT title, genre, description FROM music_music"
music = pd.read_sql_query(query, conn)

# Clean the data by removing any NaN values
music.dropna(inplace=True)

# Concatenate the name, artist, and genre columns into a single text column
music["text"] = music["title"] + " " + music["genre"] + " " + music["description"]

# Initialize the TF-IDF vectorizer
tfidf = TfidfVectorizer()

# Compute TF-IDF matrix
tfidf_matrix = tfidf.fit_transform(music["text"])

# Build the cosine similarity matrix
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

# Create a reverse mapping of names and indices
indices = pd.Series(music.index, index=music["title"]).drop_duplicates()

def recommend_songs(song_name, num_recommendations=5):
    # Get the index of the input song
    song_index = indices[song_name]

    # Get the similarity scores of the input song with other songs
    song_similarities = cosine_similarities[song_index]

    # Sort the similarity scores in descending order
    sorted_indices = song_similarities.argsort()[::-1]

    # Get the indices of the most similar songs
    recommended_indices = sorted_indices[1:num_recommendations+1]

    # Get the names of recommended songs
    recommended_songs = music["title"].iloc[recommended_indices]

    return recommended_songs

# Example usage:
# input_song_names = ["Je Chau Timi", "Sugar", "Dhairya"]
# for song_name in input_song_names:
#     recommendations = recommend_songs(song_name)
#     print(f"Recommendations for '{song_name}':")
#     print(recommendations)
#     print()
