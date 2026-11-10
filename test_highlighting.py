import unittest
from unittest.mock import patch

from app import app
from highlighting import highlight_matches


class HighlightingTests(unittest.TestCase):
    def test_highlights_all_matches_ignoring_case(self):
        result = highlight_matches("Python and PYTHON", "python")

        self.assertEqual(
            str(result),
            "<mark>Python</mark> and <mark>PYTHON</mark>",
        )

    def test_escapes_document_html(self):
        result = highlight_matches("<script>Python</script>", "python")

        self.assertEqual(
            str(result),
            "&lt;script&gt;<mark>Python</mark>&lt;/script&gt;",
        )

    def test_treats_search_as_literal_text(self):
        result = highlight_matches("Learn C++ today", "C++")

        self.assertEqual(
            str(result),
            "Learn <mark>C++</mark> today",
        )

    def test_blank_query_only_escapes_text(self):
        result = highlight_matches("<b>Python</b>", "   ")

        self.assertEqual(str(result), "&lt;b&gt;Python&lt;/b&gt;")

    def test_web_results_include_highlight(self):
        results = [("notes.txt", 1, "Learning Python")]

        with patch("app.search_documents", return_value=results):
            response = app.test_client().get(
                "/", query_string={"q": "python"}
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Learning <mark>Python</mark>", response.data)


if __name__ == "__main__":
    unittest.main()
