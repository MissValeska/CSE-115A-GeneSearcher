import sys, json, requests, user_data_parser, time
base_url = "https://playground-53aee-default-rtdb.firebaseio.com/"

if __name__ == "__main__":
    data_file = sys.argv[1]
    to_query_file = sys.argv[2]
    
    user_data = user_data_parser.parse_user_data(data_file)
    to_query = list()
    with open(to_query_file) as f:
        to_query = json.load(f)

    session = requests.session()
    count = 0
    tic = time.perf_counter()
    for rsid in to_query:
        if rsid in user_data:
            count += 1
            request_url = base_url + rsid + ".json"
            response = session.get(request_url)
            print("Completed queries: ", count, " - Response: ", response.text)
    toc = time.perf_counter()

    print("Total lookup time: ", toc - tic)
