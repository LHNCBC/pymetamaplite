""" a match is of the form:
   Term('text', 'start', 'end', 'postings')

"""
from collections import namedtuple
from metamaplite import postings_utils

NewTerm = namedtuple('NewTerm', ['text', 'start', 'end', 'postings'])


def add_semantic_types(mminst, resultlist):
    newresultlist = []
    for item in resultlist:
        postings = postings_utils.add_semantic_types(mminst, item.postings)
        newresultlist.append(NewTerm(text=item.text,
                                     start=item.start,
                                     end=item.end,
                                     postings=postings))
    return newresultlist
