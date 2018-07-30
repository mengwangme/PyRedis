import unittest
from src.command_handler import *
from src.command_parser import *
from src.memory import memory


class CommandHandlerTests(unittest.TestCase):
    def test_set(self): # 测试set处理函数
        memory.volatile = {}
        response = set_command("key", ["value"])
        self.assertEqual(memory.volatile["key"], "value")

    def test_get(self): # 测试get处理函数
        memory.volatile = {}
        set_command("key", ["value"])
        response = get_command("key")
        self.assertEqual(response, resp_bulk_string("value"))

    # 集合

    def test_sadd(self):
        memory.volatile = {}
        response = sadd_command("key", ["value"])
        self.assertEqual(memory.volatile["key"], {"value"})

    def test_spop(self):
        memory.volatile = {}
        sadd_command("key", ["value"])
        response = spop_command("key")
        self.assertEqual(response, resp_string("value"))

    def test_sdiff(self):
        memory.volatile = {}
        sadd_command("key1", ["value1", "value2"])
        sadd_command("key2", ["value1"])
        response = sdiff_command("key1", ["key2"])
        self.assertEqual(response, '*1\r\n+value2\r\n')

    def test_sinter(self):
        memory.volatile = {}
        sadd_command("key1", ["value1", "value2"])
        sadd_command("key2", ["value1"])
        response = sinter_command("key1", ["key2"])
        self.assertEqual(response, resp_array([resp_string("value1")]))

    # def test_sunion(self):
    #     memory.volatile = {}
    #     sadd_command("key1", ["value1"])
    #     sadd_command("key2", ["value2"])
    #     response = sunion_command("key1", ["key2"])
    #     self.assertEqual(response, resp_array([resp_string("value1"), resp_string("value2")]))

    # 列表
    def test_llen(self): # 测试llen处理函数
        memory.volatile = {}
        lpush_command("list", ["1", "2", "3"])
        response = llen_command("list")
        self.assertEqual(response, resp_integer(3))

    def test_lpush(self):
        memory.volatile = {}
        lpush_command("list", ["1", "2", "3"])
        self.assertEqual(memory.volatile["list"], ["1", "2", "3"])

    def test_lpop(self):
        memory.volatile = {}
        lpush_command("list", ["value"])
        response = lpop_command("list")
        self.assertEqual(response, resp_bulk_string("value"))

    def test_lindex(self):
        memory.volatile = {}
        lpush_command("list", ["value"])
        response = lindex_command("list", "0")
        self.assertEqual(response, resp_string("value"))

    # 哈希
    def test_hset(self):
        memory.volatile = {}
        response = hset_command("key",["field", "value"])
        self.assertEqual(memory.volatile["key"], {"field": "value"})

    def test_hmset(self):
        memory.volatile = {}
        response = hmset_command("key", ["field1", "value1", "field2", "value2"])
        self.assertEqual(memory.volatile["key"], {'field1': 'value1', 'field2': 'value2'})

    def test_hget(self):
        memory.volatile = {}
        hset_command("key", ["field", "value"])
        response = hget_command("key", ["field"])
        self.assertEqual(response, resp_bulk_string("value"))

    def test_hmget(self):
        memory.volatile = {}
        hmset_command("key", ["field1", "value1", "field2", "value2"])
        response = hmget_command("key", ["field1", "field2"])
        self.assertEqual(response, resp_array([resp_bulk_string("value1"), resp_bulk_string("value2")]))

    def test_hgetall(self):
        memory.volatile = {}
        hmset_command("key", ["field1", "value1", "field2", "value2"])
        response = hget_all_command("key")
        self.assertEqual(response, resp_array([resp_string("field1"), resp_string("value1"), resp_string("field2"), resp_string("value2")]))

    # 通用命令
    def test_flush(self):
        flush_command()
        self.assertEqual(memory.volatile, {})


    def test_save(self):
        flush_command()
        set_command("key", ["value"])
        save_command()
        flush_command()
        memory.load_state()
        self.assertEqual(memory.volatile["key"], 'value')

    def test_exists(self):
        flush_command()
        set_command("key", ["value"])
        response = exists_command("key")
        self.assertEqual(response, resp_integer(1))

    def test_expire(self):
        import time
        flush_command()
        set_command("key", ["value"])
        response = expire_command("key", [10])
        self.assertEqual(int(memory.expiring["key"] - time.time()),9)

    def test_ttl(self):
        flush_command()
        set_command("key", ["value"])
        expire_command("key", [10])
        response = ttl_command("key")
        self.assertEqual(response, resp_integer(int(memory.expiring["key"] - time.time())))


    def test_del(self):
        flush_command()
        flush_command()
        set_command("key", ["value"])
        del_command("key")
        self.assertEqual(memory.volatile, {})