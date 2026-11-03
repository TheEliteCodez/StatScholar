import STCORE
def event_input(binomial=False):
    key = STCORE.menu("BINOMIAL > EVENT" if binomial else "WHAT DOES IT ASK?", [("1", "EXACTLY ="), ("2", "AT MOST <="),
          ("3", "LESS THAN <"), ("4", "AT LEAST >="), ("5", "MORE THAN >"),
          ("6", "BETWEEN x AND y")] + ([("7", "AT LEAST ONE"), ("8", "NOT =")] if binomial else [("7", "NOT =")]), page_size=6)
    if key == "0": return None
    if binomial and key == "7": return ">=", (1, 1), 0
    if key == "8": key = "7"
    op = {"1": "=", "2": "<=", "3": "<", "4": ">=", "5": ">", "7": "!="}.get(key, "[]")
    a = STCORE.read_exact("VALUE / LOWER: ")
    b = 0
    if key == "6":
        b = STCORE.read_exact("UPPER: ")
        c = STCORE.menu("INCLUDE ENDPOINTS?", [("1", "BOTH [a,b]"), ("2", "NEITHER (a,b)"),
               ("3", "LOWER ONLY [a,b)"), ("4", "UPPER ONLY (a,b]")])
        if c == "0": return None
        op = {"1": "[]", "2": "()", "3": "[)", "4": "(]"}.get(c, "[]")
    return op, a, b
def read_size(prompt, maximum, minimum=1):
    while True:
        n = STCORE.read_int(prompt)
        if minimum <= n <= maximum:
            return n
        print("ENTER " + str(minimum) + ".." + str(maximum))
