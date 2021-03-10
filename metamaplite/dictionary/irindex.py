import argparse
import logging
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
        logging.debug('lookup("%s", %s)', term_or_tokens, column)
        if isinstance(term_or_tokens, list):
            term = ' '.join(term_or_tokens)
        else:
            term = term_or_tokens
        postingslist = []
        dict = Dictionary(self)
        logging.debug('find_entry("%s", %s)', column, term)
        dictentry = dict.find_entry(column, term)
        if dictentry:
            logging.debug('bs found: %s %s %s' % dictentry)
            extentsinst = extents.Extents(self)
            extentlist = extentsinst.get_extents(column, len(term),
                                                 dictentry.address,
                                                 dictentry.numposts)
            logging.debug('extents: %s' % extentlist)
            postingsinst = postings.Postings(self)
            postingslist = postingsinst.get_postings(extentlist)
            logging.debug('postingslist: %s' % postingslist)
        return postingslist


def process0(ivfdir, indexname, column, term, verbose=False):
    """ initial version of process lookup """
    logging.debug('process(%s, %s, %s, %s, %s)',
                  ivfdir, indexname, column, term, verbose)
    index = IRIndex(ivfdir, indexname)
    # found = []
    # for entry in index.list_entries(column, len(term)):
    #     if entry.term == term.encode('utf-8'):
    #         found.append(entry)
    #     print(entry)
    # print('found: %s' % found)
    dict = Dictionary(index)
    dictentry = dict.find_entry(column, term)
    if dictentry:
        logging.debug('dictionary entry: %s %s %s' % dictentry)
        extentsinst = extents.Extents(index)
        extentlist = extentsinst.get_extents(column, len(term),
                                             dictentry.address,
                                             dictentry.numposts)
        logging.debug('extents: %s' % extentlist)
        postingsinst = postings.Postings(index)
        postingslist = postingsinst.get_postings(extentlist)
        print('postingslist:')
        for posting in postingslist:
            print(posting)
    else:
        print('entry not found for term: %s in column: %s' % (term, column))


def process(ivfdir, indexname, column, term, verbose=False):
    """ current version of process lookup """
    logging.debug('process(%s, %s, %s, %s, %s)',
                  ivfdir, indexname, column, term, verbose)
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
