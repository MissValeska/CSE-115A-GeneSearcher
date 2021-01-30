import json
import requests

# TODO
# Add info about users genotype
# Parse results and match to users genotype
# Then display only the relevant information
# Also capture confidence measure and display

class opensnp_Parser:
    base_url = "https://opensnp.org/snps/json/annotation/"

    def __init__(self):
        # Create session to speed up subsequent requests
        self.session = requests.Session() 

    def fetch_RSID_info(self, rsid):
        url = self.base_url + rsid + ".json"

        # Fetch information using requests module
        # and parse with json module
        response = self.session.get(url)
        data = json.loads(response.text)

        # Extract information that we are interested in. In our
        # case the traits assocaiated with that particular RSID
        traits = {}
        for each in data["snp"]["annotations"]["snpedia"]:
            traits[each["url"][-4] + each["url"][-2]] = each["summary"][0:len(each["summary"])-1]
            #print(each["summary"])
            

        print(traits)
        return traits

    # Determines the complement of the passed in genotype and returns a tuple of
    # allele pairs that are equivalent when searching for matches.
    # Code provided by Valeska
    def complement(alleles):
        compDict = {'A' : 'T',
                    'G' : 'C',
                    'T' : 'A',
                    'C' : 'G' }
        return compDict[alleles[0]] + compDict[alleles[1]], \
               compDict[alleles[1]] + compDict[alleles[0]], \
               alleles, \
               alleles[-1::-1]
    
    # Match users specific genotype with with one from the list of traits. We first
    # compute the complements of the passed in genotype and create a list containing
    # both the allele pair passed in, its complement, and their reverse, as all four
    # of these options should be equivalent. We then check if any of those values
    # are in the traits dictionary and return any match
    def match_genotype(self, traits, genotype):
        compliments = opensnp_Parser.complement(genotype)
        # print(compliments)
        for pair in compliments:
            if pair  in traits:
                return traits[pair]
        return None


# Main function for testing
if __name__ == "__main__":
    # Parser object
    parser = opensnp_Parser()

    # Example rsid that has no data
    rsid = "rs548049170"
    traits = parser.fetch_RSID_info(rsid)
    print("\nExample rsid: ", rsid)
    print("Number of traits returned: ", len(traits))
    if len(traits) > 0:
        for trait in traits:
            print(trait, "-", traits[trait])
        print("User match on ", parser.match_genotype(traits, 'CT'))
    else:
        print("No data found for this RSID")

    # Example rsid with data 
    rsid = "rs4988235"
    traits = parser.fetch_RSID_info(rsid)
    print("Example rsid: ", rsid)
    print("Number of traits returned: ", len(traits))
    if len(traits) > 0:
        for trait in traits:
            print(trait, "-", traits[trait])
        print("User match on ", parser.match_genotype(traits, 'CT'))
    else:
        print("No data found for this RSID")