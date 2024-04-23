from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import math
import nltk
from collections import defaultdict

def tokenize(documents):
    tfidf_index = defaultdict(list)
# Assuming tfidf_index is your TF-IDF index from the State of the Union corpus
    idf_scores = {}
    nltk.download('punkt')
    nltk.download('stopwords')
    # Load the State of the Union corpus
    #documents = state_union.fileids()
    # Initialize preprocessing tools
    stop_words = set(stopwords.words('english'))
    tokenized_docs = defaultdict(list)
    term_doc_frequency = defaultdict(int)
    # Tokenize and preprocess the documents
    for doc_id, doc in enumerate(documents):
        tokens = [word.lower() for word in word_tokenize(doc) if word.isalnum()]
        filtered_tokens = [token for token in tokens if token not in stop_words]
        unique_tokens = set(filtered_tokens)
        for token in unique_tokens:
            tokenized_docs[token].append((doc_id, filtered_tokens.count(token)))
            term_doc_frequency[token] += 1
    # Calculate IDF scores
    total_docs = len(documents)
    print("total docs", total_docs)
    print("term doc freq", term_doc_frequency['academics'])
    idf_scores = {term: math.log(1+ total_docs / (term_doc_frequency[term] +1)) for term in term_doc_frequency}
    print("value in term doc freq",term_doc_frequency['academics'])
    print("idf socre ares", idf_scores['academics'])
    # Calculate TF-IDF scores and build the inverted index
    for term, docs in tokenized_docs.items():
        for doc_id, term_freq in docs:
            tfidf_score = term_freq * idf_scores[term]
            tfidf_index[term].append((doc_id, tfidf_score))

    return tfidf_index, idf_scores
            
"""
Convert tokenized query terms into a query vector using IDF
scores.
"""
def create_query_vector(query_terms, idf_scores):
    print("idf scores", idf_scores['academics'])
    query_vector = {}
    for term in query_terms:
        if term in idf_scores:
            query_vector[term] = idf_scores[term]
        else:
        # Term not found in the corpus; optionally handle this case.
            query_vector[term] = 0
            continue
    return query_vector

"""
Calculate the Euclidean norm for each document vector.
"""
def calculate_document_norms(tfidf_index):

    doc_norms = defaultdict(float)
    for term, docs in tfidf_index.items():
        for doc_id, tfidf_score in docs:
            doc_norms[doc_id] += tfidf_score**2
    for doc_id, norm in doc_norms.items():
        doc_norms[doc_id] = math.sqrt(norm)
    return doc_norms


def search_with_cosine_similarity(query_vector, doc_norms, tfidf_index):
    """
    Search documents using cosine similarity based on the query vector
    and TF-IDF index.
    """
    # Initialize a dictionary to hold accumulated dot products for documents
    doc_scores = defaultdict(float)
    # Calculate dot product for each term in the query vector with  document vectors
    for term, query_weight in query_vector.items():
        if term in tfidf_index:
            for doc_id, doc_weight in tfidf_index[term]:
                doc_scores[doc_id] += query_weight * doc_weight
    # Normalize the scores by the document vector norms and calculate cosine similarity
    
    for doc_id in doc_scores.keys():
        doc_scores[doc_id] /= doc_norms[doc_id]
    # Sort documents by score in descending order
    sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_docs
