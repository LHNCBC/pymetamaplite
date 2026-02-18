"""A most recently used cache based file pointer manager for systems
with limited resources."""


class MRU_FileManager(object):
    """An attempt a faster implementation of create_temporary_tables
    using MRU queue of file objects"""
    def __init__(self, args):
        # super(ClassName, self).__init__()
        self.args = args
        self.file_pointer_dict = {}
        self.cache = []
        self.max = 20       # allow 20 file pointer to be open

    def set_cache_size(self, size):
        """set maximum size of mru cache"""
        self.max = size

    def add(self, key):
        "Add key to cache."
        # if present, remove references to key in cache
        indexlist = []
        for index in range(len(self.cache)):
            if key == self.cache[index]:
                indexlist.append(index)
        # remove any copies of this key in cache
        for index in indexlist:
            del self.cache[index]
        if len(self.cache) >= self.max:
            # if queue larger than max then close file pointer
            # of first item in queue and delete it from
            # file_pointer_dict and cache
            if self.cache[0] in self.file_pointer_dict:
                if self.file_pointer_dict[self.cache[0]] is not None:
                    if self.cache[0] != key:
                        self.file_pointer_dict[self.cache[0]].close()
                    del self.file_pointer_dict[self.cache[0]]
                    del self.cache[0]
        self.cache.append(key)

    def open(self, filename, mode, encoding='utf-8'):
        """If file is already open, return open file pointer and
        update mru cache, otherwise open file, save file pointer to
        file pointer dictionary and update mru cache."""
        if filename in self.file_pointer_dict:
            chan = self.file_pointer_dict[filename]
        else:
            chan = open(filename, mode, encoding=encoding)
            self.file_pointer_dict[filename] = chan
        self.add(filename)
        return chan

    def close(self):
        """ close all open resources """
        for chan in self.file_pointer_dict.values():
            chan.close()
        self.file_pointer_dict = {}
        self.cache = []
