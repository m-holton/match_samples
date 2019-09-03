# match-samples
match-samples allows users to filter down a metadata file, label samples case or control, and match case to control samples. 

## Arguments
Each visualizer in match-samples takes a combination of the 9 arguments below

1. visualization 
   - file location to save augmented metadata to
2. metadata-file 
   - the metadata that contains the samples that will be processed by the program
3. keep 
   - name of file with sqlite lines used to determine what samples to exclude or keep
4. control 
   - name of file with sqlite lines used to determine what samples to label control
   - if given case must also be given
5. case 
   - name of file with sqlite lines used to determine what samples to label case
   - if given control must also be given
6. nullvalues 
   - name of file with strings that represent null values so that samples where one of these null values are in a category that is used to determine matches are filtered out
   - if given then match must also be given
7. match 
   - name of file which contains information on what conditions must be met to constitue a match
   - if given case and control must also be given
8. one 
   - flag that tells program to call stableMarriageRunner and do one to one matches
9. only_matches
   - flag that makes program filter out none matched samples at the end of matching before the metadata is outputted

   
## Input File Format
metadata must be a metadata object (tab separated file such as a .tsv). The top column contains the metadata catagories and the left most row contains the sample ids.

keep, control, and case should all contain sqlite statement that can be used in a WHERE statement.
Statements on different lines are joined by an AND.
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
Output is a visualization of a the metadata. This qzv visualiation reflects the fitering, labeling, and matching done by the program. The recommended way to view visualization is by using qiime2 view at https://view.qiime2.org.

   
## Plugin Visualizers
These functions are the visualizers that can users call using the plugin. They are defined in match_samples.py.

1. subsetting
   - Subsets a metadata object then outputs a visualization of the augmented metadata to a file

2. labeler_no_subset
   - Label samples in a metadata object then outputs a visualization of the augmented metadata to a file

3. complete_labeler
   - Subset and label samples in a metadata object then outputs a visualization of the augmented metadata to a file

4. matching_no_subset_null_filter
   - Label and match samples in a metadata object then outputs a visualization of the augmented metadata to a file

5. matching_no_subset
   - Label, filter, and match samples in a metadata object then outputs a visualization of the augmented metadata to a file

6. matching_no_null_filter
   - Subset, label, and match samples in a metadata object then outputs a visualization of the augmented metadata to a file
7. complete_matcher
   - Subset, label, filter, and match samples in a metadata object then outputs a visualization of the augmented metadata to a file

## Core Functions
These are the funtions that actually do things. They are defined in match_funtions.py. Their unit tests are detailed in test_match_samples.py.

1. get_user_input_query_lines
   - Loads input files into a dictionary that AllInOne uses
2. keep_samples
   - Filters out unwanted files befor 
3. determine_cases_and_controls
   - Labels samples case or control in a new catagory added to the metadata file
4. filter_prep_for_matchMD
   - Filters out samples that have null values for any of the metadata categories that are used to match samples
5. matcher
   - Matches samples and then calls the stable marriage class functions
6. orderDict
   - orders the elements for each key in a dictionary based on the frequency the element over the entire dictionary
   - elements with equal frequency are then sorted in alphanumeric ordering  
7. order_keys
   - order the keys in a dictionary based on how many elements are associated with the key in the dictionary
   - keys with equal number of elements are not sorted alphanumericly so the one to one matches can be slightly different for runs with identical inputs
8. stableMarriageRunner
   - Enacts the one to one matches using a stable marriage framework 


## Examples  
All files used in the examples are in the folder example_files. 

In a directory with the example files running the below commands will run the plugin. 

This command runs complete-matcher. Based on the keep file it first subsets the metadata to only be samples that fit the correct criteria such as being a stool sample. Then it uses the case and control files to label samples. In this example samples of individuals that have ptsd, depression, or bipolar disorder are case samples and those with none of these conditions plus schizophrenia are controls. Then the program check that for every catagory detailed in match that samples' values are one of the null values in the nullvalues file. If a value is a null value then the sample is excluded from the metadata passed on for matching. The match file details how to match the files and by default the paramater only-matches is True so the output visualization only includes samples that were matched to eachother.
  
      qiime match-samples complete-matcher \
          --m-metadata-file truncated_AGP.tsv \
          --p-keep keep.txt \
          --p-control control.txt \
          --p-case case.txt \
          --p-nullvalues null.txt \
          --p-match match.txt \
          --o-visualization code_review_cMatcher.qzv \
          --verbose
    
This command is similar to complete-matcher except that it does not match the samples. As such match and nullvalues are not paramaters. The metadata is ouput after labeling.

      qiime match-samples complete-labeler \
          --m-metadata-file truncated_AGP.tsv \
          --p-keep keep.txt \
          --p-control control.txt \
          --p-case case.txt \
          --o-visualization code_review_cLabeler.qzv \
          --verbose

