# match_samples
match_samples.py is the main program. _match_samples.py contains the unit tests for match_samples.py
unitTest_files contains the files used in the unit tests.

## Input 
The program takes up to eight inputs. 

verbose - flag that tells the program to display information such as how many samples were filtered out by the function that filters down the input metadata based on the keep file

output - the location and name of file to outport to

inputdata - the metadata that contains the samples that will be processed by the program

keep - name of file with sqlite lines used to determine what samples to exclude or keep

control - name of file with sqlite lines used to determine what samples to label control

case - name of file with sqlite lines used to determine what samples to label case

nullvalues - name of file with strings that represent null values so that samples where one of these null values are in a category that is used to determine matches are filtered out

match- name of file which contains information on what conditions must be met to constitue a match

## Input File Format
inputdata must be a tab separated file such as a .tsv. T
he top column contains the metadata catagories and the left most row contains the sample ids.

keep, control, and case should all contain one sqlite statement per line. 
Two statements that are usefull to use are the IN and NOT IN statements. 
The format for these statements is a metadata catagory followed by IN or NOT IN and then a list of values. 
For example the metadata input file has a column named sex that records the sex of the orginism the sample came from.
In this example sex IN ('male') will keep only the samples that came from a male organism. 
List must be surrounded by () and each value by ''. 
If the list contains multiple values separate each value with a comma. 
If a file has multiple statements then the program will join them with AND.
Therefore 

sex IN ('male')  
sample_type IN ('fecal', 'salivary') 

will keep only the samples that came from a male organism and were a salivary or fecal sample.

nullvalues should contain one line that is a list of null values. 
The list should be surrounded by (), each value surrounded by '', and multiple value separated by commas.
Example ('Unspecified', 'null', 'NULL')

match's format is like a table

| type of match | catagory | number if type of match is range |
|-|-|-|
| type of match |  catagory | number if type of match is range |
| type of match | catagory | number if type of match is range |

There are two types of matches range and exact. 
An exact match is where a case and control sample have the exact same value for the given catagory.
A range match is where the case sample's value is with in the given number range of the control sample's value for the given catagory.



