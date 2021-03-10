""" filtering results by semantic types or sources """


def explode(postingslist):
    """Split postings records into fields"""
    return [x.split('|') for x in postingslist]


def convert_postings(term_postings_list):
    """ Convert postings in term_postings_list to fields """
    return [(term, explode(postings)) for term, postings in term_postings_list]


def restrict_postings_to_sources(postingslist, sourceset):
    """remove any postings not in sourceset from postings list.  Program
    expects postings to split into fields.  Source identifier is in 4th
    column of postings record.  """
    print('postingslist: %s' % postingslist)
    print('sourceset: %s' % sourceset)
    return [posting for posting in postingslist if posting.split('|')[4] in sourceset]


def restrict_to_sources(term_postings_list, sourcelist):
    """ keep only postings in sourcelist """
    if sourcelist is set:
        sourceset = sourcelist
    else:
        sourceset = set(sourcelist)
    return [(term, restrict_postings_to_sources(postings, sourceset))
            for term, postings in term_postings_list]


def restrict_postings_to_semantic_types(postingslist, semantictypeset,
                                        test_func):
    """remove any postings not in semantic type set from postings list.
    Program expects postings to split into fields.  Semantic Type
    identifier is in 4th column of postings record.

    """
    return [posting for posting in postingslist
            if test_func(posting.split('|')[0], semantictypeset)]


def restrict_to_semantic_types(term_postings_list, semantictypelist,
                               lookup_func):
    """keep only postings in semantic type list, at func must be passed to
    lookup semantic type by cui. """
    if semantictypelist is set:
        semantictypeset = semantictypelist
    else:
        semantictypeset = set(semantictypelist)
    return [(term,
             restrict_postings_to_semantic_types(postings, semantictypeset,
                                                 lookup_func))
            for term, postings in term_postings_list]
