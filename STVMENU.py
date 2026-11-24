import STCORE
def menu(title, items, shortcuts=(), other_shortcuts=(), page_size=5):
  copied=not isinstance(items,(list,tuple))
  if copied: items=list(items)
  for shortcut in shortcuts if len(shortcuts) <= 3 else ():
    if shortcut in ('C', 'S') and not any(k == shortcut for k, label in items):
      if not copied: items=list(items);copied=True
      items.append((shortcut, 'CHANGE DATA' if shortcut == 'C' else 'SELECT MANY'))
  number=1
  for key,label in items:
    if key.isdigit(): number=max(number,int(key)+1)
  page = min(STCORE._menu_pages.get(title, 0), (len(items)-1)//page_size)
  while True:
    STCORE.heading(title)
    alias=number
    for i,(key,label) in enumerate(items):
      shown=key
      if not key.isdigit() and key not in ('N','P'):
        shown=str(alias);alias+=1
      if page*page_size<=i<(page+1)*page_size:
        if key in ('N','P'):
          shown=('RIGHT' if key=='N' else 'LEFT') if STCORE.HAS_KEYS else ('ENTER' if key=='N' else '-')
        print(shown+' '+label)
    print(('0 EXIT' if title in ('STAT1', 'STAT1 QUICK SOLVE') else ('LEFT / 0 BACK' if STCORE.HAS_KEYS and page == 0 else '0 BACK')) + (((' RIGHT NEXT' if page == 0 else ' RIGHT NEXT LEFT PREV') if STCORE.HAS_KEYS else ' ENTER NEXT - PREV') if len(items) > page_size else ''))
    key = STCORE.read_choice()
    if key == '0':
      STCORE._menu_pages.pop(title, None)
      return key
    if key in ('N', 'P') and any(key == item[0] for item in items):
      return key
    if key == 'N' and len(items) > page_size:
      page = (page + 1) % ((len(items) + page_size - 1) // page_size)
    elif key == 'P':
      if page == 0:
        STCORE._menu_pages.pop(title, None)
        return '0'
      page -= 1
    else:
      alias=number
      for i,(item,label) in enumerate(items):
        shown=item
        if not item.isdigit() and item not in ('N','P'):
          shown=str(alias);alias+=1
        if key in (item,shown):
          if len(STCORE._menu_pages)>32: STCORE._menu_pages.clear()
          STCORE._menu_pages[title]=i//page_size
          return item
      if key in shortcuts or key in other_shortcuts: return key
