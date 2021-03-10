from model import Genesearcher_Model as gm
from controller import GeneSearcher_Controller as gc
from unittest import mock
import unittest

'''
Unit tests for the Genesearcher Model module
'''

class GenesearcherModelTestSettersGetters(unittest.TestCase):
    def setUp(self):
        self.m = gm(self)
    
    def test_set_user_data(self):
        data = { "rs548049170" : [1, 69869, "TT"],
                 "rs116452738" : [1, 834830, "GG"] }
        self.m.set_user_data(data)
        self.assertEqual(self.m.get_user_data(), data, "Error in setter or getter for user_data")

    def test_set_data_set(self):
        data = {"rs2224718": {"weight": 0, "traits": {}},
                "rs3753242": {"weight": 6, "traits": {"CC": "common on affy axiom dat"}}}

        self.m.set_data_set(data)
        self.assertEqual(self.m.get_data_set(), data, "Error in setter or getter for data_set")

    def test_set_report_empty(self):
        report = {}
        self.m.set_report(report)
        self.assertEqual(self.m.get_report(), report, "Error in setter or getter for empty report")
    
    def test_set_report(self):
        report = {"rs2224718": ["CG", "1.08x ris", 15],
                  "rs10495584": ["AA", "Normal (higher) blood pressure", 15]}
        self.m.set_report(report)
        self.assertEqual(self.m.get_report(), report, "Error in setter or getter for report")


    def test_input_file(self):
        filename = "testFile.txt"
        self.m.set_input_file(filename)
        self.assertEqual(self.m.get_input_file(), filename, "Error in setter or getter for input_file")

class GenesearcherModelTestProcessing(unittest.TestCase):
    def setUp(self):
        self.m = gm(self)

    def test_load_user_data_no_header(self):
        mock_data = "rs548049170	1	69869	TT\n\
                     rs9283150	1	565508	AA\n\
                     rs114525117	1	759036	GG"
        with mock.patch("builtins.open", mock.mock_open(read_data=mock_data), create=False) as mock_file:
            self.m.load_user_data("path")
            mock_file.assert_called_once_with("path")
        
        expected_data = {"rs548049170": ["1", "69869", "TT"],
                         "rs9283150": ["1", "565508", "AA"],
                         "rs114525117": ["1", "759036", "GG"]}
        self.assertEqual(self.m.get_user_data(), expected_data, "Incorrect Data loaded!" )

    def test_load_user_data_with_header(self):
        mock_data = "# This is a header\n\
                     rs548049170	1	69869	TT\n\
                     rs9283150	1	565508	AA\n\
                     rs114525117	1	759036	GG"
        with mock.patch("builtins.open", mock.mock_open(read_data=mock_data)) as mock_file:
            self.m.load_user_data("path")
            mock_file.assert_called_once_with("path")
        
        expected_data = {"rs548049170": ["1", "69869", "TT"],
                         "rs9283150": ["1", "565508", "AA"],
                         "rs114525117": ["1", "759036", "GG"]}
        self.assertEqual(self.m.get_user_data(), expected_data, "Incorrect Data loaded!" )

    def test_load_data_set_from_file(self):
        mock_data = """{"rs2224718": {"weight": 0, "traits": {}},"rs3753242": {"weight": 6, "traits": {"CC": "common on affy axiom dat"}}}"""
        with mock.patch("builtins.open", mock.mock_open(read_data=mock_data)) as mock_file:
            self.m.load_data_set_from_file("path")
            mock_file.assert_called_once_with("path")
        
        expected_data = {"rs2224718": {"weight": 0, "traits": {}},
                         "rs3753242": {"weight": 6, "traits": {"CC": "common on affy axiom dat"}}}
        self.assertEqual(self.m.get_data_set(), expected_data, "Incorrect data set loaded!" )

    def test_load_data_set_from_server(self):
        # Not actually sure how to test this...
        self.m.load_data_set_from_server()
        server_data = self.m.get_data_set()
        self.assertIsNotNone(server_data, "Error: No server data loaded")

    def test_generate_report(self):
        # Second field in user data is filled with fake data because it is never
        test_user_data = {"rs590787": ["1","25629943","AG"],
                          "i4000422": ["1","80910740","GG"],
                          "rs1734792": ["1","37530092","CC"],
                          "rs188742236": ["8","37407375", "CC"]}
        self.m.set_user_data(test_user_data)

        test_data_set = {"rs590787": {"weight": 15, "traits": {"TT": "Rh+ (Rhesus factor positive", "CC": "Rh- (Rhesus negative", "CT": "Rh+ (Rhesus factor positive"}},
                         "i4000422": {"weight": 15, "traits": {"AG": "Maple Syrup Urine Disease Type 1B carrier", "GG": "normal", "AA": "Maple Syrup Urine Disease Type 1B "}},
                         "rs2032599": {"weight": 7, "traits": {"CC": "No summary provided"}},
                         "rs1734792": {"weight": 17, "traits": {"AC": "1.4x increased risk for lupus", "AA": "normal", "CC": "1.4x increased risk for lupus"}}}
        self.m.set_data_set(test_data_set)
        
        self.m.generate_report()
        
        expected_report = { "rs590787": ("AG", "Rh+ (Rhesus factor positive", 15),
                   "i4000422": ("GG", "normal", 15),
                   "rs1734792": ("CC", "1.4x increased risk for lupus", 17)}
        self.assertEqual(self.m.get_report(), expected_report, "Report not properly generated")
                
class GenesearcherModelTestReportOutput(unittest.TestCase):
    def setUp(self):
        self.m = gm(self)
        report = { "rs590787": ["AG", "Rh+ (Rhesus factor positive", 15],
                   "i4000422": ["GG", "normal", 15],
                   "rs1734792": ["CC", "1.4x increased risk for lupus", 17]}
        self.m.set_report(report)

    def test_report_to_json(self):
        # This test is broken.
        with mock.patch("builtins.open", mock.mock_open()) as mock_file:
            self.m.user_report_to_json("path")
            mock_file.assert_called_once_with("path", "w")
            mock_file.return_value.write.assert_called_once_with('{"rs590787": ["AG", "Rh+ (Rhesus factor positive", 15], "i4000422": ["GG", "normal", 15], "rs1734792": ["CC", "1.4x increased risk for lupus", 17]}')
        

    def test_report_to_csv(self):
        pass

if __name__ == '__main__':
    unittest.main()
