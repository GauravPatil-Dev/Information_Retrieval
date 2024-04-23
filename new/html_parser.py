import json
from bs4 import BeautifulSoup
import os
from flask import Flask, request, render_template_string, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import argparse
import pickle
import numpy as np
from query_processor import *

app = Flask(__name__)

def extract_text_from_html(html_content, url):
    soup = BeautifulSoup(html_content, 'lxml')
    text = soup.get_text(separator=' ', strip=True)
    document = f"URL: {url}\n{text}"
    return document

def extract_og_url_from_html(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    og_url_tag = soup.find('meta', property='og:url')
    if og_url_tag and 'content' in og_url_tag.attrs:
        return og_url_tag['content']
    return None

def load_documents():
    output_dir = 'output'
    documents = []
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        if os.path.isfile(file_path) and filename.endswith('.html'):
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
            url = extract_og_url_from_html(html_content) or 'Unknown URL'
            document = extract_text_from_html(html_content, url)
            documents.append(document)
    return documents

docs = load_documents()
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        json_str = request.form['json_input']
        try:
            data = json.loads(json_str)
            query = data.get('query', '')
            if query:
                sorted_doc_indices, cosine_similarities = search_documents(query, vectorizer, tfidf_matrix)
                results = [{
                    'document_id': int(idx),
                    'score': float(cosine_similarities[idx]),
                    'snippet': docs[idx].split('\n', 1)[1][:150] + "..."
                } for idx in sorted_doc_indices[:5]]  # Limiting results to top 5 for brevity
                return jsonify(results)
        except ValueError:
            return jsonify({"error": "Invalid JSON format"}), 400
    return render_template_string('''
        <form action="/" method="post">
            <label for="json_input">Enter JSON input:</label><br>
            <textarea id="json_input" name="json_input" rows="4" cols="50" placeholder='{"query": "example"}'></textarea><br>
            <input type="submit" value="Search">
        </form>
    ''')

parser = argparse.ArgumentParser(description='Search Documents via Web or CLI')
parser.add_argument('--cli', action='store_true', help='Enable CLI mode')
parser.add_argument('--query', type=str, help='Query string for CLI mode')
args = parser.parse_args()


if __name__ == '__main__':
    tfidf_matrix, vectorizer = create_tfidf_index(docs)
    save_index(tfidf_matrix, vectorizer)
    tfidf_matrix, vectorizer = load_index()

    if args.cli:
        if args.query:
            # Process the query from CLI
            sorted_doc_indices, cosine_similarities = search_documents(args.query, vectorizer, tfidf_matrix)
            results = [{
                'document_id': int(idx),
                'score': float(cosine_similarities[idx]),
                'snippet': docs[idx].split('\n', 1)[1][:150] + "..."
            } for idx in sorted_doc_indices[:5]]
            print(json.dumps(results, indent=4))
        else:
            print("No query provided. Use --query to specify the search term.")
    else:
        app.run(debug=True)
