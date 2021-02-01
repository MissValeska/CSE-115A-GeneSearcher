from opensnp_parser import opensnp_Parser
import json, requests, sys, threading, queue, time

class data_collector():

    def __init__(self, t_lim):
        self.interesting_RSIDs = list()
        self.RSID_data = {}
        self.q = queue.Queue()
        self.thread_limit = t_lim
    
    def update_worker(self):
        parser = opensnp_Parser()
        while True:
            while not self.q.empty():
                rsid = self.q.get()
                data = parser.fetch_RSID_info(rsid)
                self.RSID_data[rsid] = data
                print(data)
                self.q.task_done()

    
    # Takes a list of RSIDs and updates the RSID_data and interesting_RSIDs
    def update(self, RSIDs):
        
        # init threads
        for i in range(self.thread_limit):
            threading.Thread(target=self.update_worker, daemon=True).start()

        # Enqueu RSIDS
        for RSID in RSIDs:
            self.q.put(RSID)
        print("RSID lookups enqued")
        self.q.join()
        print("Processing finished")
    
    # reloads the structure from a JSON file
    def load(self, file):
        pass
    
    # writes the dataset to a JSON file
    def write(self, file):
        pass

    def print(self):
        print("RSID data stored in collector:")
        for rsid in self.RSID_data:
            print(rsid, " - ", self.RSID_data[rsid])


if __name__ == "__main__":
    rsid_list = ["i713057",
                 "rs548049170",
                 "rs4988235",
                 "rs53576",
                 "rs116587930",
                 "rs1815739",
                 "rs7412",
                 "rs12567639",
                 "rs13302914",
                 "rs429358",
                 "rs186101910",
                 "rs6152",
                 "rs333",
                 "rs3935066",
                 "rs77334480",
                 "rs6671356",
                 "rs1240707",
                 "rs1800497",
                 "rs1805007",
                 "rs9939609",
                 "rs662799",
                 "rs7495174",
                 "rs145313947",
                 "rs12913832",
                 "rs7903146",
                 "rs12255372",
                 "rs202061838",
                 "rs1799971",
                 "rs17822931",
                 "rs4680",
                 "rs1333049",
                 "rs1051730"]
    dc = data_collector(10)
    tic = time.perf_counter()
    dc.update(rsid_list)
    toc = time.perf_counter()
    
    print("Collection complete")
    dc.print()
    print(f"Processing Time: {toc - tic:0.4f} seconds")