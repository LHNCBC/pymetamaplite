""" find longest match """

from metamaplite.find_longest_match import token_list_utils


def always(tokenlist):
    """ always return true """
    return True


def find_longest_match(tokenlist, lookup_func, token_filter_func=always):
    """Given Example:
    "Papillary Thyroid Carcinoma is a Unique Clinical Entity."

 Check the following:
    "Papillary Thyroid Carcinoma is a Unique Clinical Entity"
    "Papillary Thyroid Carcinoma is a Unique Clinical"
    "Papillary Thyroid Carcinoma is a Unique"
    "Papillary Thyroid Carcinoma is a"
    "Papillary Thyroid Carcinoma is"
    "Papillary Thyroid Carcinoma"
    "Papillary Thyroid"
    "Papillary"
              "Thyroid Carcinoma is a Unique Clinical Entity"
              "Thyroid Carcinoma is a Unique Clinical"
              "Thyroid Carcinoma is a Unique"
              "Thyroid Carcinoma is a"
              "Thyroid Carcinoma is"
              "Thyroid Carcinoma"
              "Thyroid"
    ...
    Parameters:

      tokenlist: tokenlist of document or sentence, phrase, or other
                 text segment.

      token_start_filter: function to determine if firost token in
                          sublist is valid for lookup, usually
                          determined by part of speech

      lookup_func: dictionary lookup function

    tokenlist is a list of tokens of the form:

         (text, span, character-class, part-of-speech)

    """
    term_info_list = []
    list_of_tokensublists = token_list_utils.create_sublists_opt(tokenlist)
    # print('length of list of tokensublists: %d' % len(list_of_tokensublists))
    # print(render_list_of_lists(list_of_tokensublists))
    for tokensublist in list_of_tokensublists:
        if token_filter_func(tokensublist):
            term_info = lookup_func(tokensublist)
            if term_info:
                term_info_list.append((tokensublist, term_info))
    # print('length of list of term_info_list: %d' % len(term_info_list))
    return term_info_list
