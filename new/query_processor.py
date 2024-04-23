from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import numpy as np

def create_tfidf_index(documents):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    return tfidf_matrix, vectorizer

def save_index(tfidf_matrix, vectorizer, filename="tfidf_model.pkl"):
    with open(filename, 'wb') as f:
        pickle.dump((tfidf_matrix, vectorizer), f)

def load_index(filename="tfidf_model.pkl"):
    with open(filename, 'rb') as f:
        tfidf_matrix, vectorizer = pickle.load(f)
    return tfidf_matrix, vectorizer

def search_documents(query, vectorizer, tfidf_matrix):
    query_tfidf = vectorizer.transform([query])
    cosine_similarities = cosine_similarity(query_tfidf, tfidf_matrix).flatten()
    sorted_doc_indices = np.argsort(-cosine_similarities)
    return sorted_doc_indices, cosine_similarities