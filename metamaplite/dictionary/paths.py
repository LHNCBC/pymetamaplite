""" paths and path generators """
# workarea = '/net/lhcdevfiler/vol/cgsb5/ind/II_Group_WorkArea'
# ivfdir = workarea + '/wjrogers/data/multi-key-index/2017AA/USAbase/strict'


def gen_indexdir(ivfdir):
    """ get indexdir path for ivfdir """
    return '%s/indices' % ivfdir


def gen_tablesdir(ivfdir):
    """ get tablesdir path for ivfdir """
    return '%s/tables' % ivfdir


def gen_statsfn(indexdir, indexname, column, termlength):
    """generate pathname for stats file"""
    return '%s/%s/%s-%s-%s-term-dictionary-stats.txt' % (indexdir,
                                                         indexname,
                                                         indexname,
                                                         column,
                                                         termlength)


def gen_dictionaryfn(indexdir, indexname, column, termlength):
    """generate pathname for dirctionary file"""
    return '%s/%s/%s-%s-%s-term-dictionary' % (indexdir,
                                               indexname,
                                               indexname,
                                               column,
                                               termlength)


def gen_extentsfn(indexdir, indexname, column, termlength):
    """generate pathname for postings extents file"""
    return '%s/%s/%s-%s-%s-postings-offsets' % (indexdir,
                                                indexname,
                                                indexname,
                                                column,
                                                termlength)


def gen_postingsfn(indexdir, indexname):
    """generate pathname for postings file"""
    return '%s/%s/postings' % (indexdir, indexname)
