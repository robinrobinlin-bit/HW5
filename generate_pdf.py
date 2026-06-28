import pypandoc
import sys
import os

# Ensure pandoc binary is available (download if necessary)
try:
    pypandoc.get_pandoc_version()
except OSError:
    pypandoc.download_pandoc()

# Ensure TinyTeX LaTeX distribution is installed
try:
    # Import pytinytex and install missing LaTeX components if needed
    import pytinytex
    # install full TinyTeX if not already present
    pytinytex.install()
except Exception as e:
    print('Error installing TinyTeX:', e)
    sys.exit(1)

# Paths (adjust if needed)
md_path = r"C:/Users/user/.gemini/antigravity-ide/brain/a30454bf-57b4-451d-be5a-248f2328cf47/whitepaper.md"
pdf_path = r"C:/Users/user/Desktop/hw8_svm/whitepaper.pdf"

# Ensure output directory exists
os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

try:
    # Use default PDF engine provided by TinyTeX (pdflatex)
    output = pypandoc.convert_file(
        md_path,
        'pdf',
        outputfile=pdf_path,
        extra_args=['--toc', '--metadata', 'title=Top 10 Machine Learning Algorithms Whitepaper']
    )
    print('PDF generated at:', pdf_path)
except Exception as e:
    print('Error generating PDF:', e)
    sys.exit(1)
