"""
These are utility functions to parse RESP compliant input
Based on https://redis.io/topics/protocol
"""


def parse_array(array, size):
    """
    Produces a resp compliant array by taking in an array of resp encoded objects
    :param array:
    :param size:
    :return:
    """
    arr = []

    for i in range(0, len(array), 2):
        if command_map.get(array[i][0]) is not None:
            arr.append(command_map.get(array[i][0])(array[i:i+2]))
        else:
            print(array[i])

    return arr


def parse_simple_string(array):
    return array[1]


def parse_bulk_string(array):
    string_byte_len = int(array[0][1:])
    if string_byte_len > 0:
        return array[1]
    else:
        return None


def parse_error(array):
    return array[1]


def parse_int(array):
    return int(array[1])


command_map = {
    '*': parse_array,
    '+': parse_simple_string,
    '$': parse_bulk_string,
    '-': parse_error,
    ':': parse_int
}


def parse_command(str, index):
    """
    gets called everytime a user issues a command, parses the command array out into component parts and then passes to command_handler
    :param str:
    :param index:
    :return:
    """
    items = str.split("\r\n")
    items = list(filter(lambda x: x, items))
    array_size = int(items[0][1:])
    command_arr = parse_array(items[1:], array_size)
    return command_arr
