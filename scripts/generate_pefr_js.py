import re
from pathlib import Path
import PyPDF2
import json

male_heights = [150 + 2*i for i in range(18)]
female_heights = [150 + 2*i for i in range(17)]


def split_token(t):
    if len(t) <= 3:
        return [t]
    age = int(t[-2:])
    prefix = int(t[:-2])
    if 15 <= age <= 100 and 10 <= prefix <= 999:
        return [str(prefix), str(age)]
    return [t]


def all_tokens(text):
    raw = re.findall(r'\d+', text)
    out = []
    for t in raw:
        out.extend(split_token(t))
    return out

reader = PyPDF2.PdfReader(Path('normal_pEFR_update.pdf'))
pefr = {
    'male': {'heights': male_heights, 'values': {}},
    'female': {'heights': female_heights, 'values': {}},
}
for pi,page in enumerate(reader.pages):
    text = page.extract_text() or ''
    toks = all_tokens(text)
    header_start = None
    row_len = None
    gender = None
    for start in range(len(toks)):
        if toks[start:start+len(male_heights)] == [str(x) for x in male_heights]:
            header_start = start
            row_len = len(male_heights)
            gender = 'male'
            break
        if toks[start:start+len(female_heights)] == [str(x) for x in female_heights]:
            header_start = start
            row_len = len(female_heights)
            gender = 'female'
            break
    if header_start is None:
        raise ValueError(f'header not found on page {pi+1}')
    data = toks[header_start + row_len:]
    i = 0
    while i < len(data):
        age = int(data[i])
        row = data[i+1:i+1+row_len]
        if len(row) != row_len:
            break
        row_vals = [int(x) for x in row]
        pefr[gender]['values'][str(age)] = row_vals
        i += 1 + row_len

with open('pefr_data.js', 'w', encoding='utf-8') as f:
    f.write('const PEFR_TABLE = ')
    json.dump(pefr, f, indent=2, ensure_ascii=False)
    f.write(';\n')
print('written pefr_data.js')
