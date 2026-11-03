from STCORE import read_raw_key, normalize_key, wait_key
import STCORE
def read_choice():
    if not STCORE.HAS_KEYS:
        key = input('> ').strip().upper()
        return {'':'N','-':'P'}.get(key, key)
    text = ''
    while True:
        raw = read_raw_key()
        key = normalize_key(raw)
        if key == 'left': return 'P'
        if key == 'right': return 'N'
        if key == 'esc': return '0'
        if key == 'delete':
            text = text[:-1]
            print('CHOICE: ' + text)
            continue
        if key == 'enter':
            return text or input('CHOICE / ID: ').strip().upper()
        char = ''
        if isinstance(raw, str) and len(raw) == 1:
            char = raw.upper()
        elif STCORE.KEY_STYLE == 'ce':
            if 142 <= raw <= 151: char = str(raw-142)
            elif 243 <= raw <= 251: char = str(raw-242)
            elif raw == 62: char = '0'
            elif raw in (178,179,204,173,174,175,168,169,170,153):
                char = str((178,179,204,173,174,175,168,169,170,153).index(raw)+1)[-1]
            elif 154 <= raw <= 179: char = chr(65+raw-154)
        else:
            char = {102:'0',92:'1',93:'2',94:'3',82:'4',83:'5',84:'6',72:'7',73:'8',74:'9'}.get(raw, '')
        if char:
            text += char
            print('> ' + text)
