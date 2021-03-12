
# GeneSearcher Testing

## Module: firebase

I worked significantly in private .ipynb files as a jupyter-notebook, where I was able to significantly test my own code before deploying it to github or sharing it with team members. I did this extensively with firebase code.

## Manual Applicaton / Ad Hoc Testing

Throughout the development cycle, I manually tested many of the functionalities I was currently working on. The prominent tests were:

1. Accessing Firebase data
    * Firebase should produce a .json
    * The data should be formatted correctly with an rsid as the first parameter and the genotype and other information under that.
    * The aforementioned data structure must be maintained as a sort of pseudo-schema in the NoSQL environment of Firebase.

2. Storing data in Firebase
    * The data to be stored in Firebase must be .json
    * The data must be formatted in the aforementioned way
    * Elements in the .json file that do not contain valuable information, such as "unknown" or "common" instead of a full description must be removed before storing in Firebase.

3. Genetic algorithm for comparing Firebase data
    * The genetic genotype information has an inverse or complement, this must be accounted for when comparing data to avoid false negative matches by using my complement function.
    * The complement function must consider diploid and monoploid genomes, such as that of the mitochondria.
    * The complement function must handle unknown values, such as "N".

The nature of Firebase is very dynamic, since it is NoSQL, it doesn't have a schema or a way to enforce a schema, it is just .json. So I had to account for that and ensure all functions that produce data which enventually goes into Firebase follow the proper schema format. Moreover, as the only team member with knowledge of genomics, I had to ensure all functions that worked with genomic data, which is most of them, worked properly. This consisted of testing functions myself, such as in a jupyter-notebook, or testing the output of functions given to me by other team-members and suggesting code changes to correct any observed issues or bugs.
