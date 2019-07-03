# ----------------------------------------------------------------------------
#
# by Mark Holton
#
# ----------------------------------------------------------------------------

import getopt
import sys
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
    stable = match_controls.Stable_Marriage()

    test_unorderedDict = {'key_1':['a','b','c','d','e'],
        'key_2':['a','c','e','d','b'],  'key_3':['b','e','e','c','a']}
    correct_output = {'key_1':['a','b','c','d','e'],
        'key_2':['a','b','c','d','e'], 'key_3':['a','b','c','e','e']}

    test_error = {'key_4':['b','f','e','c','a']}

    test_equal_freq = {'key_5':['c','b','e','d','a']}
    correct_output_freq = {'key_5':['a','b','c','d','e']}

    test_frequencies = {'a':1,'b':2,'c':3,'d':4,'e':5}
    test_frequencies_equal = {'a':1,'b':3,'c':3,'d':3,'e':5}

    if (stable.orderDict(test_unorderedDict,
        test_frequencies) != correct_output):
        print('orderDict is not properly matching the output')
        print(stable.orderDict(test_unorderedDict, test_frequencies))
        print('should be')
        print(correct_output)
        return False
    counter = 0
    run_number = 1
    while run_number <=100:
        if (stable.orderDict(test_equal_freq, test_frequencies_equal)
            != correct_output_freq):
            counter = counter + 1
        run_number = run_number + 1
    if counter>=0:
        print('times out of 100 that the order was wrong = %s'%(counter))
    try:
        stable.orderDict(test_error, test_frequencies)
        return False
    except:
        return True
    return True


def test_order_keys():
    stable = match_controls.Stable_Marriage()

    test_unorderedDict={'2':['a','b'], '1':['a'],  '3':['a','b','c'],
        '5':['a','b','c','d','e'], '4':['a','b','c','d']}
    correct_output=['5','4','3','2','1']
    if (stable.order_keys(test_unorderedDict) != correct_output):
        print('order_keys is not properly matching the output')
        print(match_controls.order_keys(test_unorderedDict))
        print('should be')
        print(correct_output)
        return False

    test_unorderedDict_equ_freq={'2b':['a','b'], '1':['a'], '2a':['a', 'c'],
        '3':['a','b','c'],  '5':['a','b','c','d','e'], '4':['a','b','c','d']}
    correct_output_equ_freq=['5','4','3','2a', '2b', '1']
    if (stable.order_keys(test_unorderedDict_equ_freq)
        != correct_output_equ_freq):
        print('order_keys is not properly matching the output')
        print(match_controls.order_keys(test_unorderedDict_equ_freq))
        print('should be')
        print(correct_output_equ_freq)
        return False
    return True


def test_stable_marriage():
    stable = match_controls.Stable_Marriage()

    case_dictionary = {'14': ['15', '17'], '25': [], '19': ['20'], '21':[],
        '6': [], '9': ['10'], '3': [], '7': ['8'], '18': ['17'], '23': [],
        '16': ['13', '15'], '27': [], '11': ['12']}
    control_match_count_dictionary = {'10': 1, '15': 2, '17': 2, '12': 1,
        '8': 1, '20': 1, '13': 1}
    case_match_count_dictionary = {'23': 0, '6': 0, '14': 2, '21': 0, '16': 2,
        '11': 1, '19': 1, '9': 1, '27': 0, '7': 1, '3': 0, '25': 0, '18': 1}

    case_to_control_match = stable.stable_marriage(case_dictionary,
        control_match_count_dictionary, case_match_count_dictionary)
    test_output  = {'15': '16', '12': '11', '8': '7', '10': '9', '17': '18',
        '20': '19'}
    if case_to_control_match != test_output:
        print("stable marriage fails. \nOutput should be {'15': '16', '12': '11', '8': '7', '10': '9', '17': '18', '20': '19'} \nOutput was")
        print(case_to_control_match)

        return False
    return True










def test_get_user_input_query_lines(unit, input_metadata, match_query):

    input_dict = {"inputdata":input_metadata}
    input_dict = {"match":match_query}
    input_dict = {"keep":None, "case":None, "nullvalues":None, "match":None,
        "inputdata":input_metadata}
    assertRaises(ValueError, match_controls.get_user_input_query_lines(),
        verbose, input_dict)
    assertRaises(ValueError, match_controls.get_user_input_query_lines(),
        verbose, input_dict)


def test_keep_samples(unit, normal_input, normal_output, normal_keep,
    noentries_keep, empty_file):
    '''

    Parameters
    ----------
    each parameter is a string that is the file location

    '''
    verbose = False

    norm_in = Metadata.load("./%s/%s"%(unit, normal_input))
    norm_out = Metadata.load("./%s/%s"%(unit, normal_output))

    norm_keep = open("./%s/%s"%(unit, normal_keep), "r").readlines()
    noentry_keep = open("./%s/%s"%(unit, noentries_keep), "r").readlines()
    emp_file = open("./%s/%s"%(unit, empty_file), "r").readlines()

    unit_norm_out = match_controls.keep_samples(verbose, norm_in, norm_keep)
    unit_empty_out = match_controls.keep_samples(verbose, norm_in, emp_file)

    assertRaises(ValueError, match_controls.keep_samples(), verbose, norm_in,
        noentry_keep)

    unit_norm_out = unit_norm_out.to_dataframe()
    unit_empty_out = unit_empty_out.to_dataframe()
    norm_in = norm_in.to_dataframe()
    norm_out = norm_out.to_dataframe()
    assert_frame_equal(norm_out, unit_norm_out)
    assert_frame_equal(norm_in, unit_empty_out)


def test_determine_cases_and_controls(unit, normal_input, normal_output,
    empty_output, normal_control, normal_case, noentries_case, empty_file):
    verbose = False

    norm_in = Metadata.load("./%s/%s"%(unit, normal_input))
    norm_out = Metadata.load("./%s/%s"%(unit, normal_output))
    empty_out = Metadata.load("./%s/%s"%(unit, empty_output))

    norm_case = open("./%s/%s"%(unit, normal_case), "r").readlines()
    norm_control = open("./%s/%s"%(unit, normal_control), "r").readlines()
    noentry_case = open("./%s/%s"%(unit, noentries_case), "r").readlines()
    emp_file = open("./%s/%s"%(unit, empty_file), "r").readlines()

    case_control_dict = {"case":norm_case, "control":norm_control}
    unit_norm_out = match_controls.determine_cases_and_controls(verbose,
        norm_in, case_control_dict)

    case_control_dict = {"case":emp_file, "control":emp_file}
    unit_empty_out = match_controls.determine_cases_and_controls(verbose,
        norm_in, case_control_dict)

    case_control_dict = {"case":noentry_case, "control":norm_control}
    assertRaises(ValueError, match_controls.determine_cases_and_controls(),
        verbose, norm_in, case_control_dict)

    norm_out = norm_out.to_dataframe()
    unit_norm_out = unit_norm_out.to_dataframe()
    assert_frame_equal(norm_out, unit_norm_out)
    empty_out = empty_out.to_dataframe()
    unit_empty_out = unit_empty_out.to_dataframe()
    assert_frame_equal(empty_out, unit_empty_out)


def test_filter_prep_for_matchMD(unit, normal_input, normal_output,
    no_null_input, normal_null, normal_match, wrong_column_match,
    noentries_null, empty_file):
    verbose = False

    norm_in = Metadata.load("./%s/%s"%(unit, normal_input))
    norm_out = Metadata.load("./%s/%s"%(unit, normal_output))
    no_in = Metadata.load("./%s/%s"%(unit, no_null_input))

    norm_null = open("./%s/%s"%(unit, normal_null), "r").readlines()
    noentry_null = open("./%s/%s"%(unit, noentries_null), "r").readlines()
    emp_file = open("./%s/%s"%(unit, empty_file), "r").readlines()
    norm_match = open("./%s/%s"%(unit, normal_match), "r").readlines()
    wcolumn_match = open("./%s/%s"%(unit, wrong_column_match), "r").readlines()

    unit_norm_out = match_controls.filter_prep_for_matchMD(verbose,
        norm_in, norm_match, norm_null)
    unit_no_out = match_controls.filter_prep_for_matchMD(verbose,
        no_in, norm_match, norm_null)
    unit_empty_null_out = match_controls.filter_prep_for_matchMD(verbose,
        norm_in, norm_match, emp_file)
    unit_empty_match_out = match_controls.filter_prep_for_matchMD(verbose,
        norm_in, emp_file, norm_null)

    assertRaises(ValueError, match_controls.filter_prep_for_matchMD(), verbose,
        norm_in, norm_match, noentry_null)
    assertRaises(KeyError, match_controls.filter_prep_for_matchMD(), verbose,
        norm_in, wcolumn_match, norm_null)

    norm_out = norm_out.to_dataframe()
    unit_norm_out = unit_norm_out.to_dataframe()
    assert_frame_equal(norm_out, unit_norm_out)
    no_in = no_in.to_dataframe()
    unit_no_out = unit_no_out.to_dataframe()
    assert_frame_equal(no_in, unit_no_out)
    norm_in = norm_in.to_dataframe()
    unit_empty_null_out = unit_empty_null_out.to_dataframe()
    assert_frame_equal(norm_in, unit_empty_null_out)
    empty_out = empty_out.to_dataframe()
    unit_empty_match_out = unit_empty_match_out.to_dataframe()
    assert_frame_equal(norm_in, unit_empty_match_out)


def test_match_samples(unit, normal_input, normal_output, normal_match,
    string_control_input, string_case_input, wrong_column_match,
    string_int_match, no_match_input, no_match_output, empty_file,
    no_case_input, no_case_output, no_control_input, no_control_output):
    verbose = False

    norm_in = Metadata.load("./%s/%s"%(unit, normal_input))
    norm_out = Metadata.load("./%s/%s"%(unit, normal_output))
    no_case_in = Metadata.load("./%s/%s"%(unit, no_case_input))
    no_case_out = Metadata.load("./%s/%s"%(unit, no_case_output))
    no_control_in = Metadata.load("./%s/%s"%(unit, no_control_input))
    no_control_out = Metadata.load("./%s/%s"%(unit, no_control_output))
    no_in = Metadata.load("./%s/%s"%(unit, no_match_input))
    no_out = Metadata.load("./%s/%s"%(unit, no_match_output))
    str_cont_in = Metadata.load("./%s/%s"%(unit, string_control_input))
    str_case_in = Metadata.load("./%s/%s"%(unit, string_case_input))

    str_match = open("./%s/%s"%(unit, string_int_match), "r").readlines()
    emp_file = open("./%s/%s"%(unit, empty_file), "r").readlines()
    norm_match = open("./%s/%s"%(unit, wrong_column_match), "r").readlines()
    wcolumn_match = open("./%s/%s"%(unit, wrong_column_match), "r").readlines()

    unit_norm_out = match_controls.match_samples(verbose,
        norm_in, norm_match)
    unit_case_out = match_controls.match_samples(verbose,
        no_case_in, norm_match)
    unit_control_out = match_controls.match_samples(verbose,
        no_control_in, norm_match)
    unit_no_out = match_controls.match_samples(verbose,
        no_in, norm_match)

    assertRaises(ValueError, match_controls.match_samples(), verbose,
        str_cont_in, norm_match)
    assertRaises(ValueError, match_controls.match_samples(), verbose,
        str_case_in, norm_match)
    assertRaises(ValueError, match_controls.match_samples(), verbose,
        norm_in, str_match)
    assertRaises(KeyError, match_controls.match_samples(), verbose,
        norm_in, wcolumn_match)

    norm_out = norm_out.to_dataframe()
    unit_norm_out = unit_norm_out.to_dataframe()
    assert_frame_equal(norm_out, unit_norm_out)
    no_case_out = no_case_out.to_dataframe()
    unit_case_out = unit_case_out.to_dataframe()
    assert_frame_equal(no_case_out, unit_case_out)
    no_control_out = no_control_out.to_dataframe()
    unit_control_out = unit_control_out.to_dataframe()
    assert_frame_equal(no_control_out, unit_control_out)
    no_out = no_out.to_dataframe()
    unit_no_out = unit_no_out.to_dataframe()
    assert_frame_equal(no_out, unit_no_out)


@click.command()
@click.option("--verbose", is_flag=True,
    help="Make print statements appear")
@click.option("--unit", is_flag=True,
    help="Location of the folder that holds the unit test files")
@click.option("--emtpy_file",
    default="emtpy_file.txt",
    help="Make print statements appear")
@click.option("--test_case",
    default="test_case.txt",
    help="Make print statements appear")
@click.option("--test_case_noentries",
    default="test_case_noentries.txt",
    help="Make print statements appear")
@click.option("--test_control_in",
    default="test_control_in.txt",
    help="Make print statements appear")
@click.option("--test_control_NotIn",
    default="test_control_NotIn.txt",
    help="Make print statements appear")
@click.option("--test_keep",
    default="test_keep.txt",
    help="Make print statements appear")
@click.option("--test_keep_noentries",
    default="test_keep_noentries.txt",
    help="Make print statements appear")
@click.option("--test_match",
    default="test_match.txt",
    help="Make print statements appear")
@click.option("--test_match_error_column",
    default="test_match_error_column.txt",
    help="Make print statements appear")
@click.option("--test_match_error_int_str",
    default="test_match_error_int_str.txt",
    help="Make print statements appear")
@click.option("--test_nulls",
    default="test_nulls.txt",
    help="Make print statements appear")
@click.option("--test_nulls_noentries",
    default="test_nulls_noentries.txt",
    help="Make print statements appear")
@click.option("--unit_case_empty_output",
    default="unit_case_empty_output.tsv",
    help="Make print statements appear")
@click.option("--unit_case_input",
    default="unit_case_input.tsv",
    help="Make print statements appear")
@click.option("--unit_case_output",
    default="unit_case_output.tsv",
    help="Make print statements appear")
@click.option("--unit_keep_input",
    default="unit_keep_input.tsv",
    help="Make print statements appear")
@click.option("--unit_keep_output",
    default="unit_keep_output.tsv",
    help="Make print statements appear")
@click.option("--unit_match_input",
    default="unit_match_input.tsv",
    help="Make print statements appear")
@click.option("--unit_match_int_str_case",
    default="unit_match_int_str_case.tsv",
    help="Make print statements appear")
@click.option("--unit_match_int_str_control",
    default="unit_match_int_str_control.tsv",
    help="Make print statements appear")
@click.option("--unit_match_output",
    default="unit_match_output.tsv",
    help="Make print statements appear")
@click.option("--unit_no_match_input",
    default="unit_no_match_input.tsv",
    help="Make print statements appear")
@click.option("--unit_no_match_output",
    default="unit_no_match_output.tsv",
    help="Make print statements appear")
@click.option("--unit_no_null_input",
    default="unit_no_null_input.tsv",
    help="Make print statements appear")
@click.option("--unit_null_input",
    default="unit_null_input.tsv",
    help="Make print statements appear")
@click.option("--unit_null_output",
    default="unit_null_output.tsv",
    help="Make print statements appear")

@click.option("--unit_no_case_match_input",
    default="unit_no_case_match_input.tsv",
    help="Make print statements appear")
@click.option("--unit_no_case_match_output",
    default="unit_no_case_match_output.tsv",
    help="Make print statements appear")
@click.option("--unit_no_control_match_input",
    default="unit_no_control_match_input.tsv",
    help="Make print statements appear")
@click.option("--unit_no_control_match_output",
    default="unit_no_control_match_output.tsv",
    help="Make print statements appear")
def main(verbose, unit):

    test_orderDict()
    test_order_keys()
    test_stable_marriage()

    test_get_user_input_query_lines()



    test_keep_samples(unit, unit_keep_input, unit_keep_output, test_keep,
        test_keep_noentries, empty_file)
    test_determine_cases_and_controls(unit, unit_case_input, unit_case_output,
        unit_case_empty_output, test_control_in, test_case,
        test_case_noentries, empty_file)
    test_filter_prep_for_matchMD(unit, unit_null_input, unit_null_output,
        unit_no_null_input, test_nulls, test_match, test_match_error_column,
        test_nulls_noentries, empty_file)
    test_match_samples(unit, unit_match_input, unit_match_output, test_match,
        unit_match_int_str_control, unit_match_int_str_case,
        test_match_error_column, test_match_error_int_str,
        unit_no_match_input, unit_no_match_output, empty_file,
        unit_no_case_match_input, unit_no_case_match_output,
        unit_no_control_match_input, unit_no_control_match_output)




if __name__ == '__main__':
    main()
