import re
from pathlib import Path
import PyPDF2
reader = PyPDF2.PdfReader(Path('normal_pEFR_update.pdf'))
for pi,page in enumerate(reader.pages):
    print('PAGE', pi+1)
    text = page.extract_text() or ''
    lines = text.splitlines()
    for i,line in enumerate(lines[:30]):
        print(i, repr(line))
    print('--- total lines', len(lines))
    print()
