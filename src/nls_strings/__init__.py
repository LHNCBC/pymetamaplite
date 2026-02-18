"""
File:     nls_strings/__init__.py (formally: nls_strings.py)
Module:   NLS Strings
Author:   Lan (translated to Python by Willie Rogers
Purpose:  Provide miscellaneous string manipulation routines.
Source:   strings_lra.pl
"""
from nls_strings import lex
import sys
from nls_strings.metamap_tokenization import tokenize_text_utterly


def normalized_syntactic_uninvert_string(pstring):
    """ normalized version of uninverted string. """
    normstring = normalize_string(pstring)
    normuninvstring = syntactic_uninvert_string(normstring)
    return normuninvstring


def normalize_string(astring):
    """ Normalize string. Elminate multiple meaning designators and
    "NOS" strings.  First eliminates multiple meaning designators
    (<n>) and then eliminates all forms of NOS. """
    string1 = eliminate_multiple_meaning_designator_string(astring)
    norm_string = eliminate_nos_string(string1)
    if norm_string.strip() != '':
        return norm_string
    else:
        return astring


def eliminate_multiple_meaning_designator_string(astring):
    """ Remove multiple meaning designators; method removes an expression
    of the form <n> where n is an integer from input string.  The modified
    string is returned. """
    try:
        if (astring.find('<') >= 0) & (astring.find('>') > astring.find('<')):
            if astring[astring.find('<') + 1:astring.find('>')].isdigit():
                return (astring[0:astring.index('<')] +
                        eliminate_multiple_meaning_designator_string
                        (astring[astring.index('>')+1:]).strip())
            else:
                return astring
        else:
            return astring
    except ValueError as e:
        sys.stderr.write('%s: astring="%s"\n' % (e, astring))
        sys.exit()


def eliminate_nos_string(astring):
    """ Eliminate NOS String if present. """
    norm_string0 = eliminate_nos_acros(astring)
    return eliminate_nos_expansion(norm_string0).lower()


nos_strings = [
    ", NOS",
    " - NOS",
    " NOS",
    ".NOS",
    " - (NOS)",
    " (NOS)",
    "/NOS",
    "_NOS",
    ",NOS",
    "-NOS",
    ")NOS"
]
# "; NOS",


def eliminate_nos_acros(astring):

    # split_string_backtrack(String,"NOS",Left,Right),
    charindex = astring.find("NOS")
    if charindex >= 0:
        left = astring[0:max(charindex, 0)]
        right = astring[charindex+3: max(charindex+3, len(astring))]
        if ((right != '') and
            right[0].isalnum()) and ((left != '') and
                                     left[len(left)-1].isalpha()):
            charindex = astring.find("NOS", charindex+1)
            if charindex == -1:
                return astring

    for nos_string in nos_strings:
        charindex = astring.find(nos_string)
        if charindex >= 0:
            left2 = astring[0: max(charindex, 0)]
            right2 = astring[charindex+len(nos_string):max
                             (charindex+len(nos_string), len(astring))]

            if nos_string == ")NOS":
                return eliminate_nos_acros(left2 + ")" + right2)
            elif nos_string == ".NOS":
                return eliminate_nos_acros(left2 + "." + right2)
            elif (nos_string == " NOS"):
                if right2 != '':
                    if right2[0].isalnum():
                        return left2 + " NOS" + eliminate_nos_acros(right2)
                if not abgn_form(astring[charindex+1:]):
                    return eliminate_nos_acros(left2 + right2)
            elif nos_string == "-NOS":
                return eliminate_nos_acros(left2 + right2)
            else:
                return eliminate_nos_acros(left2 + right2)
    return astring


abgn_forms = set([
    "ANB-NOS",
    "ANB NOS",
    "C NOS",
    "CL NOS",
    # is this right?
    # C0410315|ENG|s|L0753752|PF|S0970087|Oth.inf.+bone dis-NOS|
    "NOS AB",
    "NOS AB:ACNC:PT:SER^DONOR:ORD:AGGL",
    "NOS-ABN",
    "NOS ABN",
    "NOS-AG",
    "NOS AG",
    "NOS ANB",
    "NOS-ANTIBODY",
    "NOS ANTIBODY",
    "NOS-ANTIGEN",
    "NOS ANTIGEN",
    "NOS GENE",
    "NOS NRM",
    "NOS PROTEIN",
    "NOS-RELATED ANTIGEN",
    "NOS RELATED ANTIGEN",
    "NOS1 GENE PRODUCT",
    "NOS2 GENE PRODUCT",
    "NOS3 GENE PRODUCT",
    "NOS MARGN",
])


def abgn_form(astr):
    """
    Determine if a pattern of the form: "NOS ANTIBODY", "NOS AB", etc.
    exists.  if so return true.
    """
    return astr in abgn_forms


def syntactic_uninvert_string(astring):
    """ invert strings of the form "word1, word2" to "word2 word1"
        if no prepositions or conjunction are present.

        syntactic_uninvert_string calls lex.uninvert on String if it
        contains ", " and does not contain a preposition or
        conjunction."""
    if contains_prep_or_conj(astring):
        return astring
    else:
        return lex.uninvert(astring)


prep_or_conj = set([
    # init preposition and conjunctions
    "aboard",
    "about",
    "across",
    "after",
    "against",
    "aka",
    "albeit",
    "along",
    "alongside",
    "although",
    "amid",
    "amidst",
    "among",
    "amongst",
    "and",
    # "anti",
    "around",
    "as",
    "astride",
    "at",
    "atop",
    # "bar",
    "because",
    "before",
    "beneath",
    "beside",
    "besides",
    "between",
    "but",
    "by",
    "circa",
    "contra",
    "despite",
    # "down",
    "during",
    "ex",
    "except",
    "excluding",
    "failing",
    "following",
    "for",
    "from",
    "given",
    "if",
    "in",
    "inside",
    "into",
    "less",
    "lest",
    # "like",
    # "mid",
    "minus",
    # "near",
    "nearby",
    "neath",
    "nor",
    "notwithstanding",
    "of",
    # "off",
    "on",
    "once",
    # "only",
    "onto",
    "or",
    # "out",
    # "past",
    "pending",
    "per",
    # "plus",
    "provided",
    "providing",
    "regarding",
    "respecting",
    # "round",
    "sans",
    "sensu",
    "since",
    "so",
    "suppose",
    "supposing",
    "than",
    "though",
    "throughout",
    "to",
    "toward",
    "towards",
    "under",
    "underneath",
    "unless",
    "unlike",
    "until",
    "unto",
    "upon",
    "upside",
    "versus",
    "vs",
    "w",
    "wanting",
    "when",
    "whenever",
    "where",
    "whereas",
    "wherein",
    "whereof",
    "whereupon",
    "wherever",
    "whether",
    "while",
    "whilst",
    "with",
    "within",
    "without",
    # "worth",
    "yet",
])


def contains_prep_or_conj(astring):
    for token in tokenize_text_utterly(astring):
        if token in prep_or_conj:
            return True
    return False


nos_expansion_string = [
    ", not otherwise specified",
    "; not otherwise specified",
    ", but not otherwise specified",
    " but not otherwise specified",
    " not otherwise specified",
    ", not elsewhere specified",
    "; not elsewhere specified",
    " not elsewhere specified",
    "not elsewhere specified"
]


def eliminate_nos_expansion(astring):
    """ Eliminate any expansions of NOS """

    lcString = astring.lower()
    for expansion in nos_expansion_string:
        charindex = lcString.find(expansion)
        if charindex == 0:
            return eliminate_nos_expansion(lcString[len(expansion):])
        elif charindex > 0:
            return eliminate_nos_expansion(lcString[0:charindex] +
                                           lcString[charindex +
                                                    len(expansion):])
    return astring
