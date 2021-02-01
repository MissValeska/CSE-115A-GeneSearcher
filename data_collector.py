from opensnp_parser import opensnp_Parser
import json, requests, sys, threading, queue

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
                # print(data)
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
        
        with open (file) as json_file:
            self.RSID_data = json.load(json_file)
    
    # writes the dataset to a JSON file
    def write(self, file):
        
        with open(file, "w") as out:
            json.dump(self.RSID_data, out)
            
        

    def print(self):
        print("RSID data stored in collector:")
        for rsid in self.RSID_data:
            print(rsid, " - ", self.RSID_data[rsid])


if __name__ == "__main__":
    rsid_list = ["rs548049170", "rs4988235"]
    dc = data_collector(5)
    dc.update(rsid_list)
    print("Collection complete")
    dc.print()
    dc.write("rsidj.json")