"""A blackboard (not really) actually a dictionary of postings
   offsets keyed by postings checksums."""
import hashlib
from collections import namedtuple

Extent = namedtuple('Extent', ['start', 'length'])


class BlackBoard:

    def __init__(self):
        self.dict = {}

    def record(self, postings_str, start, length):
        digest = hashlib.sha1(postings_str.encode('utf8')).hexdigest()
        if digest not in self.dict:
            self.dict[digest] = Extent(start=start, length=length)

    def present(self, postings_str):
        digest = hashlib.sha1(postings_str.encode('utf8')).hexdigest()
        if digest in self.dict:
            return self.dict[digest]
        return None
