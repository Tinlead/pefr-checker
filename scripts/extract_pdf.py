import PyPDF2
from pathlib import Path
path = Path('normal_pEFR_update.pdf')
reader = PyPDF2.PdfReader(path)
print('PAGES', len(reader.pages))
for i, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ''
    print('PAGE', i)
    print(text[:4000])
    print('-' * 80)
