""" bytes to integer and integer to byte conversion functions """


def bytes_to_int(bytes):
    "convert bytes to integer"
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result


def int_to_bytes(value, length):
    "convert integer to bytes"
    result = []
    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)
    result.reverse()
    return result
