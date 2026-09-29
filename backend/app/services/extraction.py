"""Document text extraction with page provenance (Guide Step 5).

Strategy: PyMuPDF first (fast, keeps page numbers). If a page yields almost
no text it is probably a scan -> fall back to Tesseract OCR for that page.
"""
import fitz  # PyMuPDF
import pytesseract
from PIL import Image


def extract_pages(pdf_bytes: bytes) -> list[dict]:
    """Return [{'page': 1, 'text': '...', 'method': 'pymupdf'|'ocr'}, ...]."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        method = "pymupdf"
        if len(text) < 50:  # likely a scanned image page
            pix = page.get_pixmap(dpi=200)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img).strip()
            method = "ocr"
        pages.append({"page": i + 1, "text": text, "method": method})
    return pages
