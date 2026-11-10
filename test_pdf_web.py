import unittest
from unittest.mock import patch

from app import app


class PdfWebTests(unittest.TestCase):
    def test_pdf_result_displays_page_number(self):
        sample_results = [
            ("example.pdf", 2, "Python appears on this page.")
        ]

        with patch("app.search_documents", return_value=sample_results):
            response = app.test_client().get(
                "/", query_string={"q": "Python"}
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"example.pdf", response.data)
        self.assertIn(b"Page 2", response.data)
        self.assertNotIn(b"Line 2", response.data)
        self.assertIn(b"Python appears on this page.", response.data)


if __name__ == "__main__":
    unittest.main()
