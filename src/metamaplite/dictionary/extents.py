"""
The file *cuisourceinfo-3-30-partition-offsets* is a binary file that
contains the start and end offsets (the extent) of each posting:

    | address | start |  len  |
    +---------+-------+-------+
    | FFF4556 |   58  |   57  |
    |   ...   |  176  |   66  |
    |   ...   |  279  |   59  |
    |   ...   |    0  |   58  |

Defined in irutils.MultiKeyIndex.Extent (irutils/MultiKeyIndex.java):

    class Extent {
      /** address of posting */
      long start;
      /** length of posting */
      long end;
    }

see postings.py

"""

import os.path
from collections import namedtuple
import mmap
import logging
from metamaplite.dictionary import paths

ExtentEntry = namedtuple('ExtentEntry', ['start', 'length'])


class Extents:

    def __init__(self, irindex):
        """ initialize extents instance """
        self.irindex = irindex
        self.extents_dict = {}

    def get_extents(self, column, termlength, offset, count):
        """Return count extents starting at offset."""
        logging.debug('column: %s, termlength: %s, offset: %s, count: %s',
                      column, termlength, offset, count)
        extentslist = []
        extentfn = paths.gen_extentsfn(self.irindex.indexdir,
                                       self.irindex.indexname,
                                       column,
                                       termlength)
        logging.debug('extents filename: %s, path exists: %s',
                      extentfn, os.path.exists(extentfn))
        if (column, termlength) in self.extents_dict:
            extentsarray = self.extents_dict[(column, termlength)]
        else:
            if os.path.exists(extentfn):
                extentsfp = open(extentfn, 'rb')
                extentsarray = mmap.mmap(extentsfp.fileno(), 0,
                                         access=mmap.ACCESS_READ)
                self.extents_dict[(column, termlength)] = extentsarray
                extentsfp.close()
            else:
                logging.warn('extents file %s does not exist.', extentfn)
                return []
        logging.debug('start: %d, end: %d, step: %d',
                      offset, offset+(count*16), 16)
        for i in range(offset, offset+(count*16), 16):
            start = int.from_bytes(extentsarray[i:i+8], 'big')
            length = int.from_bytes(extentsarray[i+8:i+16], 'big')
            logging.debug('start: %s, length: %s', start, length)
            extentslist.append(ExtentEntry(start=start, length=length))
        return extentslist
