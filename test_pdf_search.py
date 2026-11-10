import tempfile
import unittest
from pathlib import Path

from pypdf import PdfWriter

from pdf_search import search_pdfs


class PdfSearchTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.documents = Path(self.temp_dir.name)

    def test_empty_folder_returns_no_results(self):
        results = search_pdfs("python", self.documents)

        self.assertEqual(results, [])

    def test_blank_pdf_returns_no_results(self):
        with PdfWriter() as writer:
            writer.add_blank_page(width=612, height=792)
            writer.write(self.documents / "blank.pdf")

        results = search_pdfs("python", self.documents)

        self.assertEqual(results, [])

    def test_password_protected_pdf_is_skipped(self):
        with PdfWriter() as writer:
            writer.add_blank_page(width=612, height=792)
            writer.encrypt("test-password")
            writer.write(self.documents / "locked.pdf")

        results = search_pdfs("python", self.documents)

        self.assertEqual(results, [])

    def test_blank_query_returns_no_results(self):
        results = search_pdfs("   ", self.documents)

        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
