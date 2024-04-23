import pytest
from sklearn.feature_extraction.text import TfidfVectorizer
from html_parser import *
import numpy as np
import os
# Test documents
documents = [
    "Hello world",
    "Hello there",
    "Hi there"
]

# Expected outputs and setups
vectorizer = TfidfVectorizer(stop_words='english')
expected_tfidf_matrix = vectorizer.fit_transform(documents)

@pytest.fixture
def setup_index():
    tfidf_matrix, vectorizer = create_tfidf_index(documents)
    save_index(tfidf_matrix, vectorizer)
    yield tfidf_matrix, vectorizer
    # Cleanup
    if os.path.exists("tfidf_model.pkl"):
        os.remove("tfidf_model.pkl")

def test_create_tfidf_index():
    tfidf_matrix, vectorizer = create_tfidf_index(documents)
    assert tfidf_matrix.shape == (3, 3)  # 3 documents and 3 terms
    assert isinstance(vectorizer, TfidfVectorizer)

def test_save_and_load_index(setup_index):
    tfidf_matrix, vectorizer = setup_index
    loaded_tfidf_matrix, loaded_vectorizer = load_index()
    
    # Compare the original and loaded vectorizer settings
    assert vectorizer.get_params() == loaded_vectorizer.get_params()
    
    # Compare matrices
    assert np.array_equal(tfidf_matrix.toarray(), loaded_tfidf_matrix.toarray())

def test_search_documents(setup_index):
    tfidf_matrix, vectorizer = setup_index
    query = "hello"
    indices, similarities = search_documents(query, vectorizer, tfidf_matrix)
    
    assert len(indices) == len(documents)  # Should return an index for each document
    assert similarities[indices[0]] >= similarities[indices[1]]  # Ensure ordering by similarity

    # Check specific behavior (first document should be most similar)
    assert indices[0] == 0  # "Hello world" should be most similar to "hello"
