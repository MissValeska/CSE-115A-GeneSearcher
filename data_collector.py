from opensnp_parser import opensnp_Parser
import json, requests, sys, threading, queue, time

class data_collector():

    def __init__(self, t_lim):
        self.interesting_RSIDs = list()
        self.RSID_data = {}
        self.q = queue.Queue()
        self.thread_limit = t_lim
    
    # Worker thread for update function.
    # Instantiates an opensnp_parser (single thread) and then pulls
    # entries off the update queue. Not very efficient because as currently
    # designed it does not use bulk queries.
    def update_worker(self):
        parser = opensnp_Parser(1)
        while True:
            while not self.q.empty():
                rsid = self.q.get()
                data = parser.fetch_RSID_info(rsid)
                self.RSID_data[rsid] = data
                if len(data) > 0:
                    self.interesting_RSIDs.append(rsid)
                print(data)
                self.q.task_done()
    
    # Takes a list of RSIDs and updates the RSID_data and interesting_RSIDs
    # This function spawns multiple worker threads that each instantiate their
    # own opensnp_parser. It would probably be better to use update_bulk but
    # I'm leaving this function here just incase.
    def update(self, RSIDs):
        
        # Init threads
        for i in range(self.thread_limit):
            threading.Thread(target=self.update_worker, daemon=True).start()

        # Enqueu RSIDS
        for RSID in RSIDs:
            self.q.put(RSID)
        print("RSID lookups enqued")
        self.q.join()
        print("Processing finished")

    # Collects data for all passed in RSIDs using multithreaded opensnp
    # parser. All of the work is done by the parser wich will return a
    # dict with all of the snp data. Afterwards the data_collecter will
    # check for entries that have values and append them to the
    # interesting_RSIDs dict
    def update_bulk(self, RSIDs):
        parser = opensnp_Parser(15)
        self.RSID_data = parser.fetch_bulk_RSID_info(RSIDs)
        for RSID in self.RSID_data:
            if len(self.RSID_data[RSID]) > 0:
                self.interesting_RSIDs.append(RSID)
    
    # reloads the structure from a JSON file
    def load(self, file):
        
        with open (file) as json_file:
            self.RSID_data = json.load(json_file)
    
    # writes the dataset and list of interesting RSIDs to JSON files
    def write(self, rsid_data_file, interesting_rsids_file):
        
        with open(rsid_data_file, "w") as out:
            json.dump(self.RSID_data, out)

        with open(interesting_rsids_file, "w") as out:
            json.dump(self.interesting_RSIDs, out)

    def print(self):
        print("RSID data stored in collector:")
        for rsid in self.RSID_data:
            print(rsid, " - ", self.RSID_data[rsid])

def get_snp_list(filename):
    
    list = []
    with open(filename) as f:
        line = f.readline()
        while line:
            line = line.strip('\n')
            list.append(line)
            line = f.readline()
    return list


if __name__ == "__main__":

    filename = sys.argv[1]
    rsid_list = get_snp_list(filename)
    rsid_list.reverse()
    #rsid_list = rsid_list[0:10000] # uncomment this line to limit test length
    
    dc = data_collector(8)
    tic = time.perf_counter()
    dc.update_bulk(rsid_list)
    toc = time.perf_counter()
    dc.write("RSID_Data.json", "Interesting_RSIDs.json")
    time_two = toc - tic
    
    print("Collection complete")
    print(f"Processing Time: {time_two:0.4f} seconds")

    ## Some Stats when using bulk-update
    # @ 10,000 we get around 119 RSIDs per second (84 seconds)
    # @ 100,000 we get around 129 RSIDs per second (775 seconds)
    # @ 978,105 we get around 114 RSIDs per second (8563.8400)