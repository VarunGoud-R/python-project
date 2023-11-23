import numpy as np
import pandas as pd
from flask import Flask, request, render_template

app = Flask(__name__)
movies = pd.read_csv('movies.csv')

def getRecommendations(genre):
    try:
        recommended_movies = pd.DataFrame()
        movies['count'] = movies['genres'].apply(lambda x: sum(i in genre for i in x.split('|')))
        # print(movies['genres'].apply(lambda x: set(genre).issubset(set(x.split('|')))))
        print(movies, end = '\n\n')
        recommended_movies = movies.loc[movies['count'] > 0].sort_values(by = ['count'], ascending = False).reset_index(drop = True)
        print(recommended_movies, end = '\n\n')
        if not recommended_movies.empty:
            recommended_titles = recommended_movies['title'].tolist()
            print(recommended_titles)
            return recommended_titles
        else:
            return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods = ['POST'])
def recommend():
    features = [str(x) for x in request.form.values()]
    print(features, end = '\n\n')
    result = getRecommendations(features)
    return render_template('recommendation.html', recommended_movies = result)

if __name__ == "__main__":
    app.run(debug=True)
