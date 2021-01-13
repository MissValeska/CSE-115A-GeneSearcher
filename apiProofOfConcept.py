import json
import requests

# Proof of concept for working with the opensnp API
# using the python requests module we can simply query the
# opensnp api and recieve json formated responses from which
# we can extract the information we are looking to present to
# the user.

# Input: an RSID
# Output: a collection of traits associated with that RSID
def fetch_RSID_info(rsid):
    # Format request to opensnp api
    base_url = "https://opensnp.org/snps/json/annotation/"
    url = base_url + rsid + ".json"

    # Fetch information using requests module
    # and parse with json module
    response = requests.get(url)
    data = json.loads(response.text)

    # Extract information that we are interested in. In our
    # case the traits assocaiated with that particular RSID
    traits = []
    for each in data["snp"]["annotations"]["snpedia"]:
        traits.append((each["url"], each["summary"]))
        #print(each["summary"])

    return traits

# Example rsid 
rsid = "rs4988235"
traits = fetch_RSID_info(rsid)
for trait in traits:
    print(trait)


# TODO
# Add info about users genotype
# Parse results and match to users genotype
# Then display only the relevant information
# Also capture confidence measure and display
