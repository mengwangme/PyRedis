"""
The command handler module provides a generic handle_command which uses a string->function map to determine the appropriate command,
execute it, and return a result
"""

import gevent
import time
from src.memory import memory


def output_commands():
    """
    Returns an array of array of strings that define available commands
    :return:
    """
    return resp_array(
            [resp_array(
                [resp_string("\"get\""),
                 resp_string("(integer) 2"),
                 resp_string("1) readonly"),
                 resp_string("(integer) 1"),
                 resp_string("(integer) 1"),
                 resp_string("(integer) 1")]),
             resp_array(
                [resp_string("\"set\""),
                 resp_string("(integer) -3"),
                 resp_string("3) 1) \"write\""),
                 resp_string("   2) \"denyoom\""),
                 resp_string("(integer) 1"),
                 resp_string("(integer) 1"),
                 resp_string("(integer) 1")])
            ])


def set_command(key, args):
    """
    Performs a simple set of a value to a key
    :param key: key to set
    :param args: arg0 is the value
    :return:
    """
    memory.volatile[key] = args[0]
    return resp_bulk_string("OK")


def get_command(key):
    """
    Performs a simple get of a value from a key
    :param key: key of the value to get
    :return:
    """
    return resp_bulk_string(memory.volatile[key])


def sadd_command(key, args):
    """
    Adds a value to a set, creates the set if it does not exist.
    :param key: key of the set to add to
    :param args: args[0] is the value to add to it
    :return:
    """
    if memory.volatile.get(key) is None:  # if the set is not initialized
        memory.volatile[key] = set(args)
        return resp_integer(len(memory.volatile[args]))
    else:
        if isinstance(memory.volatile.get(key), set):  # does the given key exist in memory
            r = len(memory.volatile.get(key).intersection(set(args)))
            memory.volatile[key] = memory.volatile.get(key).union(set(args))
            if r == 0:
                return resp_integer(1)
            else:
                return resp_integer(0)
        else:  # if the set exists but is NOT a set, then throw an error
            return resp_error("KEY {0} IS NOT A SET.".format(args[1]))


def spop_command(key):
    """
    Pop the first value from a set, this is based on the dict implementation in python and as such
    is not a 1:1 with the redis implementation which is based on a hashmap and pops items randomly from a set
    :param args: args[1] is the key, args[2]
    :return:
    """
    memory.volatile[key] = memory.volatile.get(key)

    if isinstance(memory.volatile.get(key), set):
        if len(memory.volatile.get(key)) == 0:
            return resp_error("KEY {0} HAS NO ITEMS".format(key))
        else:
            return resp_string(memory.volatile[key].pop())
    else:
        return resp_error("KEY {0} IS NOT A SET.".format(key))


def sdiff_command(key, args):
    """
    Performs a set difference from the first argument to all subsequent arguments
    args1.diff(args2).diff(args3)...
    :param key: key to start set intersection from
    :param args: subsequent arguments are the other keys to diff
    :return:
    """
    starting_set = memory.volatile[key]

    for st in args:
        if st in memory.volatile:
            if not isinstance(memory.volatile[st], set):
                return resp_error("KEY {0} IS NOT A SET.".format(st))
            else:
                starting_set = starting_set.difference(memory.volatile[st])
        else:
            return resp_error("NO SUCH KEY {0} EXISTS".format(st))

    final_set = []
    for item in starting_set:
        final_set.append(resp_string(item))
    return resp_array(final_set)


def sinter_command(key, args):
    """
    Performs a set intersection from the first argument to all subsequent arguments
    args1.intersection(args2).union(args3)...
    :param key: key to start set intersection from
    :param args: list of all the other the other keys to intersect
    :return:
    """
    starting_set = memory.volatile[key]
    if len(args) == 0: # then we have no additional sets to perform intersection with
        return resp_error("SINTER REQUIRES MORE THAN ONE SET TO BE SPECIFIED")
    for st in args:
        if st in memory.volatile:
            if not isinstance(memory.volatile[st], set):
                return resp_error("KEY {0} IS NOT A SET.".format(st))
            else:
                starting_set = starting_set.intersection(memory.volatile[st])
        else:
            return resp_error("NO SUCH KEY {0} EXISTS".format(st))

    final_set = []
    for item in starting_set:
        final_set.append(resp_string(item))
    return resp_array(final_set)


def sunion_command(key, args):
    """
    Performs a set union from the first argument to all subsequent arguments
    args1.union(args2).union(args3)...
    :param key: key to start set union from
    :param args: list of all the other the other keys to union
    :return:
    """
    starting_set = memory.volatile[key]

    for st in args:
        if st in memory.volatile:
            if not isinstance(memory.volatile[st], set):
                return resp_error("KEY {0} IS NOT A SET.".format(st))
            else:
                starting_set = starting_set.union(memory.volatile[st])
        else:
            return resp_error("NO SUCH KEY {0} EXISTS".format(st))

    final_set = []
    for item in starting_set:
        final_set.append(resp_string(item))
    return resp_array(final_set)


def lpush_command(key, args):
    """
    Push a value onto a list, creates the list if it does not exist
    :param key: key of the list to push onto
    :param args: values to push onto the list, can be many
    :return:
    """
    if key not in memory.volatile:
        memory.volatile[key] = []
    memory.volatile[key] = args + memory.volatile[key]
    return resp_integer(len(memory.volatile[key]))


def flush_command():
    memory.volatile = {}
    memory.expiring = {}
    return resp_string("OK")


def save_command():
    memory.save_state()
    return resp_string("OK")


def exists_command(key):
    return resp_integer(1 if key in memory.volatile else 0)


def del_command(key):
    """
    Delete an item at key in memory
    :param key: the key to delete
    :return:
    """
    del memory.volatile[key]
    return resp_bulk_string("OK")


def expire_command(key, args):
    """
    Given a key and a time to live, set a key to expire
    :param key: the key to expire
    :param args: args[0] is the time to live
    :return:
    """
    def delete_when_expired(k):
        del memory.volatile[k]
        del memory.expiring[k]

    if key in memory.volatile:
        memory.expiring[key] = time.time() + int(args[0])
        gevent.spawn_later(int(args[0]), delete_when_expired, key)
        return resp_bulk_string("OK")
    else:
        return no_such_key(args)


def ttl_command(key):
    """
    Given a key, provide the TTL for that key. If the key was not set to expire, provide an error
    :param key: key to provide the TTL for
    :return:
    """
    if key in memory.expiring:
        return resp_integer(int(memory.expiring[key]-time.time()))
    else:
        return resp_error("NO KEY MATCHING {0} HAS AN EXPIRATION SET".format(key))


def lpop_command(key):
    """
    Pops the first entry off the list, returns an error if the list is empty
    :param key: the list to pop an entry off of
    :return:
    """
    l = memory.volatile[key]
    if len(l) > 0:
        return resp_bulk_string(l.pop(0))
    else:
        return resp_error("LIST WITH KEY {0} IS EMPTY.".format(l))


def lindex_command(key, args):
    """
    returns the value at the index in the specified list
    :param key: key of the list
    :param args: args[0] index in the list to get
    :return:
    """
    l = memory.volatile[key]
    if args[0] is not None:
        i = int(args[0])
        if i > len(l):
            return resp_error("INDEX OUT OF RANGE FOR LIST WITH KEY {0}".format(key))
        return resp_string(l[i])
    else:
        return resp_error("INDEX NOT SPECIFIED FOR LIST WITH KEY {0}".format(key))


def llen_command(key):
    """
    returns the length of the specified list
    :param key: key of the list
    :return:
    """
    l = memory.volatile[key]
    return resp_integer(len(l))


def hset_command(key, args):
    """
    Set a value in a hashmap, if the hashmap does not exist create it
    :param key: this is the hashmap key
    :param args: key,value to set in the hashmap
    :return:
    """
    hm = memory.volatile.get(key, None)  # check to see if hashmap exists
    if hm is None:  # if it does not exist
        memory.volatile[key] = {args[0]: args[1]}  # create it and set the first key value pair
        hm = memory.volatile[key]
        return resp_integer(1)
    elif args[0] in hm:
        hm[args[0]] = args[1]
        return resp_integer(0)
    else:
        hm[args[0]] = args[1]
        return resp_integer(1)


def hget_command(key, args):
    """
    get a key in a hashmap
    :param key: this is the hashmap key
    :param args: args[0] is the key in the hashmap you want to get
    :return:
    """
    hm = memory.volatile[key] # get the hashmap from memory
    if args[0] in hm: # see if the key is in the hashmap
        return resp_bulk_string(hm[args[0]]) # return it
    else:
        return no_such_key(args) # give an error if the key does not exist


def hmget_command(key, args):
    """
    get the value of multiple named keys in a hashmap, return an array of all keys, or (nil) if no such key exists.
    :param key: this is the hashmap key
    :param args: args[0].. is the key in the hashmap, can be multiple keys
    :return:
    """
    hm = memory.volatile.get(key, None) # get the hashmap from memory
    arr = []
    for val in args: # iterate over the arguments of keys
        if val in hm: # if we find the value
            arr.append( # add it to the array
                resp_bulk_string(
                    hm[val]
                ))
        else:
            arr.append("$-1\r\n")  # else append (nil) as per the redis spec for this command
    return resp_array(arr)


def hmset_command(key, args):
    """
    set multiple key values
    :param key:
    :param args:
    :return:
    """
    hm = memory.volatile.get(key, None) # check to see if hashmap exists
    if hm is None: # if it does not exist
        memory.volatile[key] = {}  # create it
        hm = memory.volatile[key]

    for i in range(0, len(args), 2): # iterate through this 2 records at a time, to grab key,value
        k = args[i]  # key is the first value
        v = args[i+1]  # value is second
        hset_command(key, [k, v])  # utilize the hset_command to set the key
    return resp_bulk_string("OK")


def hget_all_command(key):
    """
    returns all keys of the specified hashmap as an array
    :param key:
    :return:
    """
    hm = memory.volatile.get(key, None)
    return_arr = []
    for k,v in hm.items():
        return_arr.append(resp_string(k))
        return_arr.append(resp_string(v))
    return resp_array(return_arr)


def not_implemented_command():
    return resp_string("NOT IMPLEMENTED")


def no_such_key(key):
    return resp_error("NO SUCH KEY {0} EXISTS".format(key))


"""
command_map is a data structure that maps commands to functions

If you add a new command, you can add it here and tie it to it's corresponding function code
and it will be executed by handle_command when entered on a client's command line.
This callback style is similar to a Strategy or Command pattern and is a "pythonic" way to solve this problem set.
min specifies the minimum number of arguments
max specifies the maximum number of arguments
if max is -1 that means any number of arguments can be added
if max is -3 that means any number of arguments can be added but the total number of arguments must be odd
"""

command_map = {
    "COMMAND": {"min": 0, "max": 0, "function": output_commands},
    "SET": {"min": 2, "max": 2, "function": set_command},
    "GET": {"min": 1, "max": 1, "function": get_command},
    "SADD": {"min": 2, "max": -1, "function": sadd_command},
    "SPOP": {"min": 1, "max": 1, "function": spop_command},
    "SDIFF": {"min": 1, "max": -1, "function": sdiff_command},
    "SINTER": {"min": 2, "max": -1, "function": sinter_command},
    "SUNION": {"min": 2, "max": -1, "function": sunion_command},
    "FLUSH": {"min": 0, "max": 0, "function": flush_command},
    "SAVE": {"min": 0, "max": 0, "function": save_command},
    "EXISTS": {"min": 1, "max": 1, "function": exists_command},
    "EXPIRE": {"min": 2, "max": 2, "function": expire_command},
    "TTL": {"min": 1, "max": 1, "function": ttl_command},
    "DEL": {"min": 1, "max": 1, "function": del_command},
    "LPUSH": {"min": 2, "max": -1, "function": lpush_command},
    "LPOP": {"min": 1, "max": 1, "function": lpop_command},
    "LINDEX": {"min": 2, "max": 2, "function": lindex_command},
    "LLEN": {"min": 1, "max": 1, "function": llen_command},
    "HSET": {"min": 3, "max": 3, "function": hset_command},
    "HGET": {"min": 2, "max": 2, "function": hget_command},
    "HMGET": {"min": 2, "max": -1, "function": hmget_command},
    "HMSET": {"min": 3, "max": -3, "function": hmset_command},
    "HGETALL": {"min": 1, "max": 1, "function": hget_all_command}
}


def list_get(L, i, v=None):
    try: return L[i]
    except IndexError: return v


def handle_command(command_with_args):
    """
    Generic command handling function, uses command_map to determine which function to execute
    :param command_with_args:
    :return: RESP compliant response to be sent to client
    """
    command = str(command_with_args[0]).upper()
    if command not in command_map:
        return not_implemented_command()
    matched_command = command_map[command]

    args = command_with_args[2:] or []
    key = list_get(command_with_args, 1, None)
    total_arg_length = len(args) + (1 if key is not None else 0)  # includes the key as well

    # now validate the lengths of arguments with what we have in the matched command
    if total_arg_length < matched_command["min"]:
        return resp_error("Not enough arguments for command {0}, minimum {1}".format(command, matched_command["min"]))

    if matched_command["max"] >= 0:
        if total_arg_length > matched_command["max"]:
            return resp_error("Too many arguments for command {0}, maximum {1}".format(command, matched_command["min"]))
    else:   # this means there are many many values allowed, the protocol does not dictate how many
            # if the value is -1 then any number is fine, but if the value is -3 then we need to make sure args is odd
        if matched_command["max"] == -3 and not total_arg_length % 2:   # this means it is even but we need an odd value
            return resp_error("Not enough arguments or an invalid number of arguments was specified")

    # this is somewhat redundant given what we just added above
    if key is not None and key not in memory.volatile and command not in ['EXISTS', 'HSET', 'SET', 'HMSET', 'SADD', 'LPUSH']:
        return no_such_key(key)

    if len(args) > 0:
        return command_map[command]["function"](key, args)
    elif key is not None:
        return command_map[command]["function"](key)
    else:
        return command_map[command]["function"]()


"""
These are utility functions to produce RESP compliant output
Based on https://redis.io/topics/protocol
"""


def resp_string(val):
    return "+"+val+"\r\n"


def resp_bulk_string(val):
    return "$"+str(len(val))+"\r\n"+val+"\r\n"


def resp_error(val):
    return "-"+val+"\r\n"


def resp_integer(val):
    return ":"+str(val)+"\r\n"


def resp_array(arr):  # your array entries must be resp encoded strings/ints
    val = "*"+str(len(arr))+"\r\n"
    for item in arr:
        if isinstance(val, list):
            val += resp_array(item)
        else:
            val += item
    return val