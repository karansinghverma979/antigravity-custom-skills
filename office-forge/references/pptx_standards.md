# Headless PowerPoint (.pptx) Authoring Specification

When authoring presentation decks via Python (`python-pptx`), ensure clean typographic rhythm and 16:9 widescreen layout.

---

## 1. Slide Deck Architecture

1. **Widescreen Default (16:9)**:
   - Width: `Inches(13.333)`
   - Height: `Inches(7.5)`
2. **Typography & Hierarchy**:
   - Slide Title: 28pt–32pt Bold (Action-oriented takeaway).
   - Subheadings: 18pt–20pt.
   - Body & Bullet Points: 14pt–16pt.
3. **One Main Idea Per Slide**:
   - Use high-contrast callout boxes, clean tables, or embedded high-res charts rather than walls of text.

---

## 2. Best Practices with `python-pptx`

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Add blank slide
blank_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_layout)

# Add Title
txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.7), Inches(1.0))
tf = txBox.text_frame
p = tf.paragraphs[0]
p.text = "Executive Performance Overview"
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

prs.save("deck.pptx")
```
