import unittest
from src.memory import memory
from src.command_handler import *
from src.command_parser import *


class CommandHandlerTests(unittest.TestCase):
    def test_smembers(self):
        memory.volatile={}
        sadd_command("key", ["value1", "value2"])
        response = smembers_command("key")
        self.assertEqual(response, resp_array([resp_string("value1"), resp_string("value2")]))

    def test_lrange(self):
        memory.volatile={}
        lpush_command("key", ["value1", "value2", "value3"])
        response = lrange_command("key", ["0", "1"])
        self.assertEqual(response, resp_array([resp_string("value1"), resp_string("value2")]))