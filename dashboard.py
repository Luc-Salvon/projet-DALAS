import numpy as np
import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

app = Dash(__name__)

df = pd.read_csv("Donnees/cleaned_data.csv")

description_colonnes = {
        "hltb_id":           "Un identifiant unique pour chaque jeu sur HowLongToBeat.",
        "title":             "Le titre du jeu.",
        "rating":            "La note globale du jeu donnée par les utilisateurs de HowLongToBeat.",
        "retirement":        "Le taux de joueurs ayant abandonné le jeu.",
        "platform":          "La ou les plateformes sur lesquelles le jeu est disponible (PC, PS4, Xbox, etc).",
        "genre":             "Le genre du jeu (Action, Aventure, RPG, etc) d'après la plateforme HowLongToBeat.",
        "date":              "La date de sortie du jeu.",
        "time":              "Le temps de jeu moyen pour terminer le jeu.",
        "price":             "Le prix du jeu sur Steam.",
        "memoire_vive":      "La quantité de mémoire vive recommandée pour jouer au jeu.",
        "espace_disque":     "L'espace disque requis pour installer le jeu.",
        "pourcentage_pos":   "Le pourcentage de critiques positives sur Steam.",
        "review_count":      "Le nombre total de critiques sur Steam.",
        "rating_value":      "La note donnée au jeu par les utilisateurs de Steam.",
        "description":       "Une brève description du jeu.",
        "twenty_four_hours": "Le nombre de joueurs ayant joué au jeu au cours des dernières 24 heures sur Steam.",
        "all_time":          "Le nombre de joueurs actifs depuis la sortie du jeu sur Steam.",
        "steam_id":          "Un identifiant unique pour chaque jeu sur Steam.",
        "steam_tags":        "Les tags associés au jeu sur Steam (Multijoueur, RPG, Indépendant, etc).",
        "steam_genres":      "Les genres associés au jeu sur Steam (similaires à la colonne 'genre' mais spécifiques à Steam).",
        "players_by_time":   "Le nombre de joueurs en fonction des mois."
}

all_genres = df["genres"].str.replace("[", "").str.replace("]", "").str.replace("'", "").str.split(", ").explode().value_counts().index


# Combinaison des colonnes de texte pertinentes pour la similarité (titre, description, genres)
df['combined_features'] = df['title'] + " " + df['description'] + " " + df['genres']
df = df.dropna()

# Vectorisation des textes
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['combined_features'])

# Standardisation des colonnes numériques (rating, price, etc.)
numerical_features = ['rating', 'price', 'pourcentage_pos', 'review_count', 'rating_value']
scaler = StandardScaler()
scaled_numerical = scaler.fit_transform(df[numerical_features])

# Concatenation des matrices de texte et des caractéristiques numériques
features_matrix = np.hstack((tfidf_matrix.toarray(), scaled_numerical))

# Calcul de la similarité cosinus
similarity_matrix = cosine_similarity(features_matrix)


def recommend_games(liked_games, df, similarity_matrix, top_n=10):
    # Trouver les indices des jeux aimés
    liked_indices = []
    for game in liked_games:
        liked_indices.append(int(np.where(df['title']==game)[0]))

    # Calculer la similarité moyenne pour les jeux aimés
    mean_similarity = np.mean(similarity_matrix[liked_indices], axis=0)

    # Trouver les indices des jeux les plus similaires, en excluant les jeux déjà aimés
    similar_indices = mean_similarity.argsort()[::-1]
    similar_indices = [i for i in similar_indices if df.iloc[i]['title'] not in liked_games]

    # Retourner les titres des jeux recommandés
    recommended_games = df.iloc[similar_indices[:top_n]]['title'].values
    return recommended_games

@app.callback(
        Output("scatter-plot", "figure"),
        [Input("scatter-plot-x", "value"),
         Input("scatter-plot-y", "value")]
)
def update_scatter_plot(x, y):
    # Get rid of outliers
    dfbis = df[df[x] < df[x].quantile(0.95)]
    dfbis = dfbis[dfbis[y] < dfbis[y].quantile(0.95)]

    return px.scatter(dfbis, x=x, y=y)


@app.callback(
        Output("description", "children"),
        [Input("description-dropdown", "value")]
)
def update_description(value):
    return description_colonnes[value]


@app.callback(
        Output("histogram-plot", "figure"),
        [Input("histogram", "value")]
)
def update_histogram(value):
    return px.histogram(df, x=value)

@app.callback(
        Output("game-recommendations", "children"),
        [Input("game-select", "value")]
)
def update_game_recommendations(selected_games):
    if not selected_games:
        return ["Sélectionnez des jeux pour obtenir des recommandations"]

    else:
        recommended_games = recommend_games(selected_games, df, similarity_matrix, top_n=10)

    return [html.Li(game) for game in recommended_games]


# Change layout : put description and histogram on the left, scatter plot on the right

app.layout = html.Div([
        html.H1("Dashboard - How Long to Beat & Steam"),
        html.Div([
                html.Div([
                        html.H2("Description des attributs"),
                        html.Label("Choisir l'attubut dont vous voulez la description"),
                        dcc.Dropdown(
                                id="description-dropdown",
                                options=[{"label": i, "value": i} for i in df.columns],
                                value="rating"
                        ),
                        html.P(id="description"),
                        html.H2("Répartition d'un attribut"),
                        html.P("Choisissez un attribut pour voir sa répartition"),
                        dcc.Dropdown(
                                id="histogram",
                                options=[{"label": i, "value": i} for i in ["rating", "price", "time", "review_count", "twenty_four_hours", "all_time"]],
                                value="rating"
                        ),
                        dcc.Graph(id="histogram-plot")
                ], style={"float": "left", "width": "49%"}),
                html.Div([
                        html.H2("Comparaison des données"),
                        html.P("Sélectionnez deux attributs, visualisez l'un par rapport à l'autre"),
                        html.Label("Donnée en abscisse"),
                        dcc.Dropdown(
                                id="scatter-plot-x",
                                options=[{"label": i, "value": i} for i in ["rating", "price", "time", "review_count", "twenty_four_hours", "all_time"]],
                                value="rating"
                        ),
                        html.Label("Donnée en ordonnée"),
                        dcc.Dropdown(
                                id="scatter-plot-y",
                                options=[{"label": i, "value": i} for i in ["rating", "price", "time", "review_count", "twenty_four_hours", "all_time"]],
                                value="price"
                        ),
                        dcc.Graph(id="scatter-plot")
                ], style={"float": "right", "width": "49%"})
        ]),
        html.Div([
                html.H2("Recommandation de jeux"),
                html.P("Sélectionnez des jeux que vous aimez parmi cette sélection aléatoire"),
                dcc.Checklist(
                        id="game-select",
                        options=[{"label": i, "value": i} for i in df["title"].sample(30)],
                        value=[],
                        inline=True
                ),
                html.P("Vos recommandations :"),
                html.Ul(id="game-recommendations")
        ], style={"clear": "both"})
])

if __name__ == "__main__":
    app.run(debug=True)
