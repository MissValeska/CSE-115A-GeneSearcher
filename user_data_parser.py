#---------------------------------------------------------------------------
# parse.py
# 01/12/21
# Description: Given a raw data file from 23&me this program parses the
# necessary data.
#---------------------------------------------------------------------------

class User_Data_Parser(self, filename):
    rsids = dict()
    
    with open(filename) as f:
        i = 0
        while True:
            line = f.readline()
            # Skip header line
            if not line.startswith('#'):
                break
        
        # Begin to parse the real data
        while line:
            data = line.split()
            rsids[data[0]] = data[1::]
            line = f.readline()

        return rsids
        #remove \n from genotypes
        # for e in genotype:
        # 	genotype[e] = genotype[e].rstrip("\n")

filename = input('Enter a filename: ')
user_rsids = parse(filename)

for rsid in user_rsids:
    print(rsid, " : ", user_rsids[rsid])


