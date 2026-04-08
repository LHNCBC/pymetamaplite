""" Purpose:  MetaMap tokenization routines

  includes implementation of tokenize_text_utterly """

import string


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


# def remove_possessives(tokens):
#     """ remove_possessives/2 filters out possessives
#         from the results of tokenize_text_utterly/2. """
#     if len(tokens) > 2:
#         if is_ws_word(tokens[0]) & (tokens[1] == "'") & (tokens[2] == "s"):
#             return tokens[0:1] + remove_possessives(tokens[3:])
#         else:
#             return tokens[0:1] + remove_possessives(tokens[1:])
#     elif len(tokens) > 1:
#         if is_ws_word(tokens[0]) & (tokens[1] == "'") &
#             ends_with_s(tokens[0]):
#             return tokens[0:1] + remove_possessives(tokens[2:])
#         else:
#             return tokens[0:1] + remove_possessives(tokens[1:])
#     return tokens


# def remove_possessives(tokens):
#     modtokens=[]
#     for token in tokens:
#         if token[-2:] == "'s":
#             modtokens.append(token[:-2])
#         elif token[-2:] == "s'":
#             modtokens.append(token[:-1])
#         else:
#             modtokens.append(token)
#     return modtokens


# def remove_possessives(tokens):
#     """ remove_possessives/2 filters out possessives
#         from the results of tokenize_text_utterly/2. """
#     if len(tokens) > 1:
#         if is_ws_word(tokens[0]) & (tokens[1] == "'"):
#             if tokens[0].endswith('s'):
#                 return tokens[0:1] + remove_possessives(tokens[2:])
#             elif len(tokens) > 2:
#                 if (tokens[2] == "s"):
#                     return tokens[0:1] + remove_possessives(tokens[3:])
#                 else:
#                     return tokens[0:1] + remove_possessives(tokens[1:])
#             else:
#                 return tokens[0:1] + remove_possessives(tokens[1:])
#         else:
#             return tokens[0:1] + remove_possessives(tokens[1:])
#     return tokens


def is_quoted_string(tokens, i):
    pass


def is_apostrophe_s(tokens, i):
    if i+2 < len(tokens):
        if is_ws_word(tokens[i]) & (tokens[i+1] == "'") & (tokens[i+2] == "s"):
            if i+3 < len(tokens):
                if string.punctuation.find(tokens[i+3][0]) >= 0:
                    return False
            return True
    return False


def is_s_apostrophe(tokens, i):
    if i+1 < len(tokens):
        if is_ws_word(tokens[i]) & tokens[i].endswith('s') & \
           (tokens[i+1] == "'"):
            return True
    return False


def remove_possessives(tokens):
    """ remove_possessives/2 filters out possessives
        from the results of tokenize_text_utterly/2.

    EBNF for possessives using tokenization of original prolog predicates:

    tokenlist -> token tokenlist | possessive tokenlist ;
    quoted_string -> "'" tokenlist "'" ;
    possessive --> apostrophe_s_possessive | s_apostrophe_possessive ;
    apostrophe_s_possessive -> alnum_word "'" "s" ;
    s_apostrophe_possessive -> alnum_word_ending_with_s "'" ;
    """
    i = 0
    newtokens = []
    while i < len(tokens):
        if is_apostrophe_s(tokens, i):
            newtokens.append(tokens[i])
            i += 3
        elif is_s_apostrophe(tokens, i):
            newtokens.append(tokens[i])
            i += 2
        else:
            newtokens.append(tokens[i])
            i += 1
    return newtokens


def strip_possessives(astring):
    """ strip_possessives/2 tokenizes String, uses
    metamap_tokenization:remove_possessives/2, and then rebuilds
    StrippedString. """
    tokens = tokenize_text_utterly(astring)
    stripped_tokens = remove_possessives(tokens)
    if tokens == stripped_tokens:
        return astring
    else:
        return ''.join(stripped_tokens)


# def strip_possessives(astring):
    # if astring.find("''s") >= 0:
    #     rstring2 = astring.replace("''s","|dps|")
    #     rstring1 = rstring2.replace("'s","")
    #     rstring0 = rstring1.replace("|dps|","''s")
    # else:
    #     rstring0 = astring.replace("'s","")
    # return rstring0.replace("s'","s")


def remove_possessives_and_nonwords(sequence):
    if sequence is str:
        text = sequence
        if is_ws_word(text):
            return remove_possessives(text)
        return text
    else:
        tokenlist = sequence
        newtokenlist = []
        for token in tokenlist:
            if is_ws_word(token):
                newtokenlist.append(remove_possessives(token))
        return newtokenlist


def tokenize_text_mm(text):
    string_tokens_0 = tokenize_text_utterly(text)
    return [''.join(token)
            for token in remove_possessives_and_nonwords(string_tokens_0)]
