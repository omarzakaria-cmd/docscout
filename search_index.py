from pdf_search import iter_pdf_passages
import sqlite3
from contextlib import closing
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DATABASE_PATH = PROJECT_DIR / "search.db"


def build_index(documents_dir, database_path=DATABASE_PATH):
    documents_dir = Path(documents_dir)

    if not documents_dir.is_dir():
        raise FileNotFoundError(
            f"Document folder does not exist: {documents_dir}"
        )

    rows = []

    for file_path in sorted(documents_dir.glob("*.txt")):
        content = file_path.read_text(encoding="utf-8")

        for line_number, line in enumerate(content.splitlines(), start=1):
            if line.strip():
                rows.append((file_path.name, line_number, line))

    rows.extend(iter_pdf_passages(documents_dir))

    with closing(sqlite3.connect(database_path)) as connection:
        with connection:
            connection.execute(
                "CREATE VIRTUAL TABLE IF NOT EXISTS passages "
                "USING fts5(filename UNINDEXED, location UNINDEXED, content)"
            )
            connection.execute("DELETE FROM passages")
            connection.executemany(
                "INSERT INTO passages(filename, location, content) "
                "VALUES (?, ?, ?)",
                rows,
            )

    return len(rows)


def search_index(query, database_path=DATABASE_PATH):
    if not query.strip():
        return []

    phrase = '"' + query.strip().replace('"', '""') + '"'

    with closing(sqlite3.connect(database_path)) as connection:
        return connection.execute(
            "SELECT filename, location, content "
            "FROM passages WHERE passages MATCH ? "
            "ORDER BY bm25(passages), filename, location",
            (phrase,),
        ).fetchall()


if __name__ == "__main__":
    count = build_index(PROJECT_DIR / "documents")
    print(f"Indexed {count} passages from text files and PDFs.")
