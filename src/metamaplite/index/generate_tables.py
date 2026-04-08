"""A program which generates three tables: cuiconcept.txt,
cuisourceinfo.txt, and cuist.txt """
import argparse
import os
from metamaplite.index import extract_mrconso_preferred_names
from metamaplite.index import extract_mrconso_sources
from metamaplite.index import extract_mrsty_semantic_types
from metamaplite.index import extract_treecodes
from metamaplite.index import generate_variants


def create_tables(mrconsofilename, mrstyfilename, mrsatfilename, ivfdir,
                  verbose=False):
    """Create MetaMapLite Tables from MRCONSO.RRF and MRSTY.RRF UMLS files."""
    if verbose:
        print("Creating tables from:\nmrconso: {}\nmrsty: {}".format(
            mrconsofilename, mrstyfilename))
    cuiconceptfilename = "{}/tables/cuiconcept.txt".format(ivfdir)
    extract_mrconso_preferred_names.create_table(
        mrconsofilename, cuiconceptfilename, "ENG", True, "RRF")
    cuisourceinfofilename = "{}/tables/cuisourceinfo.txt".format(ivfdir)
    extract_mrconso_sources.create_table(
        mrconsofilename, cuisourceinfofilename, True, True, "ENG", True, "RRF")
    cuisemantictypesfilename = "{}/tables/cuist.txt".format(ivfdir)
    extract_mrsty_semantic_types.create_table(
        mrstyfilename, cuisemantictypesfilename, True, "RRF", None)
    meshtreecodesfilename = "{}/tables/mesh_tc_relaxed.txt".format(ivfdir)
    extract_treecodes.create_table(mrconsofilename, mrsatfilename,
                                   meshtreecodesfilename)
    varsfilename = "{}/tables/vars.txt".format(ivfdir)
    generate_variants.create_table(mrconsofilename, varsfilename,
                                   batchsize=400)


def generate_table_config():
    """Generate table configuration: Returns dictionary of dbnames to
    associated configuration fields """
    table_config = {}
    table_config["cuiconcept"] = ['cuiconcept.txt', 'cuiconcept', '2', '0,1',
                                  'cui', 'concept', 'TXT', 'TXT']
    table_config["cuisourceinfo"] = ['cuisourceinfo.txt', 'cuisourceinfo',
                                     '6', '0,1,3', 'cui', 'sui', 'i', 'str',
                                     'src', 'tty', 'TXT', 'TXT', 'INT',
                                     'TXT', 'TXT', 'TXT']
    table_config["cuist"] = ['cuist.txt', 'cuist', '2', '0', 'cui', 'st',
                             'TXT', 'TXT']
    table_config["meshtcrelaxed"] = ['mesh_tc_relaxed.txt', 'meshtcrelaxed',
                                     '2', '0,1', 'mesh', 'tc', 'TXT', 'TXT']
    table_config["vars"] = ['vars.txt', 'vars', '7', '0,2', 'term', 'tcat',
                            'word', 'wcat', 'varlevel', 'history', '', 'TXT',
                            'TXT', 'TXT', 'TXT', 'TXT', 'TXT', 'TXT']
    return table_config


def save_table_config(config_filename, table_config):
    """ Save table configuration file """
    with open(config_filename, 'w') as chan:
        for fieldlist in table_config.values():
            chan.write('{}\n'.format('|'.join(fieldlist)))


def prepare_directories(ivfdir, verbose=False):
    tablesdir = '{}/tables'.format(ivfdir)
    indicesdir = '{}/indices'.format(ivfdir)
    cuiconceptdir = "{}/indices/cuiconcept".format(ivfdir)
    cuisourceinfodir = "{}/indices/cuisourceinfo".format(ivfdir)
    cuistdir = "{}/indices/cuist".format(ivfdir)
    meshtcrelaxeddir = "{}/indices/meshtcrelaxed".format(ivfdir)
    varsdir = "{}/indices/vars".format(ivfdir)
    if verbose:
        print("Preparing directories\n workingdir: {}\n"
              "tablesdir: {}\n"
              " indicesdir: {}\n".format(ivfdir, tablesdir, indicesdir))
    if not os.path.exists(ivfdir):
        os.mkdir(ivfdir)
    if not os.path.exists(tablesdir):
        os.mkdir(tablesdir)
        table_config = generate_table_config()
        save_table_config('{}/ifconfig'.format(tablesdir), table_config)
    if not os.path.exists(indicesdir):
        os.mkdir(indicesdir)
        os.mkdir(cuiconceptdir)
        os.mkdir(cuisourceinfodir)
        os.mkdir(cuistdir)
        os.mkdir(meshtcrelaxeddir)
        os.mkdir(varsdir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='GenerateTables',
        description='generate index tables from UMLS tables')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('umlsdir')
    parser.add_argument('indexdir')
    args = parser.parse_args()
    prepare_directories(args.indexdir, verbose=args.verbose)
    mrconsofilename = '{}/MRCONSO.RRF'.format(args.umlsdir)
    mrstyfilename = '{}/MRSTY.RRF'.format(args.umlsdir)
    mrsatfilename = '{}/MRSAT.RRF'.format(args.umlsdir)
    create_tables(mrconsofilename, mrstyfilename, mrsatfilename,
                  args.indexdir, verbose=args.verbose)
