# ----------------------------------------------------------------------------
#
# by Mark Holton
#
# ----------------------------------------------------------------------------

import getopt, sys
import pandas as pd
import numpy as np
import qiime2
import time


from qiime2 import Metadata
from collections import defaultdict


import math
import itertools
import time
import operator

from nose.tools import assert_almost_equal, assert_raises, assert_equals
from pandas.util.testing import assert_frame_equal

import match_controls



correctOutFrame = open('./unitTest_files/%s'%('test_case.txt'),'r').readlines()


smallTestFile = pd.DataFrame(index = [1,2,3], data = { 'bmi': ['normal','obese','overweight'], 'age': [23,42,11] } )
largeTestFile = pd.read_csv('./unitTest_files/test_data.csv', sep = '\t' ).set_index('id')
truncatedlargeTestFile = pd.read_csv('./unitTest_files/test_data_2.csv', sep = '\t' ).set_index('id')


csvdata_keep = Metadata.load('./unitTest_files/unit_keep.csv').to_dataframe()
csvdata_case_control = Metadata.load('./unitTest_files/unit_control.csv').to_dataframe()
csvdata_filter = Metadata.load('./unitTest_files/unit_filtered.csv').to_dataframe()
csvdata_match = Metadata.load('./unitTest_files/unit_output.csv').to_dataframe()
#print(csvdata_match)


tstart = time.clock()


# reading in commandline arguments
all_arguments = sys.argv
# selecting all arguments after python file name
argumentList = all_arguments[1:]
unixOptions = "i:k:c:e:n:m:o:"
gnuOptions = ["inputData=", "keep=", "control=", "case=", "nullValues=", "match=", "output="]

try:  
    arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
except getopt.error as err:  
    # output error, and return with an error code
    print (str(err))
    sys.exit(2)
   

#metadata file
file_of_metadata = ''
user_input_file_name_exclude = ''
user_input_file_name_control = ''
user_input_file_name_experiment = ''
user_input_file_null_values = ''
user_input_file_name_match = ''    

# evaluate given options
#print(arguments)

for currentArgument, currentValue in arguments:  
    if currentArgument in ("-v", "--verbose"):
        print ("enabling verbose mode")
    elif currentArgument in ("-h", "--help"):
        print ("displaying help")
    elif currentArgument in ("-i", "--inputData"):
        file_of_metadata = currentValue
    elif currentArgument in ("-k", "--keep"):
        user_input_file_name_exclude = currentValue
    elif currentArgument in ("-c", "--control"):
        user_input_file_name_control = currentValue
    elif currentArgument in ("-e", "--case"):
        user_input_file_name_experiment = currentValue
    elif currentArgument in ("-n", "--nullValues"):
        user_input_file_null_values = currentValue
    elif currentArgument in ("-m", "--match"):
        user_input_file_name_match = currentValue
    elif currentArgument in ("-o", "--output"):
        outputFileName = currentValue

if file_of_metadata == '':
    print('metadata file not found')
    sys.exit(2)
if outputFileName == '':
    print('output put file name not entered')
    sys.exit(2)
#read metadata file into metadata object
originalMD = Metadata.load( file_of_metadata )


        
#each line is a sqlite query to determine what samples to keep
exclude_query_lines_input = match_controls.get_user_input_query_lines(user_input_file_name_exclude)
#each line is a sqlite query to determine what samples to label control
control_query_lines_input = match_controls.get_user_input_query_lines(user_input_file_name_control)
#each line is a sqlite query to determine what samples to label case
case_query_lines_input = match_controls.get_user_input_query_lines(user_input_file_name_experiment)
null_values_lines_input = match_controls.get_user_input_query_lines(user_input_file_null_values)

'''
each line is tab seperated
the first element is the type of match: range or exact
    range matches samples if the numerical values compared are with in some other number of eachother
        this is only to be used with numerical values
    exact matches samples if the values compared are exactly the same
        this can be used for strings and numbers
the second element is the column to compare values of for the case and control samples
the third element is the range number or = (if the match type is exact) 
    this determines how far away a sample can be from another sample for the given column to be matched
'''
match_condition_lines_input = match_controls.get_user_input_query_lines(user_input_file_name_match)

tloadedFiles = time.clock() 
print('time to load input files is %s'%(tloadedFiles - tstart))




def test_get_user_input_query_lines():
    
    if match_controls.get_user_input_query_lines("")!=False:
        print("null input lines does not result in False return value")
    
def test_keep_samples():
    csvdata = afterExclusionMD.to_dataframe()
    try:
        assert_frame_equal(csvdata, csvdata_keep)
        return True
    except:  
        return False
    
    
def test_determine_cases_and_controls():
    csvdata = case_controlMD.to_dataframe()
    '''print(csvdata)
    print(csvdata_case_control)
    print( assert_frame_equal(csvdata, csvdata_case_control) )
    '''
    try:
        assert_frame_equal(csvdata, csvdata_case_control)
    except:  
        return False
    return True

        
def test_filter_prep_for_matchMD():
    
    csvdata = prepped_for_matchMD.to_dataframe()
    
    try:
        assert_frame_equal(csvdata, csvdata_filter)
    except:  
        return False
    return True
    
def test_orderDict():
    test_unorderedDict = {'key_1':['a','b','c','d','e'], 'key_2':['a','b','c','d','e'],  'key_3':['b','e','e','c','a']}
    correct_output = {'key_1':['a','b','c','d','e'], 'key_2':['a','b','c','d','e'], 'key_3':['a','b','c','e','e']}
    
    test_error = {'key_4':['b','f','e','c','a']}
    
    test_equal_freq = {'key_5':['c','b','e','d','a']}
    correct_output_freq = {'key_5':['a','b','c','d','e']}
    
    test_frequencies = {'a':1,'b':2,'c':3,'d':4,'e':5}
    test_frequencies_equal = {'a':1,'b':3,'c':3,'d':3,'e':5}

    if (match_controls.orderDict(test_unorderedDict, test_frequencies) != correct_output):
        print('orderDict is not properly matching the output')
        print(match_controls.orderDict(test_unorderedDict, test_frequencies))
        print('should be')
        print(correct_output)
        return False
    counter = 0
    run_number = 1
    while run_number <=100:
        if (match_controls.orderDict(test_equal_freq, test_frequencies_equal) != correct_output_freq):
            counter = counter + 1
        run_number = run_number + 1
    if counter>=0:
        print('times out of 100 that the order was wrong = %s'%(counter))
    try:
        match_controls.orderDict(test_error, test_frequencies)
        return False
    except:  
        return True
    return True
    
def test_order_keys():
    test_unorderedDict={'2':['a','b'], '1':['a'],  '3':['a','b','c'],  '5':['a','b','c','d','e'], '4':['a','b','c','d']}
    correct_output=['5','4','3','2','1']
    if (match_controls.order_keys(test_unorderedDict) != correct_output):
        print('order_keys is not properly matching the output')
        print(match_controls.order_keys(test_unorderedDict))
        print('should be')
        print(correct_output)
        return False
    
    test_unorderedDict_equ_freq={'2b':['a','b'], '1':['a'], '2a':['a', 'c'],  '3':['a','b','c'],  '5':['a','b','c','d','e'], '4':['a','b','c','d']}
    correct_output_equ_freq=['5','4','3','2a', '2b', '1']  
    if (match_controls.order_keys(test_unorderedDict_equ_freq) != correct_output_equ_freq):
        print('order_keys is not properly matching the output')
        print(match_controls.order_keys(test_unorderedDict_equ_freq))
        print('should be')
        print(correct_output_equ_freq)
        return False
    return True
    
def test_stable_marriage():
    case_dictionary = {'14': ['15', '17'], '25': [], '19': ['20'], '21':[], '6': [], '9': ['10'], '3': [], '7': ['8'], '18': ['17'], '23': [], '16': ['13', '15'], '27': [], '11': ['12']}
    control_match_count_dictionary = {'10': 1, '15': 2, '17': 2, '12': 1, '8': 1, '20': 1, '13': 1}
    case_match_count_dictionary = {'23': 0, '6': 0, '14': 2, '21': 0, '16': 2, '11': 1, '19': 1, '9': 1, '27': 0, '7': 1, '3': 0, '25': 0, '18': 1}

    case_to_control_match = match_controls.stable_marriage(case_dictionary, control_match_count_dictionary, case_match_count_dictionary)
    test_output  = {'15': '16', '12': '11', '8': '7', '10': '9', '17': '18', '20': '19'}
    if case_to_control_match != test_output:
        print("stable marriage fails. \nOutput should be {'15': '16', '12': '11', '8': '7', '10': '9', '17': '18', '20': '19'} \nOutput was")
        print(case_to_control_match)
        
        return False
    return True
    
def test_match_samples():
    csvdata = matchedMD.to_dataframe()
    csvdata_match["matched_to"]= csvdata_match["matched_to"].astype("int64")
    csvdata_match["age_years"]= csvdata_match["age_years"].astype("int64")
    csvdata["matched_to"]= csvdata["matched_to"].astype("int64")
    csvdata["age_years"]= csvdata["age_years"].astype("int64")
   
    
    print('test---------- age_years are the same = %s'%( csvdata_match["age_years"].equals(csvdata["age_years"] )))
    #print( assert_frame_equal(csvdata, csvdata_match) )
    if csvdata_match["age_years"].equals(csvdata["age_years"]) != True:
        print("age_years columns don't match")
        print(csvdata["age_years"])
        print(csvdata_match["age_years"])
    try:
        assert_frame_equal(csvdata, csvdata_match)
        
    except:  
        return False
    return True



if test_orderDict() == False:
    sys.exit(0)
if test_order_keys() == False:
    sys.exit(0)
if test_stable_marriage() == False:
    sys.exit(0)


if exclude_query_lines_input != False:
    afterExclusionMD = match_controls.keep_samples(originalMD, exclude_query_lines_input)
else:
    afterExclusionMD = originalMD

keep = test_keep_samples()
print("keep_samples function works correctly is %s"%(keep))
    
tkeep = time.clock() 
print('time to filter out unwanted samples is %s'%(tkeep - tloadedFiles))
    
if case_query_lines_input != False and control_query_lines_input != False:
    ids = afterExclusionMD.get_ids()
    case_control_Series = pd.Series( ['Unspecified'] * len(ids), ids)
    '''
    ['Unspecified'] * len(ids) creates a list of elements. The list is the 
    same length as ids. All the elements are 'Unspecified'
    '''
    case_control_Series.index.name = afterExclusionMD.id_header
    case_controlDF = case_control_Series.to_frame('case_control') 
    case_control_dict = {'case':case_query_lines_input, 'control':control_query_lines_input }

    case_controlMD = match_controls.determine_cases_and_controls(afterExclusionMD, case_control_dict, case_controlDF)
else:
    afterExclusionMD.to_dataframe().to_csv(outputFileName, sep = '\t')
    print('keep exit')
    sys.exit(0)
        
cas_con = test_determine_cases_and_controls()
print("determine_cases_and_controls function works correctly is %s"%(cas_con))

if null_values_lines_input == False or match_condition_lines_input == False:
    prepped_for_matchMD = case_controlMD
else:    
    prepped_for_matchMD= match_controls.filter_prep_for_matchMD(case_controlMD, match_condition_lines_input, null_values_lines_input)

filtered = test_filter_prep_for_matchMD()
print("filter_prep_for_matchMD function works correctly is %s"%(filtered))
    
tprepped = time.clock() 
print('time to prep Metadata information for match is %s'%(tprepped - tkeep))

if match_condition_lines_input != False:
    matchedMD = match_controls.match_samples( prepped_for_matchMD, match_condition_lines_input )
    matchedMD.to_dataframe().to_csv(outputFileName, sep = '\t')

match = test_match_samples()    
print("match_samples function works correctly is %s"%(match))
   
tmatch = time.clock()  
tend = time.clock()
print('time to match is %s'%(tmatch- tprepped))
print('time to do everything %s'%(tend-tstart))









#start of negative tests ----------------
file_of_metadata = ''
nul_user_input_file_name_exclude = ''
nul_user_input_file_name_control = ''
nul_user_input_file_name_experiment = ''
nul_user_input_file_null_values = ''
nul_user_input_file_name_match = ''    

if match_controls.get_user_input_query_lines("")!=False:
    print("null input lines does not result in False return value")

#each line is a sqlite query to determine what samples to keep
exclude_query_lines_input = match_controls.get_user_input_query_lines(nul_user_input_file_name_exclude)
#each line is a sqlite query to determine what samples to label control
control_query_lines_input = match_controls.get_user_input_query_lines(nul_user_input_file_name_control)
#each line is a sqlite query to determine what samples to label case
case_query_lines_input = match_controls.get_user_input_query_lines(nul_user_input_file_name_experiment)
null_values_lines_input = match_controls.get_user_input_query_lines(nul_user_input_file_null_values)
match_condition_lines_input = match_controls.get_user_input_query_lines(nul_user_input_file_name_match)
  
    
if exclude_query_lines_input != False:
    print("exclude_query_lines_input is not false for the null tests when it should be false")
    
if case_query_lines_input != False and control_query_lines_input != False:
    print("case_query_lines_input or control_query_lines_input are not false for the null tests when they should both be false")
     
if null_values_lines_input != False or match_condition_lines_input != False:
    print("null_values_lines_input or match_condition_lines_input are not false for the null tests when they should both be false")

if match_condition_lines_input != False:
    print("null_values_lines_input or match_condition_lines_input are not false for the null tests when they should both be false")







