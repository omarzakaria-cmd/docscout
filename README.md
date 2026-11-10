# DocScout

A personal document search engine built with Python.

## Current features
- Search text files for a word or phrase
- Match text regardless of capitalization
- Display filenames, line numbers, and matching passages
- Run multiple searches in one session
- Handle unreadable files without stopping the search

## Run locally
Requires Python 3.9 or newer. No external packages are required.

```bash
python3 main.py

```

The documents folder includes three sample text files.
Try searching for `python` or `search`. Type `quit` to exit.

## How it works
DocScout reads text files from the documents folder and checks each
line for the search phrase. It returns each matching line with its
filename and line number.

## Current limitations
- Supports text files only
- Uses substring matching
- Searches only the documents folder, without subfolders
- Results are not ranked by relevance

## Planned improvements
- PDF support
- A searchable database index
- A web interface
- Relevance ranking and automated tests
