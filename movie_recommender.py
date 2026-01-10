import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load dataset
df = pd.read_csv('movies.csv')

# Step 2: Convert genres text into numbers
vectorizer = CountVectorizer()
genre_matrix = vectorizer.fit_transform(df['genres'])

# Step 3: Create similarity matrix
similarity = cosine_similarity(genre_matrix)

def recommend(movie_name):
    if movie_name not in df['title'].values:
        return "Movie not found!"
    
    # Find index of movie
    index = df[df['title'] == movie_name].index[0]
    
    # Get similarity scores for that movie
    scores = list(enumerate(similarity[index]))
    
    # Sort based on similarity
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    
    # Print top 5 recommendations (skip itself)
    print(f"\nMovies similar to '{movie_name}':")
    for i in sorted_scores[1:6]:
        print("-", df.iloc[i[0]]['title'])

# Test
recommend("Avatar")
recommend("The Notebook")
