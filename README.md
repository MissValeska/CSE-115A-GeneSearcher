# CSE-115A-GeneSearcher
GeneSearcher allows the user discover information about themselves, based on their genetic data, using open resources. This is a class project for CSE 115A Intro to Software Engineering.

Users are able to input a text file containing their genetic information (these files are commonly available from commercial DNA testing services such as 23AndMe) then the program automatically process their genotype and check it's own dataset for entries matching the users particular genotype that might have interesting information. It then creates simple report based on it's findings wich are presented to the user.

## Usage
### MacOS
On MacOS the program must be run at the command line from its containing directory:
`python3 main.py`

### Windows
On Windows the program can be run from the command line, or installed as a regular desktop applicaton.

## Future Improvements
Future improvements include:
* The ability to export the report in either CSV or JSON format for processing in external tools
* A filtered report option. The user should be able to query for specific traits they are interested in and the program will generate a report containing only data relevant to that query.
* An information window that can help the user understand where / how to access there raw genetic material from websites such as 23AndMe
* GUI enhancements
