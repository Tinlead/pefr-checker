import re
from pathlib import Path
import PyPDF2
reader = PyPDF2.PdfReader(Path('normal_pEFR_update.pdf'))
for pi,page in enumerate(reader.pages):
    text = page.extract_text() or ''
    tokens = re.findall(r'\d+', text)
    big = [t for t in tokens if len(t) > 3]
    print('PAGE', pi+1, 'big tokens', big[:20], 'count', len(big))
