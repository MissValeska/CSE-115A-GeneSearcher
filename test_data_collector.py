import unittest
from data_collector import data_collector

class test_data_collector(unittest.TestCase):
    def test_update_bulk(self):
        # test if the function update updates rsids properly
        collector = data_collector(1)
        rsids = ["rs548049170", "rs9283150", "rs116587930", "rs3131972", "rs12184325"]
        # what the dictionary should look like
        dictionary = {"rs548049170"  :  ['1', '69869', 'TT'],
                    "rs9283150"  :  ['1', '565508', 'AA'],
                    "rs116587930"  :  ['1', '727841', 'GG'],
                    "rs3131972"  :  ['1', '752721', 'AG'],
                    "rs12184325"  :  ['1', '754105', 'CT']}
        # what the interesting rsids list should be
        list = rsids
        collector.update_bulk(rsids)
        self.assertEqual(collector.RSID_data, dictionary)
        self.assertEqual(collector.interesting_RSIDs, list)
        print(collector.RSID_data)
        print (collector.interesting_RSIDs)
    
    # check if the function gets snp list correctly
    def test_get_snp_list(self):
        list1 = get_snp_list(snp_list.txt)
        list2 = ["rs548049170", "rs9283150", "rs116587930", "rs3131972", "rs12184325"]
        self.assertEqual(list1, list2)
    
    
if __name__ == "__main__":

    unittest.main()