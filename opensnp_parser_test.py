import unittest
from opensnp_parser import opensnp_Parser

class Test_user_data_parser_test(unittest.TestCase):
    # check if the key passed to rsid_fetch_RSID is valid
    def test_rsid_fetch_RSID(self):
        parser = opensnp_Parser()
        with self.assertRaises(KeyError):
            parser.fetch_RSID_info('gdsdasdas')