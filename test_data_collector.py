import unittest
from data_collector import data_collector
from data_collector import get_snp_list

class test_data_collector(unittest.TestCase):
    def test_update_bulk(self):
        # test if the function update updates rsids properly
        collector = data_collector(1)
        rsids = ["rs548049170", "rs9283150", "rs116587930", "rs3131972", "rs12184325"]
        # what the dictionary should look like
        dictionary = {'rs116587930': {'traits': {}, 'weight': 0},
                    'rs12184325': {'traits': {}, 'weight': 0},
                    'rs3131972': {'traits': {}, 'weight': 0},
                    'rs548049170': {'traits': {}, 'weight': 0},
                    'rs9283150': {'traits': {}, 'weight': 0}}
                    
        # what the interesting rsids list should be
        list = rsids
        collector.update_bulk(rsids)
        self.assertEqual(collector.RSID_data, dictionary)
        self.assertEqual(collector.interesting_RSIDs, list)
      
    
    # check if the function gets snp list correctly
    def test_get_snp_list(self):
        list1 = get_snp_list("snp_list.txt")
        list2 = ["rs548049170", "rs9283150", "rs116587930", "rs3131972", "rs12184325"]
        self.assertEqual(sorted(list1), sorted(list2))
    
    # check if the function loads the data properly
    def test_load(self):
        collector = data_collector()
        with open ('condensed_data_log_v3.json') as file:
           data = json.load(file)
           self.aserEqual(data, collector.load('condensed_data_log_v3.json')
    
if  __name__ == "__main__":

    unittest.main()