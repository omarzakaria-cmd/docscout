from flask import Flask, render_template, request

from main import search_documents

app = Flask(__name__)


@app.get("/")
def home():
    query = request.args.get("q", "").strip()
    results = search_documents(query) if query else []

    return render_template(
        "index.html",
        query=query,
        results=results,
    )
