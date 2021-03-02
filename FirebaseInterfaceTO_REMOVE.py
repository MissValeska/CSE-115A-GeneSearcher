import sys, json, requests, user_data_parser, time, queue, threading

base_url = "https://playground-53aee-default-rtdb.firebaseio.com/"
lookup_q = queue.Queue()

def worker():
    session = requests.Session()
    while True:
        item = lookup_q.get()
        request_url = base_url + item + ".json"
        response = session.get(request_url)
        print("Response: ", response.text)
        lookup_q.task_done()



if __name__ == "__main__":
    # Get args
    data_file = sys.argv[1]
    to_query_file = sys.argv[2]
    
    # Load data 
    user_data = user_data_parser.parse_user_data(data_file)
    to_query = list()
    with open(to_query_file) as f:
        to_query = json.load(f)

    # # Single threaded test
    # session = requests.session()
    # count = 0
    # tic = time.perf_counter()
    # for rsid in to_query:
    #     if rsid in user_data:
    #         request_url = base_url + rsid + ".json"
    #         response = session.get(request_url)
    #         print("Response: ", response.text)
    # toc = time.perf_counter()
    # single_t_time = toc - tic
    
    # Multithreaded test
    for i in range(20):
        threading.Thread(target=worker, daemon=True).start()
    print("Threads initialized")

    tic = time.perf_counter()
    for rsid in to_query:
        if rsid in user_data:
            lookup_q.put(rsid)

    lookup_q.join()
    toc = time.perf_counter()

    # print("Total lookup time 1 thread: ", single_t_time)
    print("Total lookup time 20 threads:", toc - tic)

    # 1 Thread:   82.81
    # 10 Threads: 9.85
    # 15 Threads: 5.81
    # 20 Threads:
