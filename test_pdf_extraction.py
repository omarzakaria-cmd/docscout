import tempfile
import unittest
from pathlib import Path

from pypdf import PdfWriter
from pypdf.generic import (
    DecodedStreamObject,
    DictionaryObject,
    NameObject,
)

from pdf_search import search_pdfs


class PdfExtractionTests(unittest.TestCase):
    def test_extracts_text_and_returns_correct_page(self):
        with tempfile.TemporaryDirectory() as folder:
            documents = Path(folder)

            with PdfWriter() as writer:
                writer.add_blank_page(width=612, height=792)
                page = writer.add_blank_page(width=612, height=792)

                font = DictionaryObject({
                    NameObject("/Type"): NameObject("/Font"),
                    NameObject("/Subtype"): NameObject("/Type1"),
                    NameObject("/BaseFont"): NameObject("/Helvetica"),
                })

                page[NameObject("/Resources")] = DictionaryObject({
                    NameObject("/Font"): DictionaryObject({
                        NameObject("/F1"): font,
                    }),
                })

                content = DecodedStreamObject()
                content.set_data(
                    b"BT /F1 12 Tf 72 720 Td (Learning Python) Tj ET"
                )
                page.replace_contents(content)
                writer.write(documents / "example.pdf")

            results = search_pdfs("PYTHON", documents)

            self.assertEqual(
                results,
                [("example.pdf", 2, "Learning Python")],
            )


if __name__ == "__main__":
    unittest.main()
