import json
import requests

# TODO
# Add info about users genotype
# Parse results and match to users genotype
# Then display only the relevant information
# Also capture confidence measure and display

class opensnp_Parser:
    base_url = "https://opensnp.org/snps/json/annotation/"

    def fetch_RSID_info(self, rsid):
        url = self.base_url + rsid + ".json"

        # Fetch information using requests module
        # and parse with json module
        response = requests.get(url)
        data = json.loads(response.text)

        # Extract information that we are interested in. In our
        # case the traits assocaiated with that particular RSID
        traits = {}
        for each in data["snp"]["annotations"]["snpedia"]:
            traits[(each["url"][-4],each["url"][-2])] = each["summary"][0:len(each["summary"])-1]
            #print(each["summary"])

        return traits

    # match users specific genotype with with one from the list of traits
    def match_genotype(traits, genotype):
    
        return traits[genotype]


# Main function for testing
if __name__ == "__main__":
    # Example rsid 
    rsid = "rs4988235"
    parser = opensnp_Parser()
    traits = parser.fetch_RSID_info(rsid)
    for trait in traits:
        print(trait, "-", traits[trait])
