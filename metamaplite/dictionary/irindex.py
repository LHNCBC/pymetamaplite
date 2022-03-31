import argparse
from metamaplite.dictionary import paths, extents, postings, Dictionary


class IRIndex:

    def __init__(self, ivfdir, indexname):
        self.indexdir = paths.gen_indexdir(ivfdir)
        self.indexname = indexname

    def get_indexdir(self):
        """ return directory containing index """
        return self.indexdir

    def get_indexname(self):
        """ return name of index """
        return self.indexname

    def lookup(self, term_or_tokens, column):
        """ lookup term in specified column in index"""
        if type(term_or_tokens) is list:
            term = ' '.join(term_or_tokens)
        else:
            term = term_or_tokens
        postingslist = []
        dict = Dictionary(self)
        dictentry = dict.find_entry(column, term)
        if dictentry:
            extentsinst = extents.Extents(self)
            extentlist = extentsinst.get_extents(column, len(term),
                                                 dictentry.address,
                                                 dictentry.numposts)
            postingsinst = postings.Postings(self)
            postingslist = postingsinst.get_postings(extentlist)
        return postingslist


def process0(ivfdir, indexname, column, term, verbose=False):
    """ initial version of process lookup """
    print('process(%s, %s, %s, %s, %s)',
          ivfdir, indexname, column, term, verbose)
    index = IRIndex(ivfdir, indexname)
    dict = Dictionary(index)
    dictentry = dict.find_entry(column, term)
    if dictentry:
        extentsinst = extents.Extents(index)
        extentlist = extentsinst.get_extents(column, len(term),
                                             dictentry.address,
                                             dictentry.numposts)
        postingsinst = postings.Postings(index)
        postingslist = postingsinst.get_postings(extentlist)
        print('postingslist:')
        for posting in postingslist:
            print(posting)
    else:
        print('entry not found for term: %s in column: %s' % (term, column))


def process(ivfdir, indexname, column, term, verbose=False):
    """ current version of process lookup """
    index = IRIndex(ivfdir, indexname)
    postingslist = index.lookup(term, column)
    if postingslist:
        print('postingslist:')
        for posting in postingslist:
            print(posting)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="test dictionary reading.")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument('ivfdir', help='ivfdir')
    parser.add_argument('indexname', help='indexname')
    parser.add_argument('column', help='column')
    parser.add_argument('term', nargs="+", help='term')
    args = parser.parse_args()
    process(args.ivfdir,
            args.indexname,
            args.column,
            ' '.join(args.term),
            args.verbose)
