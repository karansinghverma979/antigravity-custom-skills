# PDF Operations & Scripting Guide

This reference provides deterministic Python patterns for common PDF manipulation tasks using `pypdf` and `pdfplumber`.

---

## 1. Text & Table Extraction

### Text Extraction (`pypdf`):
```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
text = "\n".join([page.extract_text() or "" for page in reader.pages])
```

### Table Extraction (`pdfplumber`):
```python
import pdfplumber

with pdfplumber.open("tables.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)
```

---

## 2. Merging & Splitting

### Merging Multiple PDFs:
```python
from pypdf import PdfWriter

writer = PdfWriter()
for pdf in ["part1.pdf", "part2.pdf"]:
    writer.append(pdf)
writer.write("combined.pdf")
```

### Splitting Pages:
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("source.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as f:
        writer.write(f)
```
