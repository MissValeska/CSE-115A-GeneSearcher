import json, sys

def load_data_set(filename):
    data = dict()
    with open(filename) as in_file:
        data = json.load(in_file)
    return data

def clean_data_set(data, noise_set):
    cleaned_data = dict(data)
    removal_list = list()
    for RSID in cleaned_data:
        print(RSID, cleaned_data[RSID])
        if not cleaned_data[RSID]: # If the dict is empty just remove the entry
            print("EMPTY DATA! - Removing!")
            removal_list.append(RSID)

        else: # Otherwise check entries for usefulness
            to_remove = True
            for genotype in cleaned_data[RSID]:
                to_remove = to_remove and cleaned_data[RSID][genotype] in noise_set
            if to_remove:
                print("All data unuseful - Removing!")
                removal_list.append(RSID)
    
    for RSID in removal_list:
        del cleaned_data[RSID]        
    
    return cleaned_data

def write_data_set(data, filename):
    with open(filename, "w") as out_file:
        json.dump(data, out_file)

if __name__ == "__main__":
    data_file = sys.argv[1]
    out_file = sys.argv[2]
    noise = { "common in clinva",
            "common in clinvar",
            "common in complete genomic",
            "common in complete genomics",
            "No summary provided",
            # "norma",
            # "normal",
            # "Normal",
            "commo",
            "averag",
            "average",
            "common/normal",
            "common on affy axiom dat",
            "common on affy axiom data",
            None }

    data_set = load_data_set(data_file)
    cleaned_data = clean_data_set(data_set, noise)
    write_data_set(cleaned_data, out_file)

