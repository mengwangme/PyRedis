import unittest
from src.memory import memory
from src.command_handler import smembers_command,sadd_command,resp_array,resp_string,lpush_command,lrange_command
from src.command_parser import *


class CommandHandlerTests(unittest.TestCase):
    def test_smembers(self):
        memory.volatile={}
        sadd_command("key", ["value1", "value2"])
        response = smembers_command("key")
        if response=='*2\r\n+value1\r\n+value2\r\n':
            self.assertEqual(response, resp_array([resp_string("value1"), resp_string("value2")]))
        else:
            self.assertEqual(response, resp_array([resp_string("value2"), resp_string("value1")]))

    def test_lrange(self):
        memory.volatile={}
        lpush_command("key", ["value1", "value2"])
        response = lrange_command("key", ["0", "1"])
        self.assertEqual(response, resp_array([resp_string("value1"), resp_string("value2")]))
