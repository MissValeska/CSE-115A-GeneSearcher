import unittest
import queue
from opensnp_parser import opensnp_Parser

class Test_user_data_parser_test(unittest.TestCase):
    # check if the key passed to rsid_fetch_RSID is valid
    def test_rsid_fetch_RSID(self):
        parser = opensnp_Parser()
        with self.assertRaises(KeyError):
            parser.fetch_RSID_info('gdsdasdas')
    # check if bulk worker returns correct data on given snps      
    def test_fetch_bulk_worker(self):
        parser = opensnp_Parser()
        # check the follwing rsids
        rsids = ["rs12979860", "rs8099917", "rs6983267", "rs671", "rs4420638" ]
        parser.fetch_bulk_RSID_info(rsids)
        for rsid in rsids:
            self.assertEqual(parser.fetch_RSID_info(rsid), parser.RSID_data[rsid])
        
     
if __name__ == "__main__":

    unittest.main()