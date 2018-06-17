import itertools

REPLACE = { letter: str(index) for index, letter in enumerate('oizeasgtb') }

def leet2Combos(word):
    possibles = []
    for l in word.lower():
        ll = REPLACE.get(l, l)
        possibles.append( (l,) if ll == l else (l, ll) )
    return [ ''.join(t) for t in itertools.product(*possibles) ]

with open('wordlistVar.txt', 'w+') as w:
    with open('wordlist.txt', 'r') as f:
        for word in f:
            for var in list(map(''.join, itertools.product(*((c.upper(), c.lower()) for c in word)))):
                w.write(var)
                for leet in leet2Combos(var):
                    w.write(leet)


