"""
'cui|sui|idx|str|src|termtype'
'C0030705|S0071331|7|Patient|MSH|PM'
"""
from collections import namedtuple

Posting = namedtuple('Posting', ['cui', 'sui',  'idx', 'str', 'src',
                                 'termtype'])
PostingSTS = namedtuple('PostingSTS', ['cui', 'sui', 'idx', 'str', 'src',
                                       'termtype', 'semtypeset'])


def strings2tuple(postingslist):
    """ convert posting strings to namedtuples of Posting. """
    newpostinglist = []
    for result in postingslist:
        fields = result.split('|')
        newpostinglist.append(Posting(cui=fields[0],
                                      sui=fields[1],
                                      idx=fields[2],
                                      str=fields[3],
                                      src=fields[4],
                                      termtype=fields[5]))
    return newpostinglist


def add_semantic_types(mminst, postingslist):
    """ add semantic types for each concept to postings list """
    newpostinglist = []
    for result in postingslist:
        fields = result.split('|')
        semtypeset = mminst.get_semantic_types(fields[0])
        newpostinglist.append(PostingSTS(cui=fields[0],
                                         sui=fields[1],
                                         idx=fields[2],
                                         str=fields[3],
                                         src=fields[4],
                                         termtype=fields[5],
                                         semtypeset=semtypeset))
    return newpostinglist
