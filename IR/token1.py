import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup
from html_parser import *

class TestHTMLExtraction(unittest.TestCase):
    def test_extract_text_from_html(self):
        html_content = "<html><head><title>Test</title></head><body><p>Hello, world!</p></body></html>"
        url = "http://example.com"
        expected_output = "URL: http://example.com\nHello, world!"
        self.assertEqual(extract_text_from_html(html_content, url), expected_output)
        
    def test_extract_og_url_present(self):
        html_content = '<html><head><meta property="og:url" content="http://example.com"></head></html>'
        self.assertEqual(extract_og_url_from_html(html_content), "http://example.com")

    def test_extract_og_url_absent(self):
        html_content = '<html><head><title>Test</title></head></html>'
        self.assertIsNone(extract_og_url_from_html(html_content))
        
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_post_valid_json(self):
        response = self.client.post('/', data={'json_input': '{"query": "example"}'})
        self.assertEqual(response.status_code, 200)

    def test_index_post_invalid_json(self):
        response = self.client.post('/', data={'json_input': 'invalid json'})
        self.assertEqual(response.status_code, 400)

    def setUp(self):
        self.documents = [
            "Hello world",
            "Hello there",
            "Hi there"
        ]
        self.vectorizer, self.tfidf_matrix = create_tfidf_index(self.documents)

    def test_create_tfidf_index(self):
        self.assertEqual(self.tfidf_matrix.shape, (3, 3))  

    @patch('pickle.dump')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_index(self, mock_open, mock_pickle_dump):
        # Test saving the index
        save_index(self.tfidf_matrix, self.vectorizer, "tfidf_model.pkl")
        mock_open.assert_called_once_with("tfidf_model.pkl", 'wb')
        mock_pickle_dump.assert_called_once()

    @patch('pickle.load')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_load_index(self, mock_open, mock_pickle_load):
        # Prepare a mock TF-IDF matrix and vectorizer to be loaded
        mock_pickle_load.return_value = (self.tfidf_matrix, self.vectorizer)
        matrix, vectorizer = load_index("tfidf_model.pkl")
        self.assertIsNotNone(matrix)
        self.assertIsNotNone(vectorizer)

    def test_search_documents(self):
        # Test searching the documents
        query = "Hello"
        sorted_indices, similarities = search_documents(query, self.vectorizer, self.tfidf_matrix)
        print(sorted_indices[0], sorted_indices[1])
        # Expecting "Hello world" and "Hello there" to be the most similar
        self.assertEqual(sorted_indices[0], 0)  # "Hello world"
        self.assertEqual(sorted_indices[1], 1)  # "Hello there"
        self.assertTrue(np.isclose(similarities[sorted_indices[0]], 1.0, atol=0.1))  # High similarity


if __name__ == '__main__':
    unittest.main()
