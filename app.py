from pathlib import Path

from flask import Flask, abort, render_template, request

from search_index import DATABASE_PATH, search_index

app = Flask(__name__)
app.config["DATABASE_PATH"] = DATABASE_PATH


def search_documents(query):
    database_path = app.config["DATABASE_PATH"]

    if not Path(database_path).is_file():
        abort(
            503,
            description="Search index missing. Run python search_index.py first.",
        )

    return search_index(query, database_path)


@app.get("/")
def home():
    query = request.args.get("q", "").strip()
    results = search_documents(query) if query else []

    return render_template(
        "index.html",
        query=query,
        results=results,
    )
