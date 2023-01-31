"""Index builder implementation library."""

import os
from tqdm import tqdm
from metamaplite.index.mru_file_manager import MRU_FileManager
from metamaplite.index.postings_blackboard import BlackBoard


def create_temporary_tables(ivfdir, config_entry):
    """ build tables for partitions grouped by termlength """
    # temp_<indexname>_
    # temp_<indexname>_
    indexname = config_entry.indexname
    print('building temporary index for {}'.format(indexname))
    tablefilename = config_entry.tablefilename
    mru_inst = MRU_FileManager(None)
    indexname_column_bytelength_set = set([])
    if not os.path.exists('{}/indices/{}'.format(ivfdir, indexname)):
        os.mkdir('{}/indices/{}'.format(ivfdir, indexname))
    with open('{}/tables/{}'.format(ivfdir, tablefilename)) as chan:
        for line in tqdm(chan.readlines()):
            fields = line.split('|')
            for column in config_entry.columnlist:
                textbytes = fields[column].encode('utf-8')
                bytelength = len(textbytes)
                indexname_column_bytelength_set.add(
                    (indexname, column, bytelength))
                postchan = mru_inst.open(
                    '{}/indices/{}/{}-{}-{}-postings.txt'.format(
                        ivfdir, indexname,
                        indexname, column, bytelength), 'a',
                    encoding='utf-8')
                postchan.write('{}\n'.format(line.strip()))
    mru_inst.close()
    return indexname_column_bytelength_set


def write_dictionary_stats(ivfdir, indexname, column, bytelen, recordnum):
    with open(
            '{}/indices/{}/{}-{}-{}-term-dictionary-stats.txt'.format(
                ivfdir, indexname,
                indexname, column, bytelen), 'w') as stats_chan:
        stats_chan.write('termlength|{}\n'.format(bytelen))
        stats_chan.write('reclength|{}\n'.format(bytelen+16))
        stats_chan.write('datalength|{}\n'.format(16))
        stats_chan.write('recordnum|{}\n'.format(recordnum))


def write_posting_and_extent(pbb, postings_chan, extents_chan, line):
    # is posting already present in postings files?
    extent = pbb.present(line.strip())
    if extent is None:
        # write posting to postings file
        posting_start = postings_chan.tell()
        postings_chan.write('{}'.format(line.strip()))
        posting_len = postings_chan.tell() - posting_start
        # write extent of posting to extents file
        extents_chan.write(
            posting_start.to_bytes(8, byteorder='big'))
        extents_chan.write(
            posting_len.to_bytes(8, byteorder='big'))
        pbb.record(line.strip(), posting_start, posting_len)
    else:
        # write extent of posting to extents file
        extents_chan.write(
            extent.start.to_bytes(8, byteorder='big'))
        extents_chan.write(
            extent.end.to_bytes(8, byteorder='big'))


class colkeyfunc:
    """ Generate keyfunc for postings column on-the-fly. """
    def __init__(self, column=0):
        self.column = column

    def keyfunc(self, line):
        fields = line.split('|')
        return fields[self.column].lower()


def build_index(ivfdir, indexname, entry, sep='|', pbb=None):
    """ build index """
    if pbb is None:
        pbb = BlackBoard()
    index_column_bytelen_set = create_temporary_tables(ivfdir, entry)
    print('building final index for {}'.format(indexname))
    # open postings
    with open('{}/indices/{}/postings'.format(ivfdir, indexname),
              'w') as postings_chan:
        # create postings, partition offset files, and term_dictionary
        for indexname, column, bytelen in index_column_bytelen_set:
            recordnum = 0
            with open('{}/indices/{}/{}-{}-{}-postings.txt'.format(
                    ivfdir, indexname,
                    indexname, column, bytelen), 'r') as table_chan, \
                    open('{}/indices/{}/{}-{}-{}-postings-offsets'.format(
                        ivfdir, indexname,
                        indexname, column, bytelen), 'wb') as extents_chan, \
                    open('{}/indices/{}/{}-{}-{}-term-dictionary'.format(
                        ivfdir, indexname,
                        indexname, column, bytelen), 'wb') as dictionary_chan:
                current_term = None
                num_of_postings = 0
                offset_entry_start = 0
                table_lines = [line.strip() for line in table_chan.readlines()]
                table_lines.sort(key=colkeyfunc(column).keyfunc)
                for line in tqdm(table_lines):
                    # should this use normalize_meta_string instead?
                    new_term = line.split(sep)[column].lower()
                    # debug
                    if new_term == 'obstructive sleep apnea':
                        print(line)
                    # end debug
                    if new_term != current_term:
                        if current_term is not None:
                            # write current term info to dictionary file
                            dictionary_chan.write(
                                current_term.encode('utf-8'))
                            dictionary_chan.write(
                                num_of_postings.to_bytes(8,
                                                         byteorder='big'))
                            dictionary_chan.write(
                                offset_entry_start.to_bytes(
                                    8, byteorder='big'))
                            # debug
                            if current_term == 'obstructive sleep apnea':
                                print('write dictionary: {}|{}|{}'.format(
                                    current_term, num_of_postings,
                                    offset_entry_start))
                            # end debug
                            recordnum += 1
                        # initialize term info for new term and
                        # make it the current term
                        current_term = new_term
                        offset_entry_start = extents_chan.tell()
                        num_of_postings = 0
                    write_posting_and_extent(
                        pbb, postings_chan, extents_chan, line)
                    num_of_postings += 1
            write_dictionary_stats(ivfdir, indexname, column,
                                   bytelen, recordnum)
    os.remove('{}/indices/{}/{}-{}-{}-postings.txt'.format(
                        ivfdir, indexname,
                        indexname, column, bytelen))
    return pbb
