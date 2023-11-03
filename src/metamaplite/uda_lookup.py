""" User defined acronym augmented dictionary index lookup proxy. """


class UDALookup:

    def __init__(self, index, global_uda_dict={}):
        """Initialize UA proxy using lookup index instance."""
        self.index = index
        self.uda_dict = global_uda_dict

    def lookup(self, term, column):
        """Lookup term in index column, if term is in cache, then use cached
           version.  Otherwise, look up term in index, add it to the
           cache, and return it. """
        if term in self.uda_dict:
            result = self.index.lookup(self.uda_dict[term], column)
        else:
            result = self.index.lookup(term, column)
        return result
