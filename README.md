# DocScout

A personal document search engine built with Python and Flask.

## Features
- Highlight matching text in browser results
- Browser interface and command-line search
- PDF search with page numbers
- Case-insensitive word or phrase matching
- Results with filenames, line numbers, and matching passages
- Twenty-five automated tests covering search, PDFs, the database, highlighting, and the web interface

## Setup
Requires Python 3.9 or newer.

From the project folder, run these commands in order:

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt

## Build or refresh the search index

    python search_index.py

Run this before your first browser search and whenever documents are added, edited, or removed.
The local search.db database is excluded from Git.

## Run the website

    python -m flask --app app run --port 5050

Open http://127.0.0.1:5050 in your browser.
Press Control+C in Terminal to stop the server.
This server is for local development.

## Command-line search

    python3 main.py

Type a word or phrase to search. Type quit to exit.
Both interfaces require the packages in requirements.txt.

## Sample documents
Three sample text files are included in the documents folder.
Try searching for python or search.

## Run tests

    python -m unittest -v

## How it works
The index builder extracts passages from text files and PDFs into a local SQLite FTS5 database.
The browser searches that stored text and ranks results using BM25.
The command-line interface reads source files directly.

## Current limitations
- Supports text files and text-based PDFs
- Scanned PDFs require OCR, which is not yet supported
- Password-protected PDFs are skipped
- Browser search matches whole words and phrases
- Command-line search uses substring matching
- Searches only the documents folder, without subfolders

## Planned improvements
- Document type filters

## Search your own PDFs
Copy a text-based PDF into the documents folder, then search for a word in it.
PDF results show physical page numbers starting at 1.
Local PDFs in this folder are excluded from Git by .gitignore.
