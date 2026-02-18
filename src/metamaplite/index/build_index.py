""" Front end for index builder. """
import argparse
import os
from metamaplite.index.config import read_ifconfig
from metamaplite.index.postings_blackboard import BlackBoard
from metamaplite.index import build_index


def build_indexes(ivfdir, sep='|'):
    """Build the set of indexes specified in configuration file
       (tables/ifconfig) """
    config = read_ifconfig('{}/tables/ifconfig'.format(ivfdir))
    if not os.path.exists('{}/indices'.format(ivfdir)):
        os.mkdir('{}/indices'.format(ivfdir))
    items = list(config.items())
    for indexname, entry in items:
        # create temporary table grouped by term length
        pbb = BlackBoard()
        build_index(ivfdir, indexname, entry, sep=sep, pbb=pbb)


def build_one_index(ivfdir, indexname, sep='|'):
    """Build one of the indexes in the set of indexes specified in
       configuration file (tables/ifconfig) """
    config = read_ifconfig('{}/tables/ifconfig'.format(ivfdir))
    if not os.path.exists('{}/indices'.format(ivfdir)):
        os.mkdir('{}/indices'.format(ivfdir))
    if indexname in config:
        # create temporary table grouped by term length
        entry = config[indexname]
        pbb = BlackBoard()
        build_index(ivfdir, indexname, entry, sep=sep, pbb=pbb)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""Build indices using flat files.""")
    parser.add_argument('-i', '--indexname', default='all',
                        help='build specified index (default: all)')
    parser.add_argument('-s', '--separator', default='|',
                        help='field separator.')
    parser.add_argument('ivfdir', help='inverted file directory')
    args = parser.parse_args()
    if args.indexname == 'all':
        build_indexes(args.ivfdir, sep=args.separator)
    else:
        build_one_index(args.ivfdir, args.indexname, sep=args.separator)
