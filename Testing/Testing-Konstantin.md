The following modules were tested: user_data_parser.py, opensnp_parser.py, GeneSearcherProcessData.py, data_collector.py

1)user_data_parser is the model design to input a user gene file and parse the data, to retrieve the list of rsids for further 
processing 
	a) test_file_format: test is designed to check whether the program recognizes if the file provided by the user 
	is not an valid 23andme file or file retrieved from another provider, not some random file, the user could accidently input a wrong
	file without realizing it.
	b)  test_properly_foremated_file: test is designed to check whether user_data_parser is able to retrieve rsids from a properly formated,
	valid file correctly
	c)test_type: test is designed to check that an arguement provided to the parser is an actual file and not something 
	
2)opensnp_parser is the module designed to retrieve raw json data for rsids, extracted by user_data_parser, from opensnp webside using their API,
and to extract traits from the data and match genotype.
	a)test_rsid_fetch_RSID checks whether the data for a single rsid is extracted correctly and if the rsid is incorrect an  error is raised,
	not neccessary if the provided file is valid, but it may appear to be valid but have some mistakes in it
	b) test_fetch_bulk_worker checks if the module properly recieves data for list of rsids using multithreading, similar to fetch_RSID but intended
	to be faster
	
3) data_collector is the module designed to build the data set for all possibly useful rsids, by retrieving data for rsids and constructing a dictionary
rsid - data, it uses multithreaded functions of opensnp_parser to retrieve the data from opensnp webasite
	a) test_update_bulk tests if the module updates the dictionary (rsid-data) properly, given a list of rsids we want to add to the data set, tested using a
	list of various rsids
	b) test_get_snp_list checks if the module retrives the list of rsids  we want to add to the data set correctly, provided with a file listing all the rsids
	we want to add to the data set
	c)test_load checks if the module updates the data set correctly when provided with a json file containing a set of data, the module should check if the json file
	contains  a valid data representation
4) GenesearcherProcessData is a module that checks the rsids of a user  against the data set and generates a report given the rsids provided
	a) test_process_user_data_locally tests if the report is generated correctly for a provided user 23andme file using the local data set( stored on user's machine)
	b) test_process_user_data_server tests if the report generated correctly for a provided user 23andme file using the data set stored on the servers side
	
	it was hard to determine equivalence classes for rsids  since data may be present and maybe not present for totally valid rsids, the program can not be strict on inputs 
	in most cases, unit test checking the file format were implemented but the current implementation of the project does not check it and just  gives no output for incorrect
	file input since no data can be matched.