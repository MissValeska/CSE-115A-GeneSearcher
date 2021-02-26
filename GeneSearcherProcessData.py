import sys, time, requests, json, csv

# Determines the complement of the passed in genotype and returns a tuple of
# allele strings that are equivalent when searching for matches.
# Code provided by Valeska
def complement(alleles):
    compDict = {'A' : 'T',
                'G' : 'C',
                'T' : 'A',
                'C' : 'G' }
    alleles = alleles.upper()

    if(len(alleles) == 2 and "D" not in alleles and "I" not in alleles):
        return compDict[alleles[0]] + compDict[alleles[1]], compDict[alleles[1]] + compDict[alleles[0]], alleles, alleles[-1::-1]
    elif("D" in alleles or "I" in alleles and len(alleles) == 2):
        return alleles, alleles[-1::-1]
    elif("D" in alleles or "I" in alleles and len(alleles) == 1):
        return alleles
    else:
        return compDict[alleles[0]], alleles

# Match users specific genotype with with one from the list of traits. We first
# compute the complements of the passed in genotype and create a list containing
# both the allele pair passed in, its complement, and their reverse, as all four
# of these options should be equivalent. We then check if any of those values
# are in the traits dictionary and return any match
def match_genotype(traits, genotype):
    complements = complement(genotype)
    # print(comlements)
    for pair in complements:
        if pair  in traits:
            return traits[pair]
    return None

def process_user_data(user_data, data_set):
    report = dict()
    for rsid in user_data:
        if rsid in data_set:
            user_genotype = user_data[rsid][2]
            # print(rsid, " -", user_genotype)
            if user_genotype not in {"--"}:
                expression = match_genotype(data_set[rsid]["traits"], user_genotype)
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
                    weight = data_set[rsid]["weight"]
                    report[rsid] = (user_genotype, expression, weight)
    return report

# if __name__ == "__main__":
#     user_data_file = sys.argv[1]
#     if len(sys.argv) == 3:
#         data_file = sys.argv[2]
#     else:
#         data_file = None

#     # Read users genetic data from file
#     user_genetic_data = load_user_data(user_data_file)
#     # Load the data set
#     if data_file != None:
#         data_set = load_data_set_from_file(data_file)
#     else:
#         data_set = load_data_set_from_server()

#     # Process users data and generate report data
#     report = process_user_data(user_genetic_data, data_set)

#     # Output report to terminal and files
#     for item in report:
#         print(item, " - ", report[item])
#     user_report_to_json(report, "report.json")
#     user_report_to_csv(report, "report.csv")
