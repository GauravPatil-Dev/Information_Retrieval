# Information_Retrieval
# Project Documentation

# Abstract
This project involves the development of a web crawling and HTML parsing tool designed to extract text from websites for further text analysis. The primary objective is to implement effective web scraping capabilities combined with a robust text extraction system that leverages TF-IDF for document analysis. The next steps include refining the crawling efficiency, improving the user interface for the text search functionality, and expanding the document processing capabilities to include additional metadata extraction.

# Overview
The system consists of two main components: crawler.py and html_parser.py. The crawler utilizes Scrapy to systematically browse and download web pages from specified domains, specifically designed to handle depth and page count limitations. The parser, built with BeautifulSoup and Flask, extracts and processes text from the HTML files stored by the crawler, offering a web interface for querying the indexed documents. This solution draws on concepts from information retrieval and web scraping literature, proposing an integrated approach to text extraction and search.

# Design
The system is designed to:

1. Crawl websites within predefined domain limits and depth.
2. Extract and save HTML content to a local directory.
3. Parse HTML content to extract text and specific metadata.
4. Index the extracted text using a TF-IDF model.
5. Provide a query interface for searching the indexed documents based on text relevance.

Web Crawling
The system employs a Scrapy crawler (crawler.py) that is configured to scrape a maximum of 100 pages to conserve resources and limit the server load on targeted websites. The crawling depth is set to 3 levels from the initial page, which means the crawler can follow links from the main page to three levels deep. This limitation ensures that the crawl remains focused and relevant to the domain being analyzed.

Parsing and Indexing
Upon retrieving HTML content, the html_parser.py script processes the content using BeautifulSoup to extract text. This text is then indexed using a TF-IDF model, which is a statistical measure used to evaluate how important a word is to a document in a collection of documents. By converting the text data into a TF-IDF matrix, the system can efficiently perform similarity comparisons between the query and the indexed documents, thus supporting effective information retrieval.


# Architecture

Software Components Function Descriptions

1. crawler.py:
IITSpider: The primary class derived from Scrapy's Spider, which manages the crawling process. It is responsible for initiating requests, handling the response, and following links based on the specified rules regarding domain, depth, and page count.
2. html_parser.py:
extract_text_from_html(html_content, url): Extracts plain text from HTML content. It utilizes BeautifulSoup to parse the HTML and remove all markup, returning clean text.
3. extract_og_url_from_html(html_content): Searches for and extracts the 'og:url' meta tag from HTML, which is often used to specify the canonical URL of the page.
4. load_documents(): Loads and processes all .html files stored by the crawler in the local directory, preparing them for indexing.
5. index(): Web server route that handles POST requests for searching indexed documents. It processes input queries and returns search results based on cosine similarity scores.
6. query_processor.py:
7. create_tfidf_index(documents): Creates a TF-IDF matrix and trains a vectorizer on the provided documents to facilitate query processing.
8. search_documents(query, vectorizer, tfidf_matrix): Computes cosine similarity between a query vector and all document vectors in the TF-IDF matrix to find and return the most relevant documents.

9. Interfaces - a. Web interface provided by Flask for real-time document querying.
                b. Command-line interface for initiating crawls and queries.

# Implementation
The crawling and parsing operations are modular, allowing independent operation as well as integration.
Data is stored locally, and search operations are performed in-memory.

# Steps to run
To start the crawler: scrapy runspider crawler.py
To start the web server: python3 html_parser.py
CLI search mode: python3 html_parser.py --cli --query "example query"

# Dependencies
Scrapy, Flask, BeautifulSoup, Scikit-Learn, NumPy, Pickle.

# Conclusion
The crawler and parser successfully perform their intended functions, though the system's scalability and performance in broader domains are yet to be fully tested. Future improvements could include enhanced error handling and expanded metadata extraction capabilities.

# Data Sources
Source code and documentation are self-contained. External data links and access points are not applicable.

# Test Cases
Includes test cases for crawler depth and page limits, parser accuracy, and query response correctness.
Coverage includes unit tests for each function and integration tests for system components.

# Source Code
The source code is organized into three main files: crawler.py, html_parser.py, and query_processor.py.
Dependencies are standard and open-source, listed explicitly in a requirements file.

# Bibliography
References are primarily from official documentation of Python libraries such as Scrapy, BeautifulSoup, Flask, and Scikit-Learn.
1. "Scrapy 2.5 documentation," Scrapy. [Online]. Available: https://docs.scrapy.org/en/latest/
2. "Beautiful Soup Documentation," Crummy. [Online]. Available: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
3. "scikit-learn: machine learning in Python," Scikit-Learn. [Online]. Available: https://scikit-learn.org/stable/
4. "Flask Documentation," Pallets Projects. [Online]. Available: https://flask.palletsprojects.com/en/2.0.x/