import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from main import search_documents


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        documents = Path(self.temp_dir.name)
        sample = documents / "notes.txt"
        sample.write_text(
            "Learning Python\nBuilding a search engine\n",
            encoding="utf-8",
        )

        patcher = patch("main.DOCUMENTS_DIR", documents)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_search_ignores_capitalization(self):
        results = search_documents("PYTHON")

        self.assertEqual(
            results,
            [("notes.txt", 1, "Learning Python")],
        )

    def test_search_returns_correct_line_number(self):
        results = search_documents("search engine")

        self.assertEqual(
            results,
            [("notes.txt", 2, "Building a search engine")],
        )

    def test_missing_phrase_returns_no_results(self):
        results = search_documents("elephant")

        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
