import sys

COMMA = ','
SPACE = ' '


def uninvert(s):
    """
    Recursively uninverts a string.
    I.E.:

        injury, abdominal ==> abdominal injury

    Translated directly from uninvert(s,t) in lex.c.

    @param s INPUT: string "s" containing the term to be uninverted.
    @return OUTPUT: string containing the uninverted string.

    """
    if s is '':
        return s
    sp = s.find(COMMA)
    while sp > 0:
        cp = sp
        cp += 1
        if cp < len(s) and s[cp] == SPACE:
            while cp < len(s) and s[cp] == SPACE:
                cp += 1
            return uninvert(s[cp:]) + " " + s[0:sp].strip()
        else:
            sp += 1
        sp = s.find(COMMA, sp)
    return s.strip()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print('%s -> %s' % (sys.argv[1], uninvert(sys.argv[1])))
