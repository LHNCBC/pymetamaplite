""" Simple hash based lookup cache """


class SimpleCache:

    def __init__(self, index):
        """Initialize cache using lookup index instance."""
        self.index = index
        self.cache = {}

    def lookup(self, term, column):
        """Lookup term in index column, if term is in cache, then use cached
           version.  Otherwise, look up term in index, add it to the
           cache, and return it. """
        if (term, column) in self.cache:
            return self.cache[(term, column)]
        else:
            result = self.index.lookup(term, column)
            self.cache[(term, column)] = result
            return result
