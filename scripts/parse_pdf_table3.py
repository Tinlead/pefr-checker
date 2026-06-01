import re
from pathlib import Path
import PyPDF2

male_heights = [150 + 2*i for i in range(18)]
female_heights = [150 + 2*i for i in range(17)]


def split_token(t):
    if len(t) <= 3:
        return [t]
    # If last 2 digits form valid age and prefix is plausible value
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
for pi,page in enumerate(reader.pages):
    text = page.extract_text() or ''
    toks = all_tokens(text)
    # detect header
    header_start = None
    row_len = None
    for start in range(len(toks)):
        if toks[start:start+len(male_heights)] == [str(x) for x in male_heights]:
            header_start = start
            row_len = len(male_heights)
            break
        if toks[start:start+len(female_heights)] == [str(x) for x in female_heights]:
            header_start = start
            row_len = len(female_heights)
            break
    if header_start is None:
        print('page', pi+1, 'header not found')
        continue
    data = toks[header_start + row_len:]
    rows=[]
    i=0
    while i < len(data):
        age = int(data[i])
        if 15 <= age <= 100:
            row = data[i+1:i+1+row_len]
            if len(row) != row_len:
                break
            rows.append((age, [int(x) for x in row]))
            i += 1 + row_len
        else:
            i += 1
    print('page',pi+1,'row_len',row_len,'rows',len(rows),'left',len(data)-i)
    print(rows[:3])
    print(rows[-3:])
    print('---')
