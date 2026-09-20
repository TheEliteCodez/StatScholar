# Author: TheEliteCodez
# Display/menu code loads only for the active screen.
import STCORE as c

def view(title, lines):
    if len(lines) == 0:
        lines = ('NO CONTENT',)
    count = sum((1 for line in c.wrapped_lines(lines)))
    top = 0
    max_top = max(0, count - c.VIEW_LINES)
    while True:
        c.cls()
        end = min(count, top + c.VIEW_LINES)
        print(title[:30])
        print(str(top + 1) + '-' + str(end) + '/' + str(count))
        for i, line in enumerate(c.wrapped_lines(lines)):
            if i >= end:
                break
            if i >= top:
                print(line)
        if c.HAS_KEYS:
            print('UP/DN SCROLL RIGHT NEXT')
            print('LEFT BACK  CLEAR BACK' if top==0 else 'LEFT PREV  CLEAR BACK')
        else:
            print('ENTER NEXT  - PREV  0 BACK')
        k = c.wait_key()
        if k in ('up', 'u'):
            if top > 0:
                top -= 1
        elif k == 'left':
            if top==0: return 'back'
            top = max(0, top - c.VIEW_LINES)
        elif k == 'right':
            if top==max_top: return
            top = min(max_top, top + c.VIEW_LINES)
        elif k in ('down', 'd', 'enter'):
            if top < max_top:
                top += 1
            elif k=='enter': return
        elif k in ('b', 'esc'):
            return

def menu(title, items, shortcuts=(), other_shortcuts=(), page_size=5):
    page = 0
    while True:
        c.heading(title)
        for key, label in items[page * page_size:(page + 1) * page_size]:
            shown={'N':'RIGHT','P':'LEFT'}.get(key,key) if c.HAS_KEYS else {'N':'ENTER','P':'-'}.get(key,key)
            print(shown + ' ' + label)
        print((('0 EXIT  ENTER: TYPE ID' if c.HAS_KEYS else '0 EXIT / TYPE GUIDE OR Q ID') if title in ('STAT1', 'STAT1 QUICK SOLVE') else ('LEFT / 0 BACK' if c.HAS_KEYS and page==0 else '0 BACK')) + (((' RIGHT NEXT' if page==0 else ' RIGHT NEXT LEFT PREV') if c.HAS_KEYS else ' ENTER NEXT - PREV') if len(items) > page_size else ''))
        key = c.read_choice()
        if key == '0':
            return key
        if key in ('N','P') and any(key==item[0] for item in items):
            return key
        if key == 'N' and len(items) > page_size:
            page = (page + 1) % ((len(items) + page_size - 1) // page_size)
        elif key == 'P':
            if page==0: return '0'
            page-=1
        elif any((key == item[0] for item in items)):
            return key
        elif key in shortcuts or key in other_shortcuts or (title == 'STAT1' and key.startswith('PT') and key[2:].isdigit() and (1 <= int(key[2:]) <= 24)):
            return key

def results(title, answers, steps=None, default_places=4):
    style, places = ('D', default_places)
    while True:
        lines = []
        for label, value in answers:
            lines.append(label + '=' + c.answer_text(value, style, places))
        if c.view(title, lines)=='back': return
        key = c.menu('ANSWER FORMAT', [('1', 'DONE / NEXT PART'), ('2', 'DECIMAL PLACES'), ('3', 'REDUCED FRACTIONS'), ('4', 'PERCENT PLACES'), ('5', 'SHOW METHOD')])
        if key in ('0', '1'):
            return
        if key == '5':
            c.view('WORK / FORMULA', steps or ['NO ADDITIONAL METHOD'])
            continue
        if key == '3':
            style = 'F'
        else:
            style = 'P' if key == '4' else 'D'
            places = max(0, c.read_int('DECIMAL PLACES: '))

def paged_results(title, count, row_at, steps=None):
    if count <= c.VIEW_LINES:
        c.results(title, [row_at(i) for i in range(count)], steps)
        return
    start = 0
    style, places = ('D', 4)
    while True:
        end = min(count, start + c.VIEW_LINES)
        lines = []
        for i in range(start, end):
            label, value = row_at(i)
            lines.append(label + '=' + c.answer_text(value, style, places))
        if c.view(title, ['ROWS ' + str(start + 1) + '..' + str(end) + '/' + str(count)] + lines)=='back':
            if start==0: return
            start=max(0,start-c.VIEW_LINES)
            continue
        key = c.menu('TABLE PAGE / FORMAT', [('N', 'NEXT ROWS'), ('P', 'PREVIOUS ROWS' if start else 'BACK'), ('2', 'DECIMAL PLACES'), ('3', 'REDUCED FRACTIONS'), ('4', 'PERCENT PLACES'), ('5', 'SHOW METHOD')], page_size=6)
        if key == '5':
            c.view('WORK / FORMULA', steps or ['NO ADDITIONAL METHOD'])
            continue
        if key == '0':
            return
        if key == 'N':
            if end < count:
                start = end
        elif key == 'P':
            if start==0: return
            start = max(0, start - c.VIEW_LINES)
        elif key == '3':
            style = 'F'
        else:
            style = 'P' if key == '4' else 'D'
            places = max(0, c.read_int('DECIMAL PLACES: '))

def choice_pages(title, pages):
    page = 0
    while True:
        c.heading(title)
        for i, (label, token) in enumerate(pages[page]):
            print(str(i + 1) + ' ' + label[:28])
        print(('LEFT BACK / RIGHT NEXT' if page==0 else 'LEFT PREV / RIGHT NEXT') if c.HAS_KEYS else '0 BACK ENTER NEXT - PREVIOUS')
        key = c.read_choice()
        if key == '0':
            return None
        if key == 'N':
            page = (page + 1) % len(pages)
        elif key == 'P':
            if page==0: return None
            page-=1
        elif key.isdigit() and 1 <= int(key) <= len(pages[page]):
            return pages[page][int(key) - 1][1]
