"""python implementation for metamaplite dictionaries

File organization:

The file *cuisourceinfo-3-30-term-dictionary* is a binary file of
records, all the same length with each record containing a term, the
number of postings for that term and address of the posting extents
for that term:

    |            term              | # of postings | address |
    +------------------------------+---------------+---------+
    |Dipalmitoylphosphatidylcholine|       4       | FFF4556 |

See extents.py for information on extents file
*cuisourceinfo-3-30-partition-offsets*.

"""

from collections import namedtuple

import mmap
import os.path
from metamaplite.dictionary import paths
import logging
from metamaplite.byteutils import bytes_to_int
from metamaplite.dictionary.binary_search import binary_search, DictionaryEntry


DictionaryStats = namedtuple('DictionaryStats', ['termlength', 'reclength',
                                                 'datalength', 'recordnum'])


def load_stats(statsfn):
    "load information about partition"
    stats_dict = {}
    fp = open(statsfn)
    for l in fp.readlines():
        fields = l.strip().split('|')
        stats_dict[fields[0]] = int(fields[1])
    fp.close()
    return DictionaryStats(termlength=int(stats_dict['termlength']),
                           reclength=int(stats_dict['reclength']),
                           datalength=int(stats_dict['datalength']),
                           recordnum=int(stats_dict['recordnum']))


class Dictionary:

    def __init__(self, irindex):
        self.irindex = irindex
        # stats for partitions of termlength
        self.statsfn = {}
        self.stats_dict = {}
        self.dictfn_dict = {}
        self.mmaparray_dict = {}

    def list_entries(self, column, termlength):
        "list all entries in dictionary partition"
        logging.debug('list_entries(%s, %s)', column, termlength)
        elements = []
        if not (column, termlength) in self.statsfn:
            self.statsfn[(column, termlength)] = paths.gen_statsfn(
                self.irindex.indexdir,
                self.irindex.indexname,
                column,
                termlength)
        logging.debug('statsfn: %s, path exists: %s',
                      self.statsfn[(column, termlength)],
                      os.path.exists(self.statsfn[(column, termlength)]))
        if (column, termlength) in self.stats_dict:
            stats_dict = self.stats_dict[(column, termlength)]
        else:
            if os.path.exists(self.statsfn[(column, termlength)]):
                self.stats_dict[(column, termlength)] = load_stats
                (self.statsfn[(column, termlength)])
                stats_dict = self.stats_dict[(column, termlength)]
        logging.debug('stats: %s', stats_dict)
        if (column, termlength) in self.dictfn_dict:
            dictfn = self.dictfn_dict[(column, termlength)]
        else:
            dictfn = paths.gen_dictionaryfn(self.irindex.indexdir,
                                            self.irindex.indexname,
                                            column, termlength)
            self.dictfn_dict[(column, termlength)] = dictfn
        if dictfn in self.mmaparray_dict:
            dictarray = self.mmaparray_dict[dictfn]
        else:
            dictfp = open(dictfn)
            dictarray = mmap.mmap(dictfp.fileno(), 0,
                                  access=mmap.ACCESS_READ)
            self.mmaparray_dict[dictfn] = dictarray
            dictfp.close()
        for i in range(
                0,
                stats_dict.reclength * stats_dict.recordnum,
                stats_dict.reclength):
            elements.append(DictionaryEntry(
                term=dictarray[i:i+stats_dict.termlength],
                numposts=bytes_to_int(
                    dictarray[i+stats_dict.termlength:
                              i+stats_dict.termlength+8]),
                address=bytes_to_int(
                    dictarray[i+stats_dict.termlength+8:
                              i+stats_dict.reclength])))
            logging.debug('%d: %s', i, elements[-1])
        return elements

    def find_entry(self, column, term):
        "find entry in dictionary"
        # partition term length must be in bytes
        termlength = len(term.lower().encode('utf-8'))
        if not (column, termlength) in self.statsfn:
            self.statsfn[(column, termlength)] = paths.gen_statsfn(
                self.irindex.indexdir,
                self.irindex.indexname,
                column,
                termlength)
        logging.debug('statsfn: %s, path exists: %s',
                      self.statsfn[(column, termlength)],
                      os.path.exists(self.statsfn[(column, termlength)]))

        if (column, termlength) in self.stats_dict:
            stats_dict = self.stats_dict[(column, termlength)]
        else:
            if os.path.exists(self.statsfn[(column, termlength)]):
                self.stats_dict[(column, termlength)] = load_stats(
                    self.statsfn[(column, termlength)])
                stats_dict = self.stats_dict[(column, termlength)]
            else:
                stats_dict = {}
        logging.debug('stats: %s', stats_dict)

        if (column, termlength) in self.dictfn_dict:
            dictfn = self.dictfn_dict[(column, termlength)]
        else:
            dictfn = paths.gen_dictionaryfn(self.irindex.indexdir,
                                            self.irindex.indexname,
                                            column, termlength)
            self.dictfn_dict[(column, termlength)] = dictfn
        if os.path.exists(dictfn):
            if dictfn in self.mmaparray_dict:
                dictarray = self.mmaparray_dict[dictfn]
            else:
                dictfp = open(dictfn)
                dictarray = mmap.mmap(dictfp.fileno(), 0,
                                      access=mmap.ACCESS_READ)
                self.mmaparray_dict[dictfn] = dictarray
                dictfp.close()

            word = term.lower().encode('utf-8')
            return binary_search(dictarray, word, len(word),
                                 stats_dict.datalength,
                                 stats_dict.recordnum)
        return None
