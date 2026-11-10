# DocScout

A personal document search engine built with Python and Flask.

## Features
- Browser interface and command-line search
- Case-insensitive word or phrase matching
- Results with filenames, line numbers, and matching passages
- Eight automated tests covering search and the web interface

## Setup
Requires Python 3.9 or newer.

From the project folder, run these commands in order:

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt

## Run the website

    python -m flask --app app run --port 5050

Open http://127.0.0.1:5050 in your browser.
Press Control+C in Terminal to stop the server.
This server is for local development.

## Command-line search

    python3 main.py

Type a word or phrase to search. Type quit to exit.
The command-line version requires no external packages.

## Sample documents
Three sample text files are included in the documents folder.
Try searching for python or search.

## Run tests

    python -m unittest -v

## How it works
Flask receives the search phrase from the browser and calls the
same search function used by the command-line application.
The function reads text files and returns matching lines.
An HTML template displays the results.

## Current limitations
- Supports text files only
- Uses substring matching
- Searches only the documents folder, without subfolders
- Results are not ranked by relevance

## Planned improvements
- PDF support
- A searchable database index
- Relevance ranking
