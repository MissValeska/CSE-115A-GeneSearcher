import tkinter as tk
import _tkinter
from gui import App as App
from controller import GeneSearcher_Controller as controller
import unittest

class TkinterTestCase(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.pumpEvents()

    def tearDown(self):
        if self.root:
            self.root.destroy()
            self.pumpEvents()

class ExistenceTest(TkinterTestCase):
    def test_existence(self):
        a = App(self.root, controller)
        
        self.assertEqual(1, a.winfo_exists(), "Window does not exist")
        self.assertEqual(1, a.input_frame.upload_button.winfo_exists(), "Upload does not exist")
        self.assertEqual(1, a.run_frame.search_button.winfo_exists(), "Search does not exist")
        self.assertEqual(1, a.report_frame.search_bar.winfo_exists(), "Search bar does not exist")
        self.assertEqual(1, a.report_frame.find_button.winfo_exists(), "Find does not exist")
        self.assertEqual(1, a.report_frame.export_button.winfo_exists(), "Export does not exist")
        self.assertEqual(1, a.report_frame.r_display.winfo_exists(), "Report display does not exist")

if __name__ == '__main__':
    unittest.main()