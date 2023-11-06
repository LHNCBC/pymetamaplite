""" Front end for index builder. """
import argparse
import os
from metamaplite.index.config import read_ifconfig
from metamaplite.index.postings_blackboard import BlackBoard
from metamaplite.index import build_index


def build_indexes(ivfdir, sep='|'):
    """Build the set on indexes specified in configuration file
       (tables/ifconfig)"""
    config = read_ifconfig('{}/tables/ifconfig'.format(ivfdir))
    if not os.path.exists('{}/indices'.format(ivfdir)):
        os.mkdir('{}/indices'.format(ivfdir))
    # create temporary table grouped by term length
    items = list(config.items())
    pbb = BlackBoard()
    for indexname, entry in items:
        build_index(ivfdir, indexname, entry, sep=sep, pbb=pbb)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""Build indices using flat files.""")
    parser.add_argument('ivfdir',
                        help='inverted file directory')
    args = parser.parse_args()
    build_indexes(args.ivfdir)
