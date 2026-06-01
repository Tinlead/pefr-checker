import re
from pathlib import Path
import PyPDF2

path = Path('normal_pEFR_update.pdf')
reader = PyPDF2.PdfReader(path)
for pi, page in enumerate(reader.pages):
    text = page.extract_text() or ''
    nums = [int(x) for x in re.findall(r'\d+', text)]
    print('PAGE', pi+1)
    print('NUM COUNT', len(nums))
    print(nums[:40])
    # try detect first header-like sequences of even numbers at least length 10
    for start in range(0, min(40, len(nums))):
        window = nums[start:start+18]
        if len(window) == 18 and all(window[i] == 150 + 2*i for i in range(18)):
            print(' male header at', start)
        window17 = nums[start:start+17]
        if len(window17) == 17 and all(window17[i] == 150 + 2*i for i in range(17)):
            print(' female header17 at', start)
    print('----')
