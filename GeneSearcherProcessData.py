import user_data_parser
from opensnp_parser import opensnp_Parser
import sys, time, requests, json

def load_user_data(data_file):
    user_data = user_data_parser.parse_user_data(data_file)
    return user_data

def load_data_set_from_file(data_file):
    data_set = dict()
    with open(data_file) as f:
        data_set = json.load(f) 
    return data_set

def load_data_set_from_server():
    pass

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
                report[rsid] = parser.match_genotype(data_set[rsid], user_genotype)
    return report

def user_report_to_json():
    pass

def user_report_to_csv():
    pass


if __name__ == "__main__":
    user_data_file = sys.argv[1]
    data_file = sys.argv[2]

    parser = opensnp_Parser(5)

    # Read users genetic data from file
    user_genetic_data = load_user_data(user_data_file)
    data_set = load_data_set_from_file(data_file)
    report = process_user_data(user_genetic_data, data_set)

    for item in report:
        if report[item] not in {"common in clinva",
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
            print(item, " - ", report[item])
