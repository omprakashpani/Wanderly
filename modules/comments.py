from modules.db import query_all, execute
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


nltk.download("punkt")
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))


def clean(text):
    if not isinstance(text, str) or len(text.strip()) == 0:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)


def get_comments(trip_id):
    rows = query_all("""
        SELECT c.id, c.comment, c.created_at, u.username
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.trip_id = %s
        ORDER BY c.created_at DESC
    """, (trip_id,))
    return rows


def add_comment(trip_id, user_id, comment):
    return execute('INSERT INTO comments (trip_id,user_id,comment) VALUES (%s,%s,%s)',
                   (trip_id, user_id, comment))


def build_model():
    
    all_comments = query_all("SELECT comment FROM comments")
    df = pd.DataFrame(all_comments)
    if df.empty or df["comment"].str.strip().eq("").all():
        
        dummy_data = {
            "comment": [
                "I loved this trip! Everything was amazing.",
                "Worst experience ever, never coming back.",
                "The trip was okay, nothing special.",
                "Great service and wonderful people!",
                "Terrible hotel, dirty rooms and bad food.",
                "Had a decent experience, could be better."
            ]
        }
        df = pd.DataFrame(dummy_data)

    df["cleaned"] = df["comment"].apply(clean)


    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(df["cleaned"])


    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(X)


    terms = vectorizer.get_feature_names_out()
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    cluster_keywords = {}
    for i in range(kmeans.n_clusters):
        keywords = [terms[ind] for ind in order_centroids[i, :5]]
        cluster_keywords[i] = keywords


    positive_words = {"good","great","wonderful","amazing","loved","love","excellent","service","happy"}
    negative_words = {"bad","terrible","worst","dirty","never","hate"}
    sentiment_map = {}
    for cluster, keywords in cluster_keywords.items():
        if any(word in positive_words for word in keywords):
            sentiment_map[cluster] = "Good"
        elif any(word in negative_words for word in keywords):
            sentiment_map[cluster] = "Bad"
        else:
            sentiment_map[cluster] = "Neutral"

    return vectorizer, kmeans, sentiment_map


vectorizer, kmeans, sentiment_map = build_model()


def classify_sentiment(comment):
    cleaned = clean(comment)
    if cleaned.strip() == "":
        return "Neutral"
    vect = vectorizer.transform([cleaned])
    cluster = kmeans.predict(vect)[0]
    sentiment = sentiment_map.get(cluster, "Neutral")
    return sentiment
