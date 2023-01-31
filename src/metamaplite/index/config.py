""" Configuration file reader function. """
from collections import namedtuple

ConfigEntry = namedtuple('ConfigEntry', ['tablefilename', 'indexname',
                                         'num_fields', 'columnlist',
                                         'column_names', 'column_types'])


def read_ifconfig(filename):
    config = {}
    with open(filename) as chan:
        for line in chan.readlines():
            fields = line.strip().split('|')
            tablefname, indexname, num_fields_str, columnliststr = fields[0:4]
            num_fields = int(num_fields_str)
            columnlist = [int(x) for x in columnliststr.split(',')]
            column_names = fields[4:4+num_fields]
            column_types = fields[4+num_fields:4+num_fields+num_fields]
            config[indexname] = ConfigEntry(tablefilename=tablefname,
                                            indexname=indexname,
                                            num_fields=int(num_fields),
                                            columnlist=columnlist,
                                            column_names=column_names,
                                            column_types=column_types)
    return config
