import user_data_parser
from opensnp_parser import opensnp_Parser
import sys, time, requests, json, csv

def load_user_data(data_file):
    user_data = user_data_parser.parse_user_data(data_file)
    return user_data

def load_data_set_from_file(data_file):
    data_set = dict()
    with open(data_file) as f:
        data_set = json.load(f) 
    return data_set

def load_data_set_from_server():
    url = "https://playground-53aee-default-rtdb.firebaseio.com/.json"
    json_data = requests.get(url)
    data_set = json.loads(json_data.text)
    return data_set

def process_user_data(user_data, data_set):
    # Including opensnp parser to use it's functions for matching user genotype
    # to dataset. But we should probably put that functionality elsewhere at
    # this point.
    parser = opensnp_Parser(1)

    report = dict()
    for rsid in user_data:
        if rsid in data_set:
            user_genotype = user_data[rsid][2]
            # print(rsid, " -", user_genotype)
            if user_genotype not in {"--", "DD", "II"}:
                expression = parser.match_genotype(data_set[rsid], user_genotype)
                if expression not in {"common in clinva",
                                "common in clinvar",
                                "common in complete genomic",
                                "common in complete genomics",
                                "No summary provided",
                                # "norma",
                                # "normal",
                                # "Normal",
                                "commo",
                                "averag",
                                "average",
                                "common/normal",
                                "common on affy axiom dat",
                                "common on affy axiom data",
                                None}:
                    report[rsid] = (user_genotype, expression)
    return report

def user_report_to_json(user_data, filename):
    with open(filename, "w") as outfile:
        json.dump(user_data, outfile)

def user_report_to_csv(user_data, filename):
    with open(filename, "w") as outfile:
        for rsid in user_data:
            outfile.write("%s,%s,%s\n"%(rsid, user_data[rsid][0], user_data[rsid][1]))

if __name__ == "__main__":
    user_data_file = sys.argv[1]
    if len(sys.argv) == 3:
        data_file = sys.argv[2]
    else:
        data_file = None

    parser = opensnp_Parser(5)

    # Read users genetic data from file
    user_genetic_data = load_user_data(user_data_file)
    # Load the data set
    if data_file != None:
        data_set = load_data_set_from_file(data_file)
    else:
        data_set = load_data_set_from_server()

    # Process users data and generate report data
    report = process_user_data(user_genetic_data, data_set)

    # Output report to terminal and files 
    for item in report:
        print(item, " - ", report[item])
    user_report_to_json(report, "report.json")
    user_report_to_csv(report, "report.csv")
