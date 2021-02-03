import user_data_parser
from opensnp_parser import opensnp_Parser
import sys, time, requests, json

if __name__ == "__main__":
    file = sys.argv[1]
    parser = opensnp_Parser(5)

    # Read users genetic data from file
    user_genetic_data = user_data_parser.parse_user_data(file)
    ### Below is short dummy list of testing. To test comment above line
    #   out and uncomment below
    # user_genetic_data = {"rs548049170" : ["","","CT"], "rs4988235" : ["","","CT"]}
    rsids = list()
    
    # Generate list of RSID's to request
    for rsid in user_genetic_data:
        rsids.append(rsid)

    # Have the parser make the requests.
    data = parser.fetch_bulk_RSID_info(rsids)

    for rsid in data:
        if len(data[rsid]) > 0: 
            print(rsid, " - ", data[rsid])
            genotype = user_genetic_data[rsid][2]
            print("  User has ", genotype, " - " , parser.match_genotype(data[rsid], genotype))

        else:
            print(rsid, " - no data for this value")

