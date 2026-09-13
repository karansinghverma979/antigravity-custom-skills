#!/usr/bin/env python3
"""
PDF Toolkit CLI
Performs text extraction, page counting, and file merging on Windows.
"""

import sys
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def inspect_pdf(pdf_path: str):
    try:
        from pypdf import PdfReader
    except ImportError:
        print("[ERROR] 'pypdf' package not installed. Run: pip install pypdf")
        return

    path = Path(pdf_path).resolve()
    if not path.is_file():
        print(f"[ERROR] File not found: {path}")
        return

    reader = PdfReader(str(path))
    print(f"[*] PDF: {path.name}")
    print(f"  - Pages: {len(reader.pages)}")
    if reader.metadata:
        print(f"  - Title: {reader.metadata.title or 'N/A'}")
        print(f"  - Author: {reader.metadata.author or 'N/A'}")

def extract_text(pdf_path: str, out_txt: str = None):
    try:
        from pypdf import PdfReader
    except ImportError:
        print("[ERROR] 'pypdf' package not installed. Run: pip install pypdf")
        return

    path = Path(pdf_path).resolve()
    reader = PdfReader(str(path))
    text_chunks = []
    for idx, page in enumerate(reader.pages, 1):
        txt = page.extract_text() or ""
        text_chunks.append(f"--- [Page {idx}] ---\n{txt}")

    full_text = "\n\n".join(text_chunks)
    if out_txt:
        out_p = Path(out_txt).resolve()
        out_p.write_text(full_text, encoding="utf-8")
        print(f"[OK] Extracted text written to: {out_p}")
    else:
        print(full_text[:1000] + ("\n... [Truncated]" if len(full_text) > 1000 else ""))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_tools.py <inspect|extract> <pdf_path> [output_txt]")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    p_file = sys.argv[2]
    if cmd == "inspect":
        inspect_pdf(p_file)
    elif cmd == "extract":
        out = sys.argv[3] if len(sys.argv) > 3 else None
        extract_text(p_file, out)
    else:
        print(f"Unknown command: {cmd}")
