import tempfile
import unittest
from pathlib import Path

from search_index import build_index, search_index


class IndexTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        root = Path(self.temp_dir.name)
        self.documents = root / "documents"
        self.documents.mkdir()
        self.database = root / "test.db"

        self.sample = self.documents / "notes.txt"
        self.sample.write_text(
            "Learning Python\nBuilding a search engine\n",
            encoding="utf-8",
        )
        build_index(self.documents, self.database)

    def test_search_reads_stored_text(self):
        self.sample.unlink()

        results = search_index("PYTHON", self.database)

        self.assertEqual(
            results,
            [("notes.txt", 1, "Learning Python")],
        )

    def test_rebuild_removes_deleted_documents(self):
        self.sample.unlink()
        build_index(self.documents, self.database)

        self.assertEqual(search_index("python", self.database), [])

    def test_rebuild_does_not_duplicate_results(self):
        build_index(self.documents, self.database)

        self.assertEqual(
            search_index("python", self.database),
            [("notes.txt", 1, "Learning Python")],
        )

    def test_phrase_search(self):
        self.assertEqual(
            search_index("search engine", self.database),
            [("notes.txt", 2, "Building a search engine")],
        )

    def test_blank_query_returns_no_results(self):
        self.assertEqual(search_index("   ", self.database), [])

    def test_special_characters_do_not_break_search(self):
        self.assertEqual(
            search_index('" OR *', self.database),
            [],
        )


if __name__ == "__main__":
    unittest.main()
