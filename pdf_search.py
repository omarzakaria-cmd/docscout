from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import PdfReadError


def iter_pdf_passages(documents_dir):
    files = sorted(
        path for path in Path(documents_dir).iterdir()
        if path.is_file() and path.suffix.lower() == ".pdf"
    )

    for file_path in files:
        try:
            with file_path.open("rb") as pdf_file:
                reader = PdfReader(pdf_file)

                if reader.is_encrypted:
                    print(f"Skipping password-protected PDF: {file_path.name}")
                    continue

                for page_number, page in enumerate(reader.pages, start=1):
                    text = page.extract_text() or ""

                    for line in text.splitlines():
                        if line.strip():
                            yield file_path.name, page_number, line

        except (OSError, PdfReadError, ValueError, NotImplementedError) as error:
            print(f"Could not read {file_path.name}: {error}")


def search_pdfs(query, documents_dir):
    if not query.strip():
        return []

    return [
        (filename, page_number, text)
        for filename, page_number, text in iter_pdf_passages(documents_dir)
        if query.casefold() in text.casefold()
    ]
