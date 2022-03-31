""" byte array based binary search

File organization:

The file *cuisourceinfo-3-30-term-dictionary* is a binary file of
records, all the same length with each record containing a term, the
number of postings for that term and address of the posting extents
for that term:

    |       term in bytes          | # of postings | address |
    +------------------------------+---------------+---------+
    |Dipalmitoylphosphatidylcholine|       4       | FFF4556 |

"""

from collections import namedtuple

DictionaryEntry = namedtuple('DictionaryEntry', ['term', 'numposts',
                                                 'address'])


def binary_search(dictarray, word, wordlen, datalen, numrecs):
    low = 0
    high = numrecs
    mid = 0
    while low < high:
        mid = int(low + (high - low) / 2)
        address = int(mid * (wordlen + datalen))
        testword = dictarray[address:address+wordlen].lower()
        if word < testword:
            high = mid
        elif word > testword:
            low = mid + 1
        else:
            count = dictarray[address+wordlen:address+wordlen+8]
            address = dictarray[address+wordlen+8:address+wordlen+16]
            return DictionaryEntry(str(word, encoding='utf-8'),
                                   int.from_bytes(count, 'big'),
                                   int.from_bytes(address, 'big'))
    return None
