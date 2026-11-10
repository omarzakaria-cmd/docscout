import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import app


class WebTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        documents = Path(self.temp_dir.name)
        (documents / "sample.txt").write_text(
            "Learning Python\n<script>alert(1)</script>\n",
            encoding="utf-8",
        )

        patcher = patch("main.DOCUMENTS_DIR", documents)
        patcher.start()
        self.addCleanup(patcher.stop)

        self.client = app.test_client()

    def test_homepage_loads_without_searching(self):
        with patch("app.search_documents") as search:
            response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Ready to explore?", response.data)
        search.assert_not_called()

    def test_search_displays_matching_passage(self):
        response = self.client.get(
            "/", query_string={"q": "PYTHON"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"1 matching lines", response.data)
        self.assertIn(b"sample.txt", response.data)
        self.assertIn(b"Line 1", response.data)
        self.assertIn(b"Learning Python", response.data)

    def test_no_matches_displays_message(self):
        response = self.client.get(
            "/", query_string={"q": "elephant"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No matches found.", response.data)

    def test_blank_query_does_not_search(self):
        with patch("app.search_documents") as search:
            response = self.client.get(
                "/", query_string={"q": "   "}
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Ready to explore?", response.data)
        search.assert_not_called()

    def test_document_html_is_displayed_as_text(self):
        response = self.client.get(
            "/", query_string={"q": "alert"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"&lt;script&gt;", response.data)
        self.assertNotIn(b"<script>", response.data)


if __name__ == "__main__":
    unittest.main()
