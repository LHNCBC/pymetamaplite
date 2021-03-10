""" Token list utilities """


def apply_head_subtokenlist_opt(list_of_tokenlists, tokenlist):
    """Create sequence of sublists of tokenlist always starting from the
    head each sublist smaller than the previous and add it to list of
    tokenlists.
    """
    indices = [x for x in range(len(tokenlist))]
    indices.reverse()
    for i in indices:
        token_sublist = tokenlist[0:i+1]
        list_of_tokenlists.append(token_sublist)
    return list_of_tokenlists


def create_sublists_opt(tokenlist):
    """Generate token sublists from original list using successive heads
    of original list.

    """
    list_of_tokenlists = []
    for i in range(len(tokenlist)):
        apply_head_subtokenlist_opt(
            list_of_tokenlists, tokenlist[i:len(tokenlist)])
    return list_of_tokenlists


