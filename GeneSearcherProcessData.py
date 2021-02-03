import user_data_parser
from opensnp_parser import opensnp_Parser
import sys

if __name__ == "__main__":
    file = sys.argv[1]
    parser = opensnp_Parser()

    # Read users genetic data from file
    user_genetic_data = user_data_parser.parse_user_data(file)
    for rsid in user_genetic_data:
        print(rsid, ":", user_genetic_data[rsid], end="")
        traits = parser.fetch_RSID_info(rsid)
        if len(traits) != 0:
            genotype = user_genetic_data[rsid][2][0] + user_genetic_data[rsid][2][1]
            print(" - " , parser.match_genotype(traits, genotype))
            #print(traits)
        else:
            print(" - No data exists for this RSID")

    #for rsid in user_genetic_data
