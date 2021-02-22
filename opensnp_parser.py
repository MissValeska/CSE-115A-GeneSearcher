import json, requests, threading, queue, time, string

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

    # extracts just the information about the traits associated with a
    # particular genotype from rsid data.
    def extract_traits(data):
        traits = {}
        for each in data:
            traits[each["url"][-4] + each["url"][-2]] = each["summary"][0:len(each["summary"])-1]
        return traits

    # Computes the weight of evidence based on the annotation data that is returned by the opensnp
    # API. The API does not deliver the weight of evidence, but the formula is readily published
    # on the opensnp website, so it has been reimplemented here because it is easier to compute
    # than it would be to scrape the website.
    # Weight of evidence = 1 * ( num mendeley articles)
    #                    + 2 * ( num plos articles + num pgp_annotations + genome_gov_publications )
    #                    + 5 * ( snpedia articles )
    def compute_weight_of_evidence(annotation_data):
        num_mendeley = len(annotation_data["mendeley"])
        num_plos = len(annotation_data["plos"])
        num_pgp = len(annotation_data["pgp_annotations"])
        num_genome_gov = len(annotation_data["genome_gov_publications"])
        num_snpedia = len(annotation_data["snpedia"])
        return num_mendeley + (2 * (num_plos + num_pgp + num_genome_gov)) + (5 * num_snpedia)

    
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
        traits = opensnp_Parser.extract_traits(data["snp"]["annotations"]["snpedia"])
        weight_of_evidence = opensnp_Parser.compute_weight_of_evidence(data["snp"]["annotations"])
        rsid_info = {"weight" : weight_of_evidence, "traits" : traits}
        return rsid_info
    
    # Worker function for multi-threaded bulk lookup method
    # Opens a session, then while there are RSIDs on the look up queue
    # pops up to 600 RSIDs from the queue and adds them to local list.
    # Constructs request with all of the RSIDs that it popped from the queue.
    # It then makes the request, processes the json, extracts the relevant
    # information and stores it in the Parsers RSID_data dictionary for
    # later retrieval 
    def fetch_bulk_worker(self):
        bulk_session = requests.Session()
        rsid_list = list()
        while True:

            ## Pop up to 600 items off work queue and add to local rsid_list
            #  for processing.
            while len(rsid_list) < 600:
                item = self.lookup_q.get()
                rsid_list.append(item)
                if self.lookup_q.empty():
                    break
            
            # If the rsid_list is not empty try to construct request and send
            if len(rsid_list) > 0:
                # rsid_string = 
                request_url = self.base_url + ",".join(rsid_list) + ".json"

                try:
                    # Request data and parse json
                    response = bulk_session.get(request_url)
                    try:
                        data = json.loads(response.text)
                    except:
                        print("Error converting response to json")
                        print(response.text)
                        print(request_url)

                    # For each item in rsid_list extract from data object and
                    # record in objects rsid_dasta field
                    for rsid in data:
                        try:
                            if rsid == "snp": # This only happens when a single request is returned
                                rsid_traits = opensnp_Parser.extract_traits(data["snp"]["annotations"]["snpedia"])
                                weight_of_evidence = opensnp_Parser.compute_weight_of_evidence(data["snp"]["annotations"])
                                self.RSID_data[rsid_list[0]] = {"weight" : weight_of_evidence, "traits" : rsid_traits}
                            else:
                                rsid_traits = opensnp_Parser.extract_traits(data[rsid]["annotations"]["snpedia"])
                                weight_of_evidence = opensnp_Parser.compute_weight_of_evidence(data[rsid]["annotations"])
                                self.RSID_data[rsid] = {"weight" : weight_of_evidence, "traits" : rsid_traits}
                        except:
                            print("Error reading returned data:")
                            print("Data for ", rsid, ":")
                            print(data[rsid])
                            print(response.text)
                    
                    # Signal task_done for each RSID taken off queue and update queries made.
                    # important to do this last or program terminates before all data is processed
                    for i in range(len(rsid_list)):
                        self.lookup_q.task_done()
                    self.queriesMade += len(rsid_list)

                    # Print out the number of queries made for monitoring
                    # Remove this when code "works"
                    print("Queries performed: ", self.queriesMade)
                    
                    # Clear the list
                    rsid_list.clear()
                
                except:
                    # Request new session and try again in 30 seconds
                    print("Error making request - Requesting new session")
                    print("List of RSIDs in failed request:")
                    print(rsid_list)
                    # print("Server returned: ")
                    # print(response.text)
                    time.sleep(30)
                    bulk_session = requests.Session()

    
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
        print(len(rsids), " RSID lookups enqued")
        
        # Wait for processing to finish
        self.lookup_q.join() 
        print("Processing finished")

        # Return the massive dictionary of RSIDs and traits
        return self.RSID_data

    # Determines the complement of the passed in genotype and returns a tuple of
    # allele pairs that are equivalent when searching for matches.
    # Code provided by Valeska
    def complement(alleles):
        compDict = {'A' : 'T',
                    'G' : 'C',
                    'T' : 'A',
                    'C' : 'G' }
        alleles = alleles.upper()
        # if len(alleles) == 2:
        #     return compDict[alleles[0]] + compDict[alleles[1]], \
        #            compDict[alleles[1]] + compDict[alleles[0]], \
        #            alleles, \
        #            alleles[-1::-1]
        # else:
        #     return alleles, compDict[alleles]
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
