# Author: TheEliteCodez
# Small numeric text pager; no study definitions loaded.
import STCORE

def text_pages(title, definition):
    # Text input avoids relying on device-specific arrow key codes.
    lines = (definition,)
    count = sum(1 for line in STCORE.wrapped_lines(lines))
    page = 0
    pages = (count + 5) // 6
    while True:
        STCORE.heading(title.upper())
        print('PAGE ' + str(page + 1) + '/' + str(pages))
        for i, line in enumerate(STCORE.wrapped_lines(lines)):
            if i >= (page + 1) * 6: break
            if i >= page * 6: print(line)
        print(('LEFT BACK RIGHT NEXT CLEAR BACK' if page==0 else 'LEFT PREV RIGHT NEXT CLEAR BACK') if STCORE.HAS_KEYS else 'ENTER/1 NEXT  -/2 PREV  0 BACK')
        key = STCORE.read_choice()
        if key == '0': return
        if key in ('1', 'N'):
            if page+1<pages: page+=1
            elif key=='N': return
        elif key in ('2', 'P'):
            if page>0: page-=1
            elif key=='P': return
