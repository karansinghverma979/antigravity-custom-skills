---
name: pdf-toolkit
description: >-
  PDF processing, extraction, merging, and generation engine.
  Use whenever reading or extracting text/tables from PDF files, combining or splitting PDFs,
  inspecting PDF metadata, or writing programmatic PDF generation scripts via pypdf/pdfplumber/reportlab.
---

# 📄 PDF Toolkit: Extraction & Document Manipulation Suite

Use this skill when reading, parsing, merging, splitting, or generating PDF documents.

---

## 🏛️ Core Capabilities & Recipes

For complete code examples and table extraction patterns:
- [PDF Operations Guide](./references/pdf_operations.md)

---

## 🔄 Common Operations

### 1. Quick Inspection & Text Extraction
Run the bundled CLI helper to inspect metadata or extract text:

```bash
# Inspect page count and metadata:
python ~/.gemini/antigravity-cli/skills/pdf-toolkit/scripts/pdf_tools.py inspect document.pdf

# Extract full text to a .txt file:
python ~/.gemini/antigravity-cli/skills/pdf-toolkit/scripts/pdf_tools.py extract document.pdf extracted.txt
```

### 2. Table & Form Data Parsing
Use `pdfplumber` in Python scripts for high-precision table detection without layout loss.
