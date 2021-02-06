# reads snps from a file
# formated as
# rs23124125512
# rs23156612312
#..............
#(one snp on each line)

from data_collector import data_collector

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
    list = get_snp_list("rsidlist.txt")
    print (list)