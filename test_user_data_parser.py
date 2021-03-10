import unittest
from user_data_parser import parse_user_data

class Test_user_data_parser_test(unittest.TestCase):


    def test_properly_formated_file(self):
        # Test if the parser extraxts neccesarry information 
        # from a properly formated file correctly
        dictionary = {"rs548049170"  :  ['1', '69869', 'TT'],
                        "rs9283150"  :  ['1', '565508', 'AA'],
                        "rs116587930"  :  ['1', '727841', 'GG'],
                        "rs3131972"  :  ['1', '752721', 'AG'],
                        "rs12184325"  :  ['1', '754105', 'CT'],
                        
                        "rs12567639"  :  ['1', '756268', 'AA'],
                        "rs114525117"  :  ['1', '759036', 'AG'],
                        "rs12124819"  :  ['1', '776546', 'AA'],
                        "rs12127425"  :  ['1', '794332', 'GG']}
        self.assertEqual(parse_user_data('23andmeSample.txt'), dictionary)
        
    def test_type(self):
        # Test if the parser handeles inproper arguments
        self.assertRaises(TypeError, parse_user_data, int, float, complex, list, tuple, range,
        dict, set, frozenset, bool, bytes, bytearray, memoryview)
    
    def test_file_format(self):
        # Test if the parser handles inproperly formated files
        self.assertRaises(IOError, parse_user_data, 'wrongformat.txt')

if  __name__ == "__main__":

    unittest.main()
        