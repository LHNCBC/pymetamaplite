""" Purpose:  MetaMap tokenization routines

  includes implementation of tokenize_text_utterly """


def lex_word(text):
    token = text[0]
    i = 1
    if i < len(text):
        ch = text[i]
        # while (ch.isalpha() | ch.isdigit() | (ch == "'")) &
        #       (i < len(text)):
        while (ch.isalpha() | ch.isdigit()) & (i < len(text)):
            token = token + ch
            i += 1
            if i < len(text):
                ch = text[i]
    return token, text[i:]


def tokenize_text_utterly(text):
    tokens = []
    rest = text
    try:
        ch = rest[0]
        while rest != '':
            if ch.isalpha():
                token, rest = lex_word(rest)
                tokens.append(token)
            else:
                tokens.append(ch)
                rest = rest[1:]
            if rest != '':
                ch = rest[0]
        return tokens
    except IndexError as e:
        print("%s: %s" % (e, text))

# tokenize_text_utterly('For 8-bit strings, this method is locale-dependent.')


def is_ws_word(astring):
    return astring.isalnum() & (len(astring) > 1)


def ends_with_s(astring):
    return astring[-1] == 's'
