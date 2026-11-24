import STCORE as c
def view(title, lines, graph=False, top=0):
  if len(lines) == 0:
    lines = ('NO CONTENT',)
  count = sum((1 for line in c.wrapped_lines(lines)))
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
    if graph: print('6 SHOW GRAPH  < BACK  > NEXT')
    elif c.HAS_KEYS:
      print('LEFT = BACK  RIGHT = NEXT')
    else:
      print('ENTER NEXT  - PREV  0 BACK')
    k = c.wait_key()
    if k=='6' and graph: return ('graph',top)
    if k in ('up', 'u'):
      if top > 0:
        top -= 1
    elif k == 'left':
      if top == 0: return 'back'
      top = max(0, top - c.VIEW_LINES)
    elif k == 'right':
      if top == max_top: return
      top = min(max_top, top + c.VIEW_LINES)
    elif k in ('down', 'd', 'enter'):
      if top < max_top:
        top += 1
      elif k == 'enter': return
    elif k in ('b', 'esc'):
      return 'exit'
