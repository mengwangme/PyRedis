import unittest
from src.command_parser import parse_command


class CommandParserTests(unittest.TestCase):
    def test_parse_commandt(self): 
        response = parse_command("*1\r\n$7\r\nCOMMAND\r\n", 0)
        self.assertEqual(response[0], "COMMAND")

    def test_parse_set_command(self):
        '''
        SET key value
        :return:
        '''
        response = parse_command("*3\r\n$3\r\nSET\r\n$3\r\nkey\r\n$5\r\nvalue\r\n", 0)
        self.assertEqual(response[0], "SET")
        self.assertEqual(response[1], "key")
        self.assertEqual(response[2], "value")

    def test_parse_get_command(self):
        '''
        GET key
        :return:
        '''
        response = parse_command("*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n", 0)
        self.assertEqual(response[0], "GET")
        self.assertEqual(response[1], "key")

    # set

    def test_parse_sadd_command(self):
        '''
        SADD key member [member ...]
        :return:
        '''
        response = parse_command("*3\r\n$4\r\nSADD\r\n$3\r\nkey\r\n$3\r\nmember\r\n", 0)
        self.assertEqual(response[0], "SADD")
        self.assertEqual(response[1], "key")
        self.assertEqual(response[2], "member")

    def test_parse_spop_command(self):
        '''
        SPOP key
        :return:
        '''
        response = parse_command("*2\r\n$4\r\nSPOP\r\n$3\r\nkey\r\n", 0)
        self.assertEqual(response[0], "SPOP")
        self.assertEqual(response[1], "key")

    def test_parse_sdiff_command(self):
        '''
        SDIFF group1 group2
        :return:
        '''
        response = parse_command("*3\r\n$5\r\nSDIFF\r\n$6\r\ngroup1\r\n$6\r\ngroup2\r\n", 0)
        self.assertEqual(response[0], "SDIFF")
        self.assertEqual(response[1], "group1")
        self.assertEqual(response[2], "group2")

    def test_parse_sinter_command(self):
        '''
        SINTER group1 group2
        :return:
        '''
        response = parse_command("*3\r\n$6\r\nSINTER\r\n$6\r\ngroup1\r\n$6\r\ngroup2\r\n", 0)
        self.assertEqual(response[0], "SINTER")
        self.assertEqual(response[1], "group1")
        self.assertEqual(response[2], "group2")

    def test_parse_sunion_coomand(self):
        '''
        SUNION group1 group2
        :return:
        '''
        response = parse_command("*3\r\n$6\r\nSUNION\r\n$6\r\ngroup1\r\n$6\r\ngroup2\r\n", 0)
        self.assertEqual(response[0], "SUNION")
        self.assertEqual(response[1], "group1")
        self.assertEqual(response[2], "group2")


    # list

    def test_parse_lpush_command(self):
        '''
        LPUSH key value
        :return:
        '''
        response = parse_command("*3\r\n$5\r\nLPUSH\r\n$3\r\nkey\r\n$5\r\nvalue\r\n", 0)
        self.assertEqual(response[0], "LPUSH")
        self.assertEqual(response[1], "key")
        self.assertEqual(response[2], "value")

    def test_parse_lpop_command(self):
        '''
        LPOP  key
        :return:
        '''
        response = parse_command("*2\r\n$4\r\nLPOP\r\n$3\r\nkey\r\n", 0)
        self.assertEqual(response[0], "LPOP")
        self.assertEqual(response[1], "key")


    # def test_parse_lindex_commmand(self):
    #     '''
    #     LINDEX key number
    #     :return:
    #     '''
    #     response = parse_command("*3\r\n$6\r\nLINDEX\r\n$3\r\nkey\r\n:1\r\n", 0)
    #     self.assertEqual(response[0], "LINDEX")
    #     self.assertEqual(response[1], "key")
    #     self.assertEqual(response[2], 1)

    def test_parse_llen_command(self):
        '''
        LLEN key
        :return:
        '''
        response = parse_command("*2\r\n$4\r\nLLEN\r\n$3\r\nkey\r\n", 0)
        self.assertEqual(response[0], "LLEN")
        self.assertEqual(response[1], "key")

    # hash

    def test_parse_hset_command(self):
        '''
        HSET key field value
        :return:
        '''
        response = parse_command("*4\r\n$4\r\nHSET\r\n$3\r\nkey\r\n$5\r\nfield\r\n$5\r\nvalue\r\n", 0)
        self.assertEqual(response[0], "HSET")
        self.assertEqual(response[1], "key")
        self.assertEqual(response[2], "field")
        self.assertEqual(response[3], "value")

    def test_parse_hmset_command(self):
        '''
        HMSET key field1 value1 field2 valu2
        :return:
        '''
        response = parse_command("*5\r\n$5\r\nHMSET\r\n$3\r\nkey\r\n$6\r\nfield1\r\n$6\r\nvalue1\r\n$6\r\nfield2\r\n$6\r\nvalue2\r\n", 0)
        self.assertEqual(response[0], "HMSET")
        self.assertEqual(response[1], "key")
        self.assertEqual(response[2], "field1")
        self.assertEqual(response[3], "value1")
        self.assertEqual(response[4], "field2")
        self.assertEqual(response[5], "value2")

    def test_parse_hget_command(self):
        '''
        HGET key field
        :return:
        '''
        response = parse_command("*3\r\n$4\r\nHGET\r\n$3\r\nkey\r\n$5\r\nfield\r\n", 0)
        self.assertEqual(response[0], "HGET")
        self.assertEqual(response[1], "key")
        self.assertEqual(response[2], "field")

    def test_parse_hmget_command(self):
        '''
        HMGET key field1 field2
        :return:
        '''
        response = parse_command("*3\r\n$5\r\nHMGET\r\n$3\r\nkey\r\n$6\r\nfield1\r\n$6\r\nfield2\r\n", 0)
        self.assertEqual(response[0], "HMGET")
        self.assertEqual(response[1], "key")
        self.assertEqual(response[2], "field1")
        self.assertEqual(response[3], "field2")

    def test_parse_hgetall_command(self):
        '''
        HGETALL key
        :return:
        '''
        response = parse_command("*2\r\n$7\r\nHGETALL\r\n$3\r\nkey\r\n", 0)
        self.assertEqual(response[0], "HGETALL")
        self.assertEqual(response[1], "key")

    # normal

    def test_parse_flush_command(self):
        '''
        FLUSH
        :return:
        '''
        response = parse_command("*1\r\n$5\r\nFLUSH\r\n", 0)
        self.assertEqual(response[0], "FLUSH")

    def test_parse_save_command(self):
        '''
        SAVE
        :return:
        '''
        response = parse_command("*1\r\n$4\r\nSAVE\r\n", 0)
        self.assertEqual(response[0], "SAVE")

    def test_parse_exists_command(self):
        '''
        EXISTS key
        :return:
        '''
        response = parse_command("*2\r\n$6\r\nEXISTS\r\n$3\r\nkey\r\n", 0)
        self.assertEqual(response[0], "EXISTS")
        self.assertEqual(response[1], "key")

    # def test_parse_expire_command(self):
    #     '''
    #     EXPIRE key seconds
    #     :return:
    #     '''
    #     response = parse_command("*3\r\n$6\r\nEXPIRE\r\n$3\r\nkey\r\n:100\r\n", 0)
    #     self.assertEqual(response[0], "EXPIRE")
    #     self.assertEqual(response[1], "key")
    #     self.assertEqual(response[2], 100)

    def test_parse_ttl_command(self):
        '''
        TTL key
        :return:
        '''
        response = parse_command("*2\r\n$3\r\nTTL\r\n$3\r\nkey\r\n", 0)
        self.assertEqual(response[0], "TTL")
        self.assertEqual(response[1], "key")

    def test_parse_del_command(self):
        '''
        DEL key [key ...]
        :return:
        '''
        response = parse_command("*2\r\n$3\r\nDEL\r\n$3\r\nkey\r\n", 0)
        self.assertEqual(response[0], "DEL")
        self.assertEqual(response[1], "key")



