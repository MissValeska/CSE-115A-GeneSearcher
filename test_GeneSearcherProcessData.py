import unittest
import GeneSearcherProcessData
import user_data_parser

class Test_GeneSearcherProcessData(unittest.TestCase):
    
    # test if report generated properly locally
    def test_process_user_data_locally(self):
        data = load_user_data("23andMeSample.txt")
        dataset = load_data_set_from_file("RSID_Data_LOG.json")
        report = process_user_data(data, data_set)
    

    # test if report generated properly using server
     def test_process_user_data_server(self):
        data = load_user_data("23andMeSample.txt")
        dataset = load_data_set_from_server()
        report = process_user_data(data, data_set)