"""
pdf_parser.py
--------------
Handles extracting clean, readable text from an uploaded resume PDF.

We use pdfplumber as the primary extractor because it handles
column layouts and tables (common in resumes) better than most
libraries. If pdfplumber fails (e.g. on a weird/corrupted PDF),
we fall back to PyMuPDF (fitz).
"""

import pdfplumber
import fitz  # PyMuPDF
import re


def extract_text_pdfplumber(file) -> str:
    """Extract text using pdfplumber. `file` is a file-like object (BytesIO)."""
    text_chunks = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)
    return "\n".join(text_chunks)


def extract_text_pymupdf(file) -> str:
    """Fallback extractor using PyMuPDF. `file` is a file-like object (BytesIO)."""
    file.seek(0)
    text_chunks = []
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text_chunks.append(page.get_text())
    return "\n".join(text_chunks)


def clean_text(raw_text: str) -> str:
    """
    Normalize whitespace, remove weird bullet symbols / control chars,
    and collapse multiple blank lines so downstream NLP works cleanly.
    """
    text = raw_text.replace("\x0c", " ")  # form feed chars pdfplumber sometimes leaves
    text = re.sub(r"[•●▪◦]", "-", text)   # normalize bullet symbols
    text = re.sub(r"[ \t]+", " ", text)   # collapse repeated spaces/tabs
    text = re.sub(r"\n{2,}", "\n\n", text)  # collapse repeated blank lines
    return text.strip()


def extract_resume_text(uploaded_file) -> str:
    """
    Main entry point. Takes a Streamlit UploadedFile (or any file-like
    object) and returns cleaned resume text as a single string.

    Tries pdfplumber first; if it returns little/no text (common with
    scanned or image-based PDFs) it retries with PyMuPDF.
    """
    uploaded_file.seek(0)
    try:
        text = extract_text_pdfplumber(uploaded_file)
    except Exception:
        text = ""

    if len(text.strip()) < 30:  # suspiciously little text -> try fallback
        try:
            text = extract_text_pymupdf(uploaded_file)
        except Exception:
            pass

    if len(text.strip()) < 30:
        raise ValueError(
            "Could not extract readable text from this PDF. "
            "It may be a scanned/image-based resume — try exporting a "
            "text-based PDF instead."
        )

    return clean_text(text)
