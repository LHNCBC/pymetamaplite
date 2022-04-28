""" Semantic type lookup using Inverted File Index """

# from dictionary.irindex import IRIndex
# stindexname = "cuist"
# stindex = IRIndex(ivfdir, stindexname)
# stcolumn = 0
# semtypes = list_semantic_types(stindex, 'C0032285')


def has_semantic_type(stindex, cui, semantictypeset):
    """Does the supplied cui have a record with a semantic type in
       supplied semantic type set?"""
    inset = False
    for record in stindex.lookup(cui, 0):
        if record.split('|')[1] in semantictypeset:
            inset = True
    return inset


def list_semantic_types(stindex, cui):
    """Does the supplied cui have a record with a semantic type in
       supplied semantic type set?"""
    semtypes = []
    for record in stindex.lookup(cui, 0):
        fields = record.split('|')
        if len(fields) > 1:
            semtypes.append(fields[1])
    return semtypes
