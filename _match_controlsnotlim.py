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
import unittest
import click

from qiime2 import Metadata
from collections import defaultdict


import math
import itertools
import time
import operator

from nose.tools import assert_almost_equal, assert_raises, assert_equals
from pandas.util.testing import assert_frame_equal

import match_controls



def test_orderDict():
    test_unorderedDict = {'key_1':['a','b','c','d','e'], 'key_2':['a','c','e','d','b'],  'key_3':['b','e','e','c','a']}
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







def test_get_user_input_query_lines():
    if not assertRaises(SomeException):
        print("null input lines does not result in Exception")
    if match_controls.get_user_input_query_lines("")!=False:
        print("null input lines does not result in False return value")








def test_keep_samples(afterExclusionMD, csvdata_keep):
    csvdata = afterExclusionMD.to_dataframe()

    assert_frame_equal(csvdata, csvdata_keep)



def test_determine_cases_and_controls(case_controlMD, csvdata_case_control):
    csvdata = case_controlMD.to_dataframe()
    '''print(csvdata)
    print(csvdata_case_control)
    print( assert_frame_equal(csvdata, csvdata_case_control) )
    '''

    assert_frame_equal(csvdata, csvdata_case_control)



def test_filter_prep_for_matchMD(prepped_for_matchMD, csvdata_filter):

    csvdata = prepped_for_matchMD.to_dataframe()


    assert_frame_equal(csvdata, csvdata_filter)



def test_match_samples(matchedMD, csvdata_match):
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
    assert_frame_equal(csvdata, csvdata_match)








def test_Everything(verbose, inputdata, keep, control, case, nullvalues, match, output, csvdata_keep, csvdata_case_control, csvdata_filter, csvdata_match):

    csvdata_keep = Metadata.load(csvdata_keep).to_dataframe()
    csvdata_case_control = Metadata.load(csvdata_case_control).to_dataframe()
    csvdata_filter = Metadata.load(csvdata_filter).to_dataframe()
    csvdata_match = Metadata.load(csvdata_match).to_dataframe()

    tstart = time.clock()
    inputDict = {"inputdata":inputdata, "keep":keep, "control":control, "case":case, "nullvalues":nullvalues, "match":match}
    #loads and opens input files
    inputDict = match_controls.get_user_input_query_lines(verbose,inputDict)

    tloadedFiles = time.clock()
    if verbose:
        print('Time to load input files is %s'%(tloadedFiles - tstart))
    afterExclusionMD = match_controls.keep_samples(verbose, inputDict["inputdata"], inputDict["keep"])


    tkeep = time.clock()
    keep = test_keep_samples(afterExclusionMD, csvdata_keep)
    if verbose:
        print("keep_samples function works correctly is %s"%(keep))
        print('Time to filter out unwanted samples is %s'%(tkeep - tloadedFiles))
    ids = afterExclusionMD.get_ids()
    case_control_Series = pd.Series( ['Unspecified'] * len(ids), ids)
    '''
    ['Unspecified'] * len(ids) creates a list of elements. The list is the
    same length as ids. All the elements are 'Unspecified'
    '''
    case_control_Series.index.name = afterExclusionMD.id_header
    case_controlDF = case_control_Series.to_frame('case_control')
    case_control_dict = {'case':inputDict["case"], 'control':inputDict["control"] }

    case_controlMD = match_controls.determine_cases_and_controls(verbose, afterExclusionMD, case_control_dict, case_controlDF)

    tcase_control = time.clock()
    case_control = test_determine_cases_and_controls(case_controlMD, csvdata_case_control)
    if verbose:
        print("determine_cases_and_controls function works correctly is %s"%(case_control))
        print('Time to label case and control samples is %s'%(tcase_control - tkeep))

    prepped_for_matchMD= match_controls.filter_prep_for_matchMD(verbose, case_controlMD, inputDict["match"], inputDict["nullvalues"])

    tprepped = time.clock()
    prepped = test_filter_prep_for_matchMD(prepped_for_matchMD, csvdata_filter)
    if verbose:
        print("filter_prep_for_matchMD function works correctly is %s"%(prepped))
        print('Time to filter Metadata information for samples with null values is %s'%(tprepped - tcase_control))

    if inputDict["match"] != False:
        matchedMD = match_controls.match_samples(verbose, prepped_for_matchMD, inputDict["match"] )
        matchedMD.to_dataframe().to_csv(output, sep = '\t')
    tmatch = time.clock()
    tend = time.clock()
    match = test_match_samples(matchedMD, csvdata_match)
    if verbose:
        print("match_samples function works correctly is %s"%(match))
        print('Time to match is %s'%(tmatch- tprepped))
        print('Time to do everything %s'%(tend-tstart))



@click.command()
@click.option('--verbose', is_flag=True, help='Make print statements appear')
@click.option('--keep', default=1, type = str, help='name of file with sqlite lines used to determine what samples to exclude or keep')
@click.option('--control', default=1, type = str, help='name of file with sqlite lines used to determine what samples to label control')
@click.option('--case', default=1, type = str, help='name of file with sqlite lines used to determine what samples to label case')
@click.option('--nullvalues', default=1, type = str, help='name of file with sqlite lines used to determine what samples to exclude or keep')
@click.option('--match', default=1, type = str, help='name of file with sqlite lines used to determine what samples to exclude or keep')
@click.option('--inputdata', required = True, type = str, help='Name of file with sample metadata to analyze.')
@click.option('--output', required = True, type = str, help='Name of file to export data to.')
@click.option('--csvdata_keep', default=1, type = str, help='Name of file that include the proper output of keep_samples to the corresponding test file.')
@click.option('--csvdata_case_control', default=1, type = str, help='Name of file that include the proper output of determine_cases_and_controls to the corresponding test file.')
@click.option('--csvdata_filter', default=1, type = str, help='Name of file that include the proper output of filter_prep_for_matchMD to the corresponding test file.')
@click.option('--csvdata_match', default=1, type = str, help='Name of file that include the proper output of match_samples to the corresponding test file.')
def mainControler(verbose, inputdata, keep, control, case, nullvalues, match, output, csvdata_keep, csvdata_case_control, csvdata_filter, csvdata_match):

    '''
    #test_get_user_input_query_lines()
    test_keep_samples()
    test_determine_cases_and_controls()
    test_filter_prep_for_matchMD()
    test_orderDict()
    test_order_keys()
    test_stable_marriage()
    test_match_samples()




    csvdata_keep = Metadata.load('./unitTest_files/unit_keep.csv').to_dataframe()
    csvdata_case_control = Metadata.load('./unitTest_files/unit_control.csv').to_dataframe()
    csvdata_filter = Metadata.load('./unitTest_files/unit_filtered.csv').to_dataframe()
    csvdata_match = Metadata.load('./unitTest_files/unit_output.csv').to_dataframe()
    '''
    test_get_user_input_query_lines()
    test_orderDict()
    test_order_keys()
    test_stable_marriage()

    #correctOutFrame = open('./unitTest_files/%s'%('test_case.txt'),'r').readlines()


    #smallTestFile = pd.DataFrame(index = [1,2,3], data = { 'bmi': ['normal','obese','overweight'], 'age': [23,42,11] } )
    #largeTestFile = pd.read_csv('./unitTest_files/test_data.csv', sep = '\t' ).set_index('id')
    #truncatedlargeTestFile = pd.read_csv('./unitTest_files/test_data_2.csv', sep = '\t' ).set_index('id')





    if isinstance(keep, str) and isinstance(case, str):
        if isinstance(control, str) and isinstance(case, str) and isinstance(case, str):
                if isinstance(match, str) and isinstance(case, str):
                    if isinstance(nullvalues, str) and isinstance(case, str):
                        if verbose:
                            print("Testing Everything")
                            test_Everything(verbose, inputdata, keep, control, case, nullvalues, match, output, csvdata_keep, csvdata_case_control, csvdata_filter, csvdata_match)
                    else:
                        if verbose:
                            print("Testing ExcludeControlCaseAndMatch")
                        test_ExcludeControlCaseAndMatch(verbose,inputdata,keep,control,case, match, output, csvdata_keep, csvdata_case_control, csvdata_match)
                else:
                    if verbose:
                            print("Testing KeepAndControlCase")
                    test_KeepAndControlCase(verbose,inputdata,keep,control,case,output, csvdata_keep, csvdata_case_control)
        else:
            if verbose:
                print("Testing KeepOnly")
            test_KeepOnly(verbose, inputdata, keep, output, csvdata_keep)
    elif isinstance(control, str) and isinstance(case, str) and isinstance(case, str):
        if isinstance(match, str) and isinstance(case, str):
            if isinstance(nullvalues, str) and isinstance(case, str):
                if verbose:
                    print("Testing ControlCaseNullAndMatch")
                test_ControlCaseNullAndMatch(verbose,inputdata,control,case, nullvalues, match, output, csvdata_case_control, csvdata_filter, csvdata_match)
            else:
                if verbose:
                    print("Testing ControlCaseAndMatch")
                test_ControlCaseAndMatch(verbose,inputdata,control,case,match,output, csvdata_case_control, csvdata_match)
        else:
            if verbose:
                print("Testing ControlAndCaseOnly")
            test_ControlAndCaseOnly(verbose,inputdata,control, case, output, csvdata_case_control)



if __name__ == '__main__':
    mainControler()





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
