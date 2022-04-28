"""bytes to integer and integer to byte conversion functions

For python 3.2 and greater use int.from_bytes instead of bytes_to_int
and int.to_bytes instead of int_to_bytes.  The python implementation
is 4 times faster than this one.

"""


def bytes_to_int(bytes):
    "convert bytes to integer"
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result


def int_to_bytes(value, length, byteorder='little'):
    "convert integer to bytes"
    result = []
    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)
    if byteorder == 'big':
        result.reverse()
    return bytes(result)
