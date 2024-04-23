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

# Architecture

Software Components
1. crawler.py: Manages web crawling.
2. html_parser.py: Handles HTML parsing, text extraction, and serves the Flask web application.
3. query_processor.py: Includes functions for creating and querying the TF-IDF index.
Interfaces
Web interface provided by Flask for real-time document querying.
Command-line interface for initiating crawls and queries.

# Implementation
The crawling and parsing operations are modular, allowing independent operation as well as integration.
Data is stored locally, and search operations are performed in-memory.

# Operation
Commands
To start the crawler: scrapy runspider crawler.py
To start the web server: python html_parser.py
CLI search mode: python html_parser.py --cli --query "example query"

# Installation
Dependencies: Scrapy, Flask, BeautifulSoup, Scikit-Learn, NumPy, Pickle.
Install dependencies via pip: pip install -r requirements.txt

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
