from pathlib import Path
import sys

try:
    import pypdf
except Exception as e:
    print('PYPDF_IMPORT_ERROR', e)
    sys.exit(0)

pdf_path = Path('Capstone Project _ CrisisOps AI team 2.pdf')
reader = pypdf.PdfReader(str(pdf_path))
print('PAGES', len(reader.pages))
for i, p in enumerate(reader.pages):
    text = p.extract_text() or ''
    print(f'--- PAGE {i+1} ---')
    print(text[:4000])
    print()
