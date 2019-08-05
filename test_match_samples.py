# ----------------------------------------------------------------------------
#
# by Mark Holton
#
# ----------------------------------------------------------------------------

import time
import click

import pandas as pd
import numpy as np

from nose.tools import assert_raises, assert_equals
from pandas.util.testing import assert_frame_equal
from click.testing import CliRunner

import match_samples
from qiime2 import Metadata

def test_orderDict(verbose):
    '''
    Tests the function that orders the lists associated with each key
        in a dictionary based of the frequency through out the entire
        dictionary of each entry in the lists

    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not.
            True outputs print statements.

    '''
    stable = match_samples.Stable_Marriage()

    test_unorderedDict = {'key_1':['a','b','c','d','e'],
        'key_2':['a','c','e','d','b'],  'key_3':['b','e','e','c','a']}
    test_frequencies = {'a':1,'b':2,'c':3,'d':4,'e':5}
    correct_output = {'key_1':['a','b','c','d','e'],
        'key_2':['a','b','c','d','e'], 'key_3':['a','b','c','e','e']}

    assert_equals(stable.orderDict(verbose, test_unorderedDict,
        test_frequencies), correct_output)

    test_equal_freq = {'key_5':['c','b','e','d','a']}
    test_frequencies_equal = {'a':1,'b':3,'c':3,'d':3,'e':5}
    correct_output_freq = {'key_5':['a','b','c','d','e']}

    assert_equals(stable.orderDict(verbose, test_equal_freq,
        test_frequencies_equal), correct_output_freq)

    counter = 0
    run_number = 1
    print("Running orderDict 100 times to test order when frequencies "
          "are equal.")
    while run_number <=100:
        if (stable.orderDict(verbose, test_equal_freq, test_frequencies_equal)
            != correct_output_freq):
            counter = counter + 1
        run_number = run_number + 1
    print('times out of 100 that the order was wrong = %s'%(counter))

def test_order_keys(verbose):
    '''
    Tests the function that orders keys based one their number of
        entries

    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not.
            True outputs print statements.

    '''
    stable = match_samples.Stable_Marriage()

    test_unorderedDict=  {'2':['a','b'], '1':['a'],  '3':['a','b','c'],
        '5':['a','b','c','d','e'], '4':['a','b','c','d']}
    correct_output = ['5','4','3','2','1']
    assert_equals(stable.order_keys(verbose, test_unorderedDict),
        correct_output)


    test_unorderedDict_equ_freq = {'2b':['a','b'], '1':['a'], '2a':['a', 'c'],
        '3':['a','b','c'],  '5':['a','b','c','d','e'], '4':['a','b','c','d']}

    correct_output_equ_freq_one = ['5','4','3','2b', '2a', '1']
    correct_output_equ_freq_two = ['5','4','3','2a', '2b', '1']

    counter_one = 0
    counter_two = 0
    print("Running order_keys 100 times to test order when frequencies are "
          "equal.")
    num_runs = 1000
    for i in range(0,num_runs):
        ans = stable.order_keys(verbose, test_unorderedDict_equ_freq)
        if (ans == correct_output_equ_freq_one):
            counter_one = counter_one + 1
        if (ans == correct_output_equ_freq_two):
            counter_two = counter_two + 1

    print('Times out of 100 that the order was wrong = %s'
        %(num_runs-counter_two-counter_one))
    print("The ratio of solution one to solution two was %s/%s"
        %(counter_one, counter_two))



def test_stable_marriage(verbose):
    '''
    Tests the stable marriage function

    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not.
            True outputs print statements.

    '''
    stable = match_samples.Stable_Marriage()

    case_dictionary = {'14': ['15', '17'], '25': [], '19': ['20'], '21':[],
        '6': [], '9': ['10'], '3': [], '7': ['8'], '18': ['17'], '23': [],
        '16': ['13', '15'], '27': [], '11': ['12']}
    control_match_count_dictionary = {'10': 1, '15': 2, '17': 2, '12': 1,
        '8': 1, '20': 1, '13': 1}
    case_match_count_dictionary = {'23': 0, '6': 0, '14': 2, '21': 0, '16': 2,
        '11': 1, '19': 1, '9': 1, '27': 0, '7': 1, '3': 0, '25': 0, '18': 1}
    case_to_control_match = stable.stableMarriageRunner(verbose,
        case_dictionary, control_match_count_dictionary,
        case_match_count_dictionary)
    test_output = {'20':'19', '10':'9', '12':'11', '8':'7', '15':'14',
        '17':'18', '13':'16'}
    assert_equals(case_to_control_match, test_output)

    case_dictionary = {'2': ['10', '1'], '4': ['3'], '6': [], '9':[]}
    control_match_count_dictionary = {'10': 1, '1': 1, '3': 1}
    case_match_count_dictionary = {'9': 0, '4': 1, '6': 0, '2': 2}
    case_to_control_match = stable.stableMarriageRunner(verbose,
        case_dictionary, control_match_count_dictionary,
        case_match_count_dictionary)
    test_output = {'10':'2', '3':'4'}
    assert_equals(case_to_control_match, test_output)


def test_get_user_input_query_lines(verbose, unit, input_metadata,
    match_query):
    '''
    Tests the fuction that reads in the sql query files

    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not.
            True outputs print statements.
    unit: string
        Location of the folder that holds the unit test files
    input_metadata: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used to test the keeping of samples functionality
            of the match_samples.py
    match_query: string
    '''
    input_dict = {"inputdata":input_metadata}
    input_dict = {"match":match_query}

    input_dict = {"keep":None, "case":None, "nullvalues":None, "match":None,
        "inputdata":"input_metadata"}
    assert_raises(ValueError, match_samples.get_user_input_query_lines,
        verbose, input_dict)
    input_dict = {"keep":"None", "case":None, "nullvalues":None, "match":None,
        "inputdata":input_metadata}
    assert_raises(ValueError, match_samples.get_user_input_query_lines,
        verbose, input_dict)


def test_keep_samples(verbose, unit, normal_input, normal_output, normal_keep,
    noentries_keep, empty_file):
    '''
    Test the programs filtering out of unwanted samples based on sql queries

    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not.
            True outputs print statements.
    unit: string
        Location of the folder that holds the unit test files
    normal_input: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used to test the keeping of samples functionality
            of the match_samples.py
    normal_output: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used to test that valid inputs for keeping samples
            gets the correct output
    normal_keep: string
        Name of the query file that contains the sql queries to do a normal
            keep
    noentries_keep: string
        Name of the query file that contains the sql queries that keeps not
            samples
    empty_file: string
        Name of the empty file used in various tests
    '''
    norm_in = Metadata.load("./%s/%s"%(unit, normal_input))
    norm_out = Metadata.load("./%s/%s"%(unit, normal_output))

    norm_keep = open("./%s/%s"%(unit, normal_keep), "r").read().splitlines()
    noentry_keep = open("./%s/%s"%(unit, noentries_keep),
        "r").read().splitlines()
    emp_file = open("./%s/%s"%(unit, empty_file), "r").read().splitlines()

    unit_norm_out = match_samples.keep_samples(verbose, norm_in, norm_keep)

    assert_raises(ValueError, match_samples.keep_samples, verbose, norm_in,
        emp_file)
    assert_raises(ValueError, match_samples.keep_samples, verbose, norm_in,
        noentry_keep)

    unit_norm_out = unit_norm_out.to_dataframe()
    norm_out = norm_out.to_dataframe()
    assert_frame_equal(norm_out, unit_norm_out)


def test_determine_cases_and_controls(verbose, unit, normal_input,
    normal_output, normal_control, normal_case, noentries_case, empty_file):
    '''
    Tests the programs labeling of case and control samples

    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not.
            True outputs print statements.
    unit: string
        Location of the folder that holds the unit test files
    normal_input: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used to test the case and control labeling
            functionality of the match_samples.py
    normal_output: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used to test that valid case and control inputs get
            the correct output
    normal_control: string
        Name of the query file that contains the normal control query using IN
    normal_case: string
        Name of the query file that contains the normal case query
    noentries_case: string
        Name of the query file that results in no cases being found. This tests
            the that filtering everything out gives an error.
    empty_file: string
        Name of the empty file used in various tests
    '''
    norm_in = Metadata.load("./%s/%s"%(unit, normal_input))
    norm_out = Metadata.load("./%s/%s"%(unit, normal_output))

    norm_case = open("./%s/%s"%(unit, normal_case), "r").read().splitlines()
    norm_control = open("./%s/%s"%(unit, normal_control),
        "r").read().splitlines()
    noentry_case = open("./%s/%s"%(unit, noentries_case),
        "r").read().splitlines()
    emp_file = open("./%s/%s"%(unit, empty_file), "r").read().splitlines()

    case_control_dict = {"case":norm_case, "control":norm_control}
    unit_norm_out = match_samples.determine_cases_and_controls(verbose,
        norm_in, case_control_dict)

    case_control_dict = {"case":emp_file, "control":emp_file}
    assert_raises(ValueError, match_samples.determine_cases_and_controls,
        verbose, norm_in, case_control_dict)

    case_control_dict = {"case":noentry_case, "control":norm_control}
    assert_raises(ValueError, match_samples.determine_cases_and_controls,
        verbose, norm_in, case_control_dict)

    norm_out = norm_out.to_dataframe()
    unit_norm_out = unit_norm_out.to_dataframe()
    assert_frame_equal(norm_out, unit_norm_out)

def test_filter_prep_for_matchMD(verbose, unit, normal_input, normal_output,
    no_null_input, normal_null, normal_match, wrong_column_match,
    noentries_null, empty_file):
    '''
    Tests the null filtering functionality

    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not.
            True outputs print statements.
    unit: string
        Location of the folder that holds the unit test files
    normal_input: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be as input to test that valid inputs for filtering
            out samples with null values in the columns used for matching gets
            the correct output.
    normal_output: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be compared to output of the funtion that preps the
            metadata object for matching. It test that valid inputs for
            filtering out samples with null values in the columns used for
            matching gets the correct output.
    no_null_input: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used to test if giving a file with no null entries
            as input for null filtering returns an output equal to the input.
    normal_null: string
        Name of the file that contains the null values used to prepare
            metadata objects for match in filter_prep_for_matchMD
    normal_match: string
        Name of the file that contains the lines to match the samples normally
    wrong_column_match: string
        Name of the file that contains the lines to match samples but one of
            the columns in the file is not in the metadata input
    noentries_null: string
        Name of the file that contains the null values used to prepare metadata
            objects for match in filter_prep_for_matchMD. The null values will
            filter every sample out which should result in an error.
    empty_file: string
        Name of the empty file used in various tests
    '''
    norm_in = Metadata.load("./%s/%s"%(unit, normal_input))
    norm_out = Metadata.load("./%s/%s"%(unit, normal_output))
    no_in = Metadata.load("./%s/%s"%(unit, no_null_input))

    norm_null = open("./%s/%s"%(unit, normal_null), "r").read().splitlines()
    noentry_null = open("./%s/%s"%(unit, noentries_null),
        "r").read().splitlines()
    emp_file = open("./%s/%s"%(unit, empty_file), "r").read().splitlines()
    norm_match = open("./%s/%s"%(unit, normal_match), "r").read().splitlines()
    wcolumn_match = open("./%s/%s"%(unit, wrong_column_match),
        "r").read().splitlines()

    unit_norm_out = match_samples.filter_prep_for_matchMD(verbose,
        norm_in, norm_match, norm_null)
    unit_no_out = match_samples.filter_prep_for_matchMD(verbose,
        no_in, norm_match, norm_null)
    unit_empty_null_out = match_samples.filter_prep_for_matchMD(verbose,
        norm_in, norm_match, emp_file)
    unit_empty_match_out = match_samples.filter_prep_for_matchMD(verbose,
        norm_in, emp_file, norm_null)

    assert_raises(ValueError, match_samples.filter_prep_for_matchMD, verbose,
        norm_in, norm_match, noentry_null)
    assert_raises(KeyError, match_samples.filter_prep_for_matchMD, verbose,
        norm_in, wcolumn_match, norm_null)

    norm_out = norm_out.to_dataframe()
    unit_norm_out = unit_norm_out.to_dataframe()
    norm_out["age_years"] = norm_out["age_years"].astype(int)
    norm_out["age_years"] = norm_out["age_years"].astype(str)
    assert_frame_equal(norm_out, unit_norm_out)

    no_in = no_in.to_dataframe()
    unit_no_out = unit_no_out.to_dataframe()
    assert_frame_equal(no_in, unit_no_out)

    norm_in = norm_in.to_dataframe()
    unit_empty_null_out = unit_empty_null_out.to_dataframe()
    assert_frame_equal(norm_in, unit_empty_null_out)

    unit_empty_match_out = unit_empty_match_out.to_dataframe()
    assert_frame_equal(norm_in, unit_empty_match_out)

def test_match_samples(verbose, unit, normal_input, normal_output, normal_match,
    string_control_input, string_case_input, wrong_column_match,
    string_int_match, no_match_input, no_match_output, empty_file,
    no_case_input, no_case_output, no_control_input, no_control_output,
    all_matches_input, all_matches_output,
    only_all_matches_output, only_one_match_output, all_matches):
    '''
    Tests the match functionality

    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not.
            True outputs print statements.
    unit: string
        Location of the folder that holds the unit test files
    normal_input: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used to test the matching of case and control
            labeled samples functionality of the match_samples.py
    normal_output: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used to test that valid inputs for matching case
            and control samples yields the correct output
    normal_match: string
        Name of the file that contains the lines to match the samples normally
    string_control_input: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used to test
    string_case_input: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used to test
    wrong_column_match: string
        Name of the file that contains the lines to match samples but one of
            the columns in the file is not in the metadata input
    string_int_match: string
        Name of the file that contains the lines to match samples but the
            number for the age_years range is a string that can not be type
            cased to a float
    no_match_input: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used to test the match function when there are no
            possible matches. It is the input metadata for the funtion.
    no_match_output: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used to test if the match funtion gives the correct
            output when there are no possible matches. The file stores the
            correct output.
    empty_file: string
        Name of the empty file used in various tests
    no_case_input: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used to test the match function when there are no
            case samples. It is the input metadata for the funtion.
    no_case_output: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used to test if the match funtion gives the correct
            output when there are no case samples. The file stores the correct
            output.
    no_control_input: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used to test the match function when there are no
            control samples. It is the input metadata for the funtion.
    no_control_output: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used to test if the match funtion gives the correct
            output when there are no control samples. The file stores the
            correct output.
    all_matches_input: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used as input to test the 'one' and 'only_matches'
            flags' effect on the function match.
    all_matches_output: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used to test if the match funtion gives the correct
            output when one is False and only_matches is False. The file
            stores the correct output.
    only_all_matches_output: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used to test if the match funtion gives the correct
            output when one is False and only_matches is True. The file stores
            the correct output.
    only_one_match_output: string
        Name of the tsv file that will be loaded into a metadata object. This
            object will be used to test if the match funtion gives the correct
            output when one is True and only_matches is True. The file stores
            the correct output.
    all_matches: string
        Name of the file that contains the lines to match the samples used when
            testing the exporting all matches instead of one to one and
            exporting only samples that got matched
    '''
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

    str_match = open("./%s/%s"%(unit, string_int_match),
        "r").read().splitlines()
    emp_file = open("./%s/%s"%(unit, empty_file), "r").read().splitlines()
    norm_match = open("./%s/%s"%(unit, normal_match), "r").read().splitlines()
    wcolumn_match = open("./%s/%s"%(unit, wrong_column_match),
        "r").read().splitlines()

    unit_norm_out = match_samples.matcher(verbose,
        norm_in, norm_match, True, False)
    unit_case_out = match_samples.matcher(verbose,
        no_case_in, norm_match, True, False)
    unit_control_out = match_samples.matcher(verbose,
        no_control_in, norm_match, True, False)
    unit_no_out = match_samples.matcher(verbose,
        no_in, norm_match, True, False)

    assert_raises(ValueError, match_samples.matcher, verbose,
        str_cont_in, norm_match, True, False)
    assert_raises(ValueError, match_samples.matcher, verbose,
        str_case_in, norm_match, True, False)
    assert_raises(ValueError, match_samples.matcher, verbose,
        norm_in, str_match, True, False)
    assert_raises(KeyError, match_samples.matcher, verbose,
        norm_in, wcolumn_match, True, False)

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

    #apg match tests
    all_in = Metadata.load("./%s/%s"%(unit, all_matches_input))
    all_out = Metadata.load("./%s/%s"%(unit, all_matches_output))
    all_only_matches_out = Metadata.load("./%s/%s"
        %(unit, only_all_matches_output))
    one_only_match_out = Metadata.load("./%s/%s"
        %(unit, only_one_match_output))
    all_match = open("./%s/%s"
        %(unit, all_matches),"r").read().splitlines()
    unit_all_out = match_samples.matcher(verbose, all_in, all_match,
        False, False)
    unit_only_all_out = match_samples.matcher(verbose, all_in, all_match,
        False, True)
    unit_only_one_out = match_samples.matcher(verbose, all_in, all_match,
        True, True)
    assert_frame_equal(all_out.to_dataframe(),  unit_all_out.to_dataframe())
    assert_frame_equal(all_only_matches_out.to_dataframe(),
                       unit_only_all_out.to_dataframe())
    #assert_frame_equal(one_only_match_out.to_dataframe(),
    #                   unit_only_one_out.to_dataframe())


def test_mainControler(verbose, unit, test_keep, test_case, test_control,
              test_nulls, test_match, unit_main_input):
    '''
    Tests that match_samples.py's mainControler function follows the correct
        steps based on different inputs

    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not.
            True outputs print statements.
    unit: string
        Location of the folder that holds the unit test files
    test_case: string
        Name of the query file that contains the normal case query
    test_control_in: string
        Name of the query file that contains the normal control query using IN
    test_keep: string
        Name of the query file that contains the sql queries to do a normal keep
    test_match: string
        Name of the file that contains the lines to match the samples normally
    test_nulls: string
        Name of the file that contains the null values used to prepare
            metadata objects for match in filter_prep_for_matchMD
    unit_main_input: string
        Name of the tsv file that will be loaded into a metadata object.
            This object will be used to test the logic of mainControler
            function.
    '''
    runner = CliRunner()

    #kccnm
    args = ["--inputdata", "./%s/%s"%(unit, unit_main_input),
        "--keep", "./%s/%s"%(unit, test_keep),
        "--control", "./%s/%s"%(unit, test_control),
        "--case", "./%s/%s"%(unit, test_case),
        "--nullvalues", "./%s/%s"%(unit, test_nulls),
        "--match", "./%s/%s"%(unit, test_match),
        "--one", "--unit"]
    unit_all_out = runner.invoke(match_samples.mainControler, args)
    ans = ("Calling keep_samples\n"
        "Calling determine_cases_and_controls\n"
        "Calling filter_prep_for_matchMD\n"
        "Calling matcher\n"
        "Returning metadata\n")
    assert_equals(ans, unit_all_out.output)

    #kccm
    args = ["--inputdata", "./%s/%s"%(unit, unit_main_input),
        "--keep", "./%s/%s"%(unit, test_keep),
        "--control", "./%s/%s"%(unit, test_control),
        "--case", "./%s/%s"%(unit, test_case),
        "--match", "./%s/%s"%(unit, test_match),
        "--one", "--unit"]
    unit_all_out = runner.invoke(match_samples.mainControler, args)
    ans = ("Calling keep_samples\n"
        "Calling determine_cases_and_controls\n"
        "Skipped filter_prep_for_matchMD\n"
        "Calling matcher\n"
        "Returning metadata\n")
    assert_equals(ans, unit_all_out.output)

    #kccn
    args = ["--inputdata", "./%s/%s"%(unit, unit_main_input),
        "--keep", "./%s/%s"%(unit, test_keep),
        "--control", "./%s/%s"%(unit, test_control),
        "--case", "./%s/%s"%(unit, test_case),
        "--nullvalues", "./%s/%s"%(unit, test_nulls),
        "--one", "--unit"]
    unit_all_out = runner.invoke(match_samples.mainControler, args)
    ans = ("Calling keep_samples\n"
        "Calling determine_cases_and_controls\n"
        "--nullvalues was given but --match was not so returning "
        "current metadata withouth null filtering\n")
    assert_equals(ans, unit_all_out.output)

    #kcc
    args = ["--inputdata", "./%s/%s"%(unit, unit_main_input),
        "--keep", "./%s/%s"%(unit, test_keep),
        "--control", "./%s/%s"%(unit, test_control),
        "--case", "./%s/%s"%(unit, test_case),
        "--one", "--unit"]
    unit_all_out = runner.invoke(match_samples.mainControler, args)
    ans = ("Calling keep_samples\n"
        "Calling determine_cases_and_controls\n"
        "Skipped filter_prep_for_matchMD\n"
        "Skipping matcher and returning metadata\n")
    assert_equals(ans, unit_all_out.output)

    #kcontrol
    args = ["--inputdata", "./%s/%s"%(unit, unit_main_input),
        "--keep", "./%s/%s"%(unit, test_keep),
        "--control", "./%s/%s"%(unit, test_control),
        "--one", "--unit"]
    unit_all_out = runner.invoke(match_samples.mainControler, args)
    ans = ("Calling keep_samples\n"
        "Skipped determine_cases_and_controls and returning the metadata\n")
    assert_equals(ans, unit_all_out.output)

    #kcase
    args = ["--inputdata", "./%s/%s"%(unit, unit_main_input),
        "--keep", "./%s/%s"%(unit, test_keep),
        "--case", "./%s/%s"%(unit, test_case),
        "--one", "--unit"]
    unit_all_out = runner.invoke(match_samples.mainControler, args)
    ans = ("Calling keep_samples\n"
        "Skipped determine_cases_and_controls and returning the metadata\n")
    assert_equals(ans, unit_all_out.output)

    #k
    args = ["--inputdata", "./%s/%s"%(unit, unit_main_input),
        "--keep", "./%s/%s"%(unit, test_keep),
        "--one", "--unit"]
    unit_all_out = runner.invoke(match_samples.mainControler, args)
    ans = ("Calling keep_samples\n"
        "Skipped determine_cases_and_controls and returning the metadata\n")
    assert_equals(ans, unit_all_out.output)

    #km
    args = ["--inputdata", "./%s/%s"%(unit, unit_main_input),
        "--keep", "./%s/%s"%(unit, test_keep),
        "--match", "./%s/%s"%(unit, test_match),
        "--one", "--unit"]
    unit_all_out = runner.invoke(match_samples.mainControler, args)
    ans = ("Calling keep_samples\n"
        "Skipped determine_cases_and_controls and returning the metadata\n")
    assert_equals(ans, unit_all_out.output)

    #ccnm
    args = ["--inputdata", "./%s/%s"%(unit, unit_main_input),
        "--control", "./%s/%s"%(unit, test_control),
        "--case", "./%s/%s"%(unit, test_case),
        "--nullvalues", "./%s/%s"%(unit, test_nulls),
        "--match", "./%s/%s"%(unit, test_match),
        "--one", "--unit"]
    unit_all_out = runner.invoke(match_samples.mainControler, args)
    ans = ("Skipped keep_samples\n"
        "Calling determine_cases_and_controls\n"
        "Calling filter_prep_for_matchMD\n"
        "Calling matcher\n"
        "Returning metadata\n")
    assert_equals(ans, unit_all_out.output)

    #ccm
    args = ["--inputdata", "./%s/%s"%(unit, unit_main_input),
        "--control", "./%s/%s"%(unit, test_control),
        "--case", "./%s/%s"%(unit, test_case),
        "--match", "./%s/%s"%(unit, test_match),
        "--one", "--unit"]
    unit_all_out = runner.invoke(match_samples.mainControler, args)
    ans = ("Skipped keep_samples\n"
        "Calling determine_cases_and_controls\n"
        "Skipped filter_prep_for_matchMD\n"
        "Calling matcher\n"
        "Returning metadata\n")
    assert_equals(ans, unit_all_out.output)

    #none
    args = ["--inputdata", "./%s/%s"%(unit, unit_main_input), "--one", "--unit"]
    unit_all_out = runner.invoke(match_samples.mainControler, args)
    ans = ("Skipped keep_samples\n"
        "Skipped determine_cases_and_controls and returning the metadata\n")
    assert_equals(ans, unit_all_out.output)


@click.command()
@click.option("--verbose", is_flag=True,
    help="Tells function if it should output print statements or not."
         "True outputs print statements.")
@click.option("--unittest_files",
    default="unitTest_files",
    help="Location of the folder that holds the unit test files")
@click.option("--test_case",
    default="test_case.txt",
    help="Name of the query file that contains the normal case query")
@click.option("--test_case_noentries",
    default="test_case_noentries.txt",
    help="Name of the query file that results in no cases being found."
         "This tests the that filtering everything out gives an error.")
@click.option("--test_control_in",
    default="test_control_in.txt",
    help="Name of the query file that contains the normal control query "
        "using IN")
@click.option("--test_control_notin",
    default="test_control_notin.txt",
    help="Name of the query file that contains the sql queries to do a normal "
        "control queries using NOT IN")
@click.option("--test_keep",
    default="test_keep.txt",
    help="Name of the query file that contains the sql queries to do a "
        "normal keep")
@click.option("--test_keep_noentries",
    default="test_keep_noentries.txt",
    help="Name of the query file that contains the sql queries that keeps "
        "not samples")
@click.option("--test_match",
    default="test_match.txt",
    help="Name of the file that contains the lines to match the samples "
        "normally")
@click.option("--test_match_error_column",
    default="test_match_error_column.txt",
    help="Name of the file that contains the lines to match samples but one "
        "of the columns in the file is not in the metadata input")
@click.option("--test_match_error_int_str",
    default="test_match_error_int_str.txt",
    help="Name of the file that contains the lines to match samples but the "
        "number for the age_years range is a string that can not be type "
        "cased to a float")
@click.option("--test_nulls",
    default="test_nulls.txt",
    help="Name of the file that contains the null values used to prepare "
        "metadata objects for match in filter_prep_for_matchMD")
@click.option("--test_nulls_noentries",
    default="test_nulls_noentries.txt",
    help="Name of the file that contains the null values used to prepare "
        "metadata objects for match in filter_prep_for_matchMD. The null "
        "values will filter every sample out which should result in an "
        "error.")
@click.option("--unit_case_input",
    default="unit_case_input.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used to test the case and control labeling "
        "functionality of the match_controls.py")
@click.option("--unit_case_output",
    default="unit_case_output.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used to test that valid case and control inputs "
        "get the correct output")
@click.option("--unit_keep_input",
    default="unit_keep_input.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used to test the keeping of samples "
        "functionality of the match_controls.py")
@click.option("--unit_keep_output",
    default="unit_keep_output.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used to test that valid inputs for keeping "
        "samples gets the correct output")
@click.option("--unit_match_input",
    default="unit_match_input.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used to test the matching of case and control "
        "labeled samples functionality of the match_controls.py")
@click.option("--unit_match_output",
    default="unit_match_output.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used to test that valid inputs for matching "
        "case and control samples yields the correct output")
@click.option("--unit_match_int_str_case",
    default="unit_match_int_str_case.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used to test")
@click.option("--unit_match_int_str_control",
    default="unit_match_int_str_control.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used to test")
@click.option("--unit_no_match_input",
    default="unit_no_match_input.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used to test the match function when there are "
        "no possible matches. It is the input metadata for the funtion.")
@click.option("--unit_no_match_output",
    default="unit_no_match_output.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used to test if the match funtion gives the "
        "correct output when there are no possible matches. The file stores "
        "the correct output.")
@click.option("--unit_no_null_input",
    default="unit_no_null_input.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used to test if giving a file with no null "
        "entries as input for null filtering returns an output equal to the "
        "input.")
@click.option("--unit_null_input",
    default="unit_null_input.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be as input to test that valid inputs for "
        "filtering out samples with null values in the columns used for "
        "matching gets the correct output.")
@click.option("--unit_null_output",
    default="unit_null_output.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be compared to output of the funtion that preps "
        "the metadata object for matching. It test that valid inputs for "
        "filtering out samples with null values in the columns used for "
        "matching gets the correct output.")
@click.option("--unit_no_cases_match_input",
    default="unit_no_cases_match_input.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used to test the match function when there are "
        "no case samples. It is the input metadata for the funtion.")
@click.option("--unit_no_cases_match_output",
    default="unit_no_cases_match_output.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used to test if the match funtion gives the "
        "correct output when there are no case samples. The file stores the "
        "correct output.")
@click.option("--unit_no_controls_match_input",
    default="unit_no_controls_match_input.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used to test the match function when there are "
        "no control samples. It is the input metadata for the funtion.")
@click.option("--unit_no_controls_match_output",
    default="unit_no_controls_match_output.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used to test if the match funtion gives the "
        "correct output when there are no control samples. The file stores "
        "the correct output.")
@click.option("--empty_file",
    default="empty_file.txt",
    help="Name of the empty file used in various tests")
@click.option("--all_matches_input",
    default="all_matches_input.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used as input to test the 'one' and "
        "'only_matches' flags' effect on the function match.")
@click.option("--all_matches_output",
    default="all_matches_output.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used to test if the match funtion gives the "
        "correct output when one is False and only_matches is False. The "
        "file stores the correct output.")
@click.option("--only_all_matches_output",
    default="only_all_matches_output.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used to test if the match funtion gives the "
        "correct output when one is False and only_matches is True. The "
        "file stores the correct output.")
@click.option("--only_one_match_output",
    default="only_one_match_output.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used to test if the match funtion gives the "
        "correct output when one is True and only_matches is True. The file "
        "stores the correct output.")
@click.option("--all_matches",
    default="all_matches.txt",
    help="Name of the file that contains the lines to match the samples "
        "used when testing the exporting all matches instead of one to one "
        "and exporting only samples that got matched")
@click.option("--unit_main_input",
    default="unit_main_input.tsv",
    help="Name of the tsv file that will be loaded into a metadata object. "
        "This object will be used to test the logic of mainControler function.")
def main(verbose, unittest_files, test_case, test_case_noentries, test_control_in,
         test_control_notin, test_keep, test_keep_noentries, test_match,
         test_match_error_column, test_match_error_int_str, test_nulls,
         test_nulls_noentries, unit_case_input, unit_case_output, unit_keep_input,
         unit_keep_output, unit_match_input, unit_match_int_str_case,
         unit_match_int_str_control, unit_match_output, unit_no_match_input,
         unit_no_match_output, unit_no_null_input, unit_null_input,
         unit_null_output, unit_no_cases_match_input, unit_no_cases_match_output,
         unit_no_controls_match_input, unit_no_controls_match_output, empty_file,
         all_matches_input, all_matches_output, only_all_matches_output,
         only_one_match_output, all_matches, unit_main_input):

    test_orderDict(verbose)
    test_order_keys(verbose)
    test_stable_marriage(verbose)

    test_get_user_input_query_lines(verbose, unittest_files, unit_keep_input,
        test_match)

    test_keep_samples(verbose, unittest_files, unit_keep_input,
        unit_keep_output, test_keep, test_keep_noentries, empty_file)

    test_determine_cases_and_controls(verbose, unittest_files, unit_case_input,
        unit_case_output, test_control_in, test_case, test_case_noentries,
        empty_file)

    test_filter_prep_for_matchMD(verbose, unittest_files, unit_null_input,
        unit_null_output, unit_no_null_input, test_nulls, test_match,
        test_match_error_column, test_nulls_noentries, empty_file)

    test_match_samples(verbose, unittest_files, unit_match_input,
        unit_match_output, test_match, unit_match_int_str_control,
        unit_match_int_str_case, test_match_error_column,
        test_match_error_int_str, unit_no_match_input, unit_no_match_output,
        empty_file, unit_no_cases_match_input, unit_no_cases_match_output,
        unit_no_controls_match_input, unit_no_controls_match_output,
        all_matches_input, all_matches_output, only_all_matches_output,
        only_one_match_output, all_matches)

    test_mainControler(verbose, unittest_files, test_keep, test_case,
        test_control_in, test_nulls, test_match, unit_main_input)




if __name__ == '__main__':
    main()
