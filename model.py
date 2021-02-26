import user_data_parser
import GeneSearcherProcessData as proc
import sys, time, requests, json, csv

class Genesearcher_Model:
    def __init__(self, vc):
        self.vc = vc
        self.user_data = dict()
        self.data_set = dict()
        self.report = dict()
        self.input_file = ""

    '''
    Setter and getter methods
    '''
    def set_user_data(self, data):
        self.user_data = data

    def set_data_set(self, data):
        self.data_set = data

    def set_report(self, data):
        self.report = data

    def set_input_file(self, f):
        self.input_file = f

    def get_user_data(self):
        return self.user_data

    def get_data_set(self):
        return self.data_set

    def get_report(self):
        return self.report

    def get_input_file(self):
        return self.input_file

    '''
    Processing functions
    '''
    def load_user_data(self, data_file):
        self.input_file = data_file
        self.user_data = user_data_parser.parse_user_data(data_file)

    def load_data_set_from_file(self, data_file):
        with open(data_file) as f:
            self.data_set = json.load(f) 

    def load_data_set_from_server(self):
        url = "https://playground-53aee-default-rtdb.firebaseio.com/.json"
        json_data = requests.get(url)
        self.data_set = json.loads(json_data.text)

    def generate_report(self):
        report = proc.process_user_data(self.user_data, self.data_set)
        self.report = report
        return self.report
    
    '''
    Report output functions
    '''
    def user_report_to_json(self, filename):
        user_data = self.report
        with open(filename, "w") as outfile:
            json.dump(user_data, outfile)

    def user_report_to_csv(self, filename):
        user_data = self.report
        with open(filename, "w") as outfile:
            for rsid in user_data:
                outfile.write("%s,%s,%s,%s\n"%(rsid, user_data[rsid][0], user_data[rsid][1], user_data[rsid][2]))