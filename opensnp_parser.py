import json, requests, threading, queue

# @ 200 RSIDs per request
# ~1.5 for full file

# @ 400 RSIDs per request
# 

# TODO
# Add info about users genotype
# Parse results and match to users genotype
# Then display only the relevant information
# Also capture confidence measure and display

class opensnp_Parser:

    def __init__(self, t_lim = 1):
        self.base_url = "https://opensnp.org/snps/json/annotation/"
        # Create session to speed up subsequent requests
        self.session = requests.Session()
        
        # Data objects for multi-threaded bulk lookup
        self.lookup_q = queue.Queue()
        self.thread_limit = t_lim
        self.RSID_data = {}
        self.queriesMade = 0

    # Simple, single threaded rsid lookup will return the a dictionary of traits
    # with format {genotype : phenotype}
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
            traits[(each["url"][-4],each["url"][-2])] = each["summary"][0:len(each["summary"])-1]

        # print(traits)
        return traits
    
    # Worker function for multi-threaded bulk lookup method
    # Opens a session, then while there are RSIDs on the look up queue
    # pops up to 600 RSIDs from the queue and adds them to local list.
    # Constructs request with all of the RSIDs that it popped from the queue.
    # It then makes the request, processes the json, extracts the relevant
    # information and stores it in the Parsers RSID_data dictionary for
    # later retrieval 
    def fetch_bulk_worker(self):
        bulk_session = requests.Session()
        while True:

            ## Pop up to 600 items off work queue and add to local rsid_list
            #  for processing.
            #  Currently set to 200 because the latency per request is lower.
            ## Finding the right combination of number of threads and items per request is challening
            rsid_list = list()
            while (not self.lookup_q.empty()) and len(rsid_list) < 400:
                item = self.lookup_q.get()
                rsid_list.append(item)
                self.lookup_q.task_done()
            
            # If the rsid_list is not empty try to construct request and send
            if len(rsid_list) > 0:
                rsid_string = ",".join(rsid_list)
                
                request_url = self.base_url + rsid_string + ".json"
                response = bulk_session.get(request_url)
                data = json.loads(response.text)
                self.queriesMade += len(rsid_list)

                if len(rsid_list) > 1:
                    for rsid in data:
                        print("Queries performed: ", self.queriesMade, " - ", rsid, " - ", data[rsid]["annotations"]["snpedia"])
                        self.RSID_data[rsid] = data[rsid]["annotations"]["snpedia"]
                else: # len of rsid_list == 1
                    print("Single item query! : (")
                    print("Queries performed: ", self.queriesMade, " - ",rsid_list[0], " - ", data["snp"]["annotations"]["snpedia"])
                    self.RSID_data[rsid_list[0]] = data["snp"]["annotations"]["snpedia"]

    
    # Bulk RSID fetch takes in a list of rsids and requests the entire list
    # at once. Bulk look up places all rsids in lookup queue and then spawns
    # worker threads to break up in to lists of manageable length wich can be 
    # requested all at once (up to 600 rsids at once)
    def fetch_bulk_RSID_info(self, rsids):
        # Spawn worker threads
        for i in range(self.thread_limit):
            threading.Thread(target=self.fetch_bulk_worker, daemon=True).start()
        print(self.thread_limit, " lookup threads spawned")

        # Enqueue list of RSIDS that need to be queried
        for rsid in rsids:
            self.lookup_q.put(rsid)    
        print("RSID lookups enqued")
        
        # Wait for processing to finish
        self.lookup_q.join() 
        print("Processing finished")

        # Return the massive JSON data structure
        return self.RSID_data


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