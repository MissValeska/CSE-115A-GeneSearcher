#---------------------------------------------------------------------------
# parse.py
# 01/12/21
# Description: Given a raw data file from 23&me this program parses the
# necessary data.
#---------------------------------------------------------------------------
import pandas as pd

from tabulate import tabulate
#Create arrays for the rest of the stats being scraped
rsid = {}
chromosome = {}
position = {}
genotype = {}
data = []

# Creating an empty dictionary 
myDict = {}
def parse(filename):
	# Open the file and skip comments
	with open(filename) as f:
		i = 0;
		while True:
			line = f.readline();
			if not line.startswith('#'):
				break;
		
		#begin to parse the real data
		while line:
			j = 0;
			x = line.split("\t")
			rsid[i] = x[j]
			chromosome[i] = x[j+1]
			position[i] = x[j+2]
			genotype[i] = x[j+3]
			i = i + 1;
			line = f.readline();

		#remove \n from genotypes
		for e in genotype:
			genotype[e] = genotype[e].rstrip("\n")

		#enter everything into dictionary
		for x in rsid:
			myDict[rsid[x]] = [genotype[x]]
		#print(myDict)
		
		# This was previously used before the dictionary. This was a dataframe from Pandas library that held all the data.
		# Going to keep this here just in case we revert to this instead of the dictionary data structure.
		# for x in rsid:
		# 	data.append([rsid[x], chromosome[x], position[x], genotype[x]])
		# full_stat = pd.DataFrame(data, columns = ['rsid', 'chromosome', 'position', 'genotype'])
		# print(tabulate(full_stat, showindex=False, headers=full_stat.columns))

filename = input('Enter a filename: ')
parse(filename);

