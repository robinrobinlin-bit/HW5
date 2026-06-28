import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_JUSTIFY

# Paths
md_path = r"C:/Users/user/.gemini/antigravity-ide/brain/a30454bf-57b4-451d-be5a-248f2328cf47/whitepaper.md"
pdf_path = r"C:/Users/user/Desktop/hw8_svm/whitepaper_reportlab.pdf"

# Ensure output directory exists
os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

# Load markdown content (very simple processing: keep headings and paragraphs)
with open(md_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Prepare document
doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                        rightMargin=40, leftMargin=40,
                        topMargin=60, bottomMargin=60)
styles = getSampleStyleSheet()
# Custom style for body text
body_style = ParagraphStyle(
    name='Body',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10,
    leading=12,
    alignment=TA_JUSTIFY,
)
# Style for headings
heading_style = styles['Heading1']
heading_style.fontName = 'Helvetica-Bold'
heading_style.fontSize = 14
heading_style.leading = 18

story = []
for line in lines:
    stripped = line.strip()
    if not stripped:
        # empty line -> add space
        story.append(Spacer(1, 12))
        continue
    if stripped.startswith('#'):
        # heading level detection (simple)
        level = len(stripped) - len(stripped.lstrip('#'))
        text = stripped.lstrip('#').strip()
        # Use appropriate heading style
        style = styles.get(f'Heading{min(level,4)}', heading_style)
        story.append(Paragraph(text, style))
        story.append(Spacer(1, 8))
    else:
        # regular paragraph
        story.append(Paragraph(stripped, body_style))
        story.append(Spacer(1, 6))

# Build PDF
doc.build(story)
print('PDF generated at', pdf_path)
