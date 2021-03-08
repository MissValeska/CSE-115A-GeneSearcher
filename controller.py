import tkinter as tk
from model import Genesearcher_Model
from gui import App
import os

class GeneSearcher_Controller:
    def __init__(self):
        self.model = Genesearcher_Model(self)
        self.load_data_set()
        self.root = tk.Tk()
        self.view = App(self.root, self)
        self.root.mainloop()

    def load_data_set(self, filepath=None):
        if filepath == None:
            self.model.load_data_set_from_server()
        else:
            self.model.load_data_set_from_file(filepath)
    
    def input_data_file(self, filepath):
        self.model.load_user_data(filepath)

    def generate_report(self):
        '''
        Primary backend linkage. Utilize functions from GeneSearcherProcessData.py
        to load in user data from file and data from server to compare to. Generates
        the report and sends it to display function. Bound to search_button in gui.py
        PARAMS : text frame to display report in.
        '''
        print("Generating Report for: " + self.model.get_input_file())
        report = self.model.generate_report()
        self.view.display_report(report)

    def export_report(self, filepath = "report"):
        self.model.user_report_to_csv(filepath + ".csv")
        # self.model.user_report_to_json(filepath + ".json")