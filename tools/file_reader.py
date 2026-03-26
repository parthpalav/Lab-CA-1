import os

import fitz


def extract_text_from_pdf(path):
    try:
        doc = fitz.open(path)
    except Exception as e:
        raise ValueError(f"Unable to open PDF '{path}': {e}") from e

    try:
        is_encrypted = bool(getattr(doc, "is_encrypted", False))
        needs_pass = bool(getattr(doc, "needs_pass", False))
        if is_encrypted or needs_pass:
            raise ValueError(f"PDF '{path}' is encrypted and cannot be processed.")

        pages = []
        for page in doc:
            pages.append(page.get_text("text"))

        text = "\n".join(pages).strip()
        if not text:
            raise ValueError(f"PDF '{path}' is empty or contains no extractable text.")

        return text
    finally:
        doc.close()


def read_file(path):
    if os.path.splitext(path)[1].lower() == ".pdf":
        return extract_text_from_pdf(path)

    with open(path, "r") as f:
        return f.read()