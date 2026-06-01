import re
from pathlib import Path
import json
import PyPDF2

path = Path('normal_pEFR_update.pdf')
reader = PyPDF2.PdfReader(path)

# Known header heights sequence
heights = [150 + 2*i for i in range(18)]  # 150..184 step 2

def parse_page(text):
    nums = [int(x) for x in re.findall(r'\d+', text)]
    # find header sequence
    header_idx = None
    for i in range(len(nums) - len(heights) + 1):
        if nums[i:i+len(heights)] == heights:
            header_idx = i
            break
    if header_idx is None:
        raise ValueError('Header not found on page')
    data = nums[header_idx + len(heights):]
    rows = []
    i = 0
    while i < len(data):
        age = data[i]
        if age < 10 or age > 120:
            # skip stray numbers until valid age found
            i += 1
            continue
        row = data[i+1:i+1+len(heights)]
        if len(row) < len(heights):
            break
        if len(row) == len(heights):
            rows.append((age, row))
            i += 1 + len(heights)
        else:
            i += 1
    return rows

male = {}
female = {}
for pi, page in enumerate(reader.pages):
    text = page.extract_text() or ''
    rows = parse_page(text)
    if pi < 4:
        for age, row in rows:
            male[age] = row
    else:
        for age, row in rows:
            female[age] = row

print('male ages', sorted(male.keys())[:5], '...', sorted(male.keys())[-5:])
print('female ages', sorted(female.keys())[:5], '...', sorted(female.keys())[-5:])
print('male count', len(male), 'female count', len(female))

output = {
    'heights': heights,
    'male': male,
    'female': female,
}
print(json.dumps(output, indent=2))
