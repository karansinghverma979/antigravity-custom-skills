---
name: office-forge
description: >-
  Headless document and spreadsheet generation architect (.xlsx, .pptx, .docx).
  Use whenever generating Excel spreadsheets with formulas and formatting, building 16:9 PowerPoint presentation decks,
  or producing local office files via openpyxl/python-pptx without requiring live Microsoft Office add-ins.
---

# 📄 Office Forge: Headless Document & Spreadsheet Generator

Use this skill when generating standalone Excel workbooks (`.xlsx`), PowerPoint decks (`.pptx`), or Word documents (`.docx`) directly on disk via Python.

---

## 🏛️ Document Standards & Specifications

To ensure high-fidelity outputs without live Office applications:
- **Excel Formatting & Color Codes**: [Excel Standards](./references/xlsx_standards.md)
- **PowerPoint Layout & Widescreen Rules**: [PowerPoint Standards](./references/pptx_standards.md)

---

## 🔄 Headless Generation Workflow

### Step 1: Scaffolding Generation Script
Generate a starter Python builder for the desired format:

```bash
# For Excel (.xlsx):
python ~/.gemini/antigravity-cli/skills/office-forge/scripts/generate_office.py xlsx build_sheet.py

# For PowerPoint (.pptx):
python ~/.gemini/antigravity-cli/skills/office-forge/scripts/generate_office.py pptx build_deck.py
```

### Step 2: Implement Logic & Formulas
- For `.xlsx`: Ensure calculation cells use uppercase formulas (`=SUM(B2:B10)`), inputs are styled in blue text, and headers have high-contrast background fills.
- For `.pptx`: Ensure widescreen `16:9` (`13.333in x 7.5in`) dimensions, one clear title per slide, and readable typography (>=14pt).

### Step 3: Execute & Output Verification
Run the generator script locally to produce the binary file on disk:

```bash
python build_sheet.py
```
Verify the output file exists and has non-zero size.
