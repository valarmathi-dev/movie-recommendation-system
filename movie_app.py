from flask import Flask, request, render_template_string
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Dataset
data = {
    'title': ['Avatar', 'Titanic', 'The Avengers', 'Jurassic Park', 'The Notebook',
              'Twilight', 'Iron Man', 'Spider-Man', 'Fast & Furious', 'Frozen'],
    'genre': ['Action Fantasy', 'Romance Drama', 'Action Adventure', 'Sci-Fi Adventure',
              'Romance Drama', 'Romance Fantasy', 'Action Sci-Fi', 'Action Adventure',
              'Action Thriller', 'Animation Family']
}
df = pd.DataFrame(data)

# Vectorize genre features
cv = CountVectorizer()
count_matrix = cv.fit_transform(df['genre'])
similarity = cosine_similarity(count_matrix)

# Recommendation function
def recommend(movie):
    movie = movie.title()
    if movie not in df['title'].values:
        return ["Movie not found!"]

    index = df[df['title'] == movie].index[0]
    distances = list(enumerate(similarity[index]))
    movies_list = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]
    return [df.iloc[i[0]]['title'] for i in movies_list]

# Flask app
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Movie Recommender</title>
</head>
<body style="font-family: Arial; margin: 50px;">
    <h2>🎬 Movie Recommendation System</h2>
    <form action="/" method="POST">
        <input type="text" name="movie" placeholder="Enter movie name">
        <button type="submit">Recommend</button>
    </form>

    {% if movie %}
        <h3>Recommendations for '{{ movie }}'</h3>
        <ul>
        {% for m in recs %}
            <li>{{ m }}</li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    movie = None
    recs = []
    if request.method == "POST":
        movie = request.form.get("movie")
        recs = recommend(movie)
    return render_template_string(HTML, movie=movie, recs=recs)

if __name__ == "__main__":
    app.run(debug=True)
