"""
The postings for all of the partitions reside in the file postings.

address | data
--------+-------------------------------------------------------------------
      0 | C0000039|S0033298|4|Dipalmitoylphosphatidylcholine|SNMI|PT
     58 | C0000039|S0033298|7|Dipalmitoylphosphatidylcholine|LNC|CN
    176 | C0000039|S0033298|6|Dipalmitoylphosphatidylcholine|SNOMEDCT_US|OAP
    279 | C0000039|S0033298|5|Dipalmitoylphosphatidylcholine|NDFRT|SY

The postings file is shared among all of the partitions.

"""
import os.path
import mmap
from metamaplite.dictionary import paths
import logging


class Postings:

    def __init__(self, irindex):
        """initialize postings instance """
        self.irindex = irindex
        self.postingsarray = None

    def get_postings(self, extentlist):
        """ return list of postings references by  extents list."""
        postingslist = []
        postingsfn = paths.gen_postingsfn(self.irindex.indexdir,
                                          self.irindex.indexname)
        if self.postingsarray is None:
            if os.path.exists(postingsfn):
                postingsfp = open(postingsfn, 'rb')
                self.postingsarray = mmap.mmap(postingsfp.fileno(), 0,
                                               access=mmap.ACCESS_READ)
                postingsfp.close()
            else:
                logging.warn('postings file %s does not exist.', postingsfn)
                return []
        for extent in extentlist:
            postingslist.append(
                str(self.postingsarray[extent.start:extent.start+extent.length],
                    encoding='utf-8'))
        return postingslist
