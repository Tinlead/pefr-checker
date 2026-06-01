import re
from pathlib import Path
import PyPDF2

path = Path('normal_pEFR_update.pdf')
reader = PyPDF2.PdfReader(path)

for pi, page in enumerate(reader.pages):
    text = page.extract_text() or ''
    nums = [int(x) for x in re.findall(r'\d+', text)]
    header_start = None
    # detect male header 18 and female header 17
    male_heights = [150 + 2*i for i in range(18)]
    female_heights = [150 + 2*i for i in range(17)]
    for start in range(len(nums)):
        if nums[start:start+18] == male_heights:
            header_start = start
            row_len = 18
            break
        if nums[start:start+17] == female_heights:
            header_start = start
            row_len = 17
            break
    if header_start is None:
        print('Page',pi+1,'no header found')
        continue
    data = nums[header_start + row_len:]
    rows=[]
    i=0
    while i < len(data):
        age = data[i]
        if age < 15 or age > 120:
            i += 1
            continue
        row = data[i+1:i+1+row_len]
        if len(row) < row_len:
            break
        rows.append((age,row))
        i += 1 + row_len
    print('PAGE', pi+1, 'row len', row_len, 'rows', len(rows), 'remaining', len(data)-i)
    print(rows[:3])
    print(rows[-3:])
    print('---')
