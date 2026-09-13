# Headless Excel (.xlsx) Authoring Specification

When authoring Excel workbooks via Python (`openpyxl`), follow clean modeling standards.

---

## 1. Sheet Architecture

1. **Tab Structure**:
   - `Inputs`: Hardcoded assumptions, raw numbers, parameters.
   - `Calculations` / `Model`: Pure formulas linking to the `Inputs` tab.
   - `Summary` / `Dashboard`: Key metrics, formatted KPIs, and charts.
2. **Color Conventions**:
   - **Blue text (`#0000FF`)**: Hardcoded input values.
   - **Black text (`#000000`)**: Calculated formulas.
   - **Green text (`#008000`)**: External links / cross-tab references.

---

## 2. Best Practices with `openpyxl`

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = Workbook()
ws = wb.active
ws.title = "Summary"

# Formatting Headers
ws["A1"] = "Metric"
ws["B1"] = "Value"
ws["A1"].font = Font(bold=True, color="FFFFFF")
ws["B1"].font = Font(bold=True, color="FFFFFF")
ws["A1"].fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
ws["B1"].fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")

wb.save("output.xlsx")
```
