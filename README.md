# match_samples
match_samples.py is the main program. _match_samples.py contains the unit tests for match_samples.py
unitTest_files contains the files used in the unit tests.

match_samples allows users to filter down a metadata file, label samples case or control, and match case to control samples. 

## Input 
The program takes up to eight inputs. 

1. verbose 
   - flag that tells the program to display information such as how many samples were filtered out by the function that filters down the input metadata based on the keep file
2. output 
   - the location and name of file to outport to
   - required
3. inputdata 
   - the metadata that contains the samples that will be processed by the program
   - required
4. keep 
   - name of file with sqlite lines used to determine what samples to exclude or keep
5. control 
   - name of file with sqlite lines used to determine what samples to label control
   - if given case must also be given
6. case 
   - name of file with sqlite lines used to determine what samples to label case
   - if given control must also be given
7. nullvalues 
   - name of file with strings that represent null values so that samples where one of these null values are in a category that is used to determine matches are filtered out
   - if given then match must also be given
8. match 
   - name of file which contains information on what conditions must be met to constitue a match
   - if given case and control must also be given
9. one 
   - flag that tells program to call stableMarriageRunner and do one to one matches
10. only_matches
    - flag that makes program filter out none matched samples at the end of matching before the metadata is outputted

   
## Input File Format
inputdata must be a tab separated file such as a .tsv. The top column contains the metadata catagories and the left most row contains the sample ids.

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
Range matches require the third column to contain a number like 3 or 5.2. The number can not be a string such as five.
Separate each column with a tab. An example of a match file is

range    age    3

exact    sex

exact    sample_type

This would match case and control samples that have the same value for sex and sample_type and their values for age are within 3 of eachother. 

## Output
Output is a metadata object. This metadata objects reflects the fitering, labeling, and matching done by the program. 

## Program Functions

1. main
   - Calls the other functions depending on which inputs are given
   - Returns the final metadata object 
2. get_user_input_query_lines
   - Loads input files into a dictionary that AllInOne uses
3. keep_samples
   - Filters out unwanted files befor 
4. determine_cases_and_controls
   - Labels samples case or control in a new catagory added to the metadata file
5. filter_prep_for_matchMD
   - Filters out samples that have null values for any of the metadata categories that are used to match samples
6. matcher
   - Matches samples and then calls the stable marriage class functions
7. orderDict
   - orders the elements for each key in a dictionary based on the frequency the element over the entire dictionary
   - elements with equal frequency are then sorted in alphanumeric ordering  
8. order_keys
   - order the keys in a dictionary based on how many elements are associated with the key in the dictionary
   - keys with equal number of elements are not sorted alphanumericly so the one to one matches can be slightly different for runs with identical inputs
9. stableMarriageRunner
   - Enacts the one to one matches using a stable marriage framework 


