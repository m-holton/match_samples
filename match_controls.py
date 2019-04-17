'''
Created on Jun 24, 2018

@author: Mark Holton
'''

import getopt, sys
import pandas as pd
import numpy as np
import qiime2
import time
import click

from qiime2 import Metadata
from collections import defaultdict

class Stable_Marriage:
    
    def orderDict(self, verbose, dictionary, value_frequency):
        '''
        orders the elements of each array that is associated with a sample key by how often they get matched to other samples
        least to greatest. Ties are sorted Alphanumbericly

        Parameters
        ----------
        verbose: boolean
            Tells function if it should output print statements or not. True outputs print statements.
        
        dictionary: dictionary
            keys are linked to arrays that contain strings that correspond to samples that match to the
            sample the key represents

        value_frequency: dictionary
            keys are samples found in arrays of dictionary. Elements are numerical representation of
            how many samples element matches to

        Returns
        -------
        dictionary: dictionary
            dictionary with elements of the arrays that correspond to keys ordered from least to greatest abundance
        '''
        for k in dictionary:
            dictionary[k] = sorted(dictionary[k])
            dictionary[k] = sorted(dictionary[k], key = lambda x:value_frequency[x] )
        return dictionary

    def order_keys(self, verbose, dictionary):
        '''
        orders the keys of a dictionary so that they can be used properly as the freemen of stable marriage. In order greatest to least since pop is used to get least freeman and pop takes the right most entry.

        Parameters
        ----------
        verbose: boolean
            Tells function if it should output print statements or not. True outputs print statements.
        
        dictionary
            dictionary of cases or controls with their matching controls or cases ordered
            by rising abundance

        Return
        ------
        keys_greatest_to_least: list
            contains keys in order of greatest to least amount of samples they match to
        '''
        keys_greatest_to_least = sorted(dictionary, key=lambda x: len (dictionary[x]), reverse=True)
        return keys_greatest_to_least

    def stableMarriageRunner(self, verbose, case_dictionary, pref_counts_control, pref_counts_case):
        '''
        based on code shown by Tyler Moore in his slides for Lecture 2 for CSE 3353, SMU, Dallas, TX
        these slides can be found at https://tylermoore.ens.utulsa.edu/courses/cse3353/slides/l02-handout.pdf

        Gets back the best way to match samples to eachother to in a one to one manner. Best way refers to getting back the most amount of one to one matches.

        Parameters
        ----------
        verbose: boolean
            Tells function if it should output print statements or not. True outputs print statements.
        
        case_dictionary: dictionary
            case_dictionary is a dictionary of cases with their matching controls 

        pref_counts_control: dictionary
            pref_counts_control is a dictionary with the frequency control match to something in control_dictionary. How many case samples each control sample matches to.
            
        pref_counts_case: dictionary
            pref_counts_case is a dictionary with the frequency cases match to something in case_dictionary

        Returns
        -------
        one_to_one_match_dictionary: dictionary
            dictionary with keys representing control samples and their corresponding values representing a match between a case and control sample
        '''
        #orders control samples (elements) by rising abundance of how many case samples they match to
        case_dictionary = self.orderDict(verbose, case_dictionary, pref_counts_control)
        #first make master copy
        master_copy_of_case_dict = case_dictionary.copy()

        free_keys = self.order_keys(verbose, case_dictionary)

        one_to_one_match_dictionary = {}
        while free_keys :
            key = free_keys.pop()
            if case_dictionary[key]==[]:
                continue
            #get the highest ranked woman that has not yet been proposed to
            entry = case_dictionary[key].pop()

            if entry not in one_to_one_match_dictionary:
                one_to_one_match_dictionary[entry] = key
                #remove key to reorder but this my not be the best if a switch is needed later
                if case_dictionary[key]==[]:
                    case_dictionary.pop(key,None)
                for case_key in case_dictionary:
                    if entry in case_dictionary[case_key]:
                        case_dictionary[case_key].remove(entry)
                #reorder keys
                free_keys = self.order_keys(verbose, case_dictionary)

            else:
                key_in_use = one_to_one_match_dictionary[entry]
                if pref_counts_case[key] < pref_counts_case[key_in_use]:
                    one_to_one_match_dictionary[entry] = key
                    free_keys.append(key_in_use)
                else:
                    free_keys.append(key)

        return one_to_one_match_dictionary
    
    
    

    
    
    
    
def get_user_input_query_lines(verbose, dictofFiles):
    '''
    Uses a dictionary of files path/names(dictofFiles) to create a new dictionary (dict_of_file_lines) of arrays that represent the lines of each file from the origianal input dictionary (dictofFiles)

    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not. True outputs print statements.
    
    dictofFiles: dictionary of strings 
        Each key is what the string is for like inputdata being the input metadata file. The element of the each key is a file path/name 

    Returns
    -------
    dict_of_file_lines: ditioary of arrays of strings
        The dictionary has the keys that have some value in dictofFiles. The elements are an array of the lines of the file the key corrisponds to.
    
     
    '''
    #dictOfReturnValues = {"inputdata":None, "keep":None, "control":None, "case":None, "nullvalues":None, "match":None}
    dict_of_file_lines = {}
    for key in dictofFiles:
        if dictofFiles[key] is None:
            continue
        if key == "inputdata":
            #read metadata file into metadata object
            if verbose:
                print("metadata file path entered is %s"%(dictofFiles[key]))
            try:
                dict_of_file_lines[key] = Metadata.load(dictofFiles[key])
            except:
                raise ValueError('metadata file could not load. The file must be a TSV metadata file.')
        else:
            if verbose:
                    print("file path entered is %s"%(dictofFiles[key]))
            try:
                dict_of_file_lines[key] = open('./%s'%(dictofFiles[key]),'r').readlines()
            except:
                raise ValueError('File could not be opened') 
    return dict_of_file_lines


def keep_samples(verbose, original_MD, keep_query_lines):
    '''
    Filters out unwanted rows based on values in chosen columns detailed in keep_query_lines.

    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not. True outputs print statements.
        
    original_MD : Metadata object
        Metadata object with all samples

    keep_query_lines : array of strings
        list of strings that are the lines of the file
        each string is a sqlite query that determines what ids to keep

    Returns
    -------
    shrunk_MD : Metadata object
        original_MD input except that desired exclution has been applied so only the samples that match the input querys
        are kept
    '''
    try:
        initial_size = original_MD.id_count
        ids = original_MD.get_ids(' AND '.join(keep_query_lines))
        shrunk_MD = original_MD.filter_ids(ids)
        if verbose:
            print("size of original MetaData Object = %s   size of filtered MetaData Object = %s"%(initial_size, shrunk_MD.id_count))
            print("filtered out %s samples"%(initial_size-shrunk_MD.id_count))
            print("kept %s samples"%(shrunk_MD.id_count))
    except:
        raise Exception('No samples fulfill keep queries. Exited while filtering out unwanted samples')
        
    return shrunk_MD


def determine_cases_and_controls(verbose, afterExclusion_MD, query_line_dict, case_controlDF):
    '''
    Determines what samples are cases or controls using the queries in query_line_array. The labels of each sample are
    stored in case_controlDF

    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not. True outputs print statements.
        
    afterExclusion_MD : Metadata object
        Metadata object with unwanted samples filtered out

    query_line_array : array of arrays of strings
        there are two sub arrays
        the first array are made of queries to determine controls
        the second array are made of queries to determine cases

    case_controlDF : dataframe
        dataframe with one column named case_control. The indexs are the same as the indexs of afterExclution_MD
        all values are Undefined to start

    Returns
    -------
    mergedMD : Metadata object
        Metadata object with unwanted samples filtered out and a case_control column that reflects if the index is
        a case, control, or Undefined
    '''
    if verbose:
        print("Metadata Object has %s samples"%(afterExclusion_MD.id_count))
    for key in query_line_dict:
        if key != 'case' and key != 'control':
            if verbose:
                print("Wrong keys used for query. Must be 'case' or 'control'.")
            continue
        #resets shrunk_MD so that filtering down to control samples does not influence filtering down to case
        shrunk_MD = afterExclusion_MD
        #get query and filtering down to control or case samples based on key
        query_lines = query_line_dict[key]
        try:
            ids = shrunk_MD.get_ids(' AND '.join(query_lines))
            shrunk_MD = shrunk_MD.filter_ids(ids)
            if verbose:
                print("%s %s samples "%(shrunk_MD.id_count,key))
        except:
            raise Exception('No samples fulfill %s queries. Exited while determining %s samples'%(key, key))


        #replaces the true values created by the loop above to case or control
        ids = shrunk_MD.ids
        case_controlDF.loc[ids,'case_control'] = key

    #turns case_controlDF into a metadata object
    case_controlMD = Metadata(case_controlDF)

    #merges afterExclution_MD and case_controlMD into one new metadata object
    mergedMD = Metadata.merge(afterExclusion_MD, case_controlMD)

    return mergedMD

def filter_prep_for_matchMD(verbose, merged_MD, match_condition_lines, null_value_lines):
    '''
    filters out samples that do not have valid entries (null values) for columns that determine matching

    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not. True outputs print statements.
        
    merged_MD : Metadata object
        has case_control with correct labels but some samples might not have all matching information

    match_condition_lines : array of strings
        contains conditons to match samples on. In this function it is used only to get the columns for matching.

    null_value_lines : array of strings
        contains strings that corrrespond to the null values in the dataset that is being analysed

    Returns
    -------
    returned_MD : Metadata object
        Samples that do not have valid entries for columns that determine matching are removed. Everything else is the
        same as merged_MD.
    '''
    returned_MD = merged_MD
    if verbose:
        totalNumOfSamples = returned_MD.id_count
        print("%s samples before filtered out null samples"%(returned_MD.id_count))
    for condition in match_condition_lines:
        column = condition.split('\t')[1].strip()
        try:
            returned_MD.get_column(column)
        except:
            raise Exception('Column %s not found in your input data. Correct this error in your --match/-m file'%(column))
            
        #Get the ids of samples in the metadata object that have non null values for every column used for matching
        try:
            ids = returned_MD.get_ids(column + ' NOT IN ' + null_value_lines[0])
        except:
            raise Exception('No samples pass null filter queries. Exited while determining non null samples')
            
        #shrinks the MD so that future ids do not include samples that fail past queries
        returned_MD = returned_MD.filter_ids(ids)
        
    if verbose:
        print("%s samples filtered out due to null samples"%(totalNumOfSamples-returned_MD.id_count))
        print("%s samples after filtering out null samples"%(returned_MD.id_count))

    return returned_MD


def match_samples(verbose, prepped_for_match_MD, conditions_for_match_lines):
    '''
    matches case samples to controls and puts the case's id in column matched to on the control sample's row

    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not. True outputs print statements.
    
    prepped_for_match_MD : Metadata object
        Samples that do not have valid entries for columns that determine matching are removed. Everything else is the
        same as merged_MD.

    conditions_for_match_lines : array of strings
        contains information on what conditions must be met to constitue a match

    Returns
    -------
    masterDF : dataframe
        masterDF with matches represented by a column called matched to. Values in matched to are the sample ids of the
        sample samples matches to

    '''
    case_dictionary = {}
    control_dictionary = {}
    control_match_count_dictionary = {}
    case_match_count_dictionary = {}

    matchDF = prepped_for_match_MD.to_dataframe()
    case_for_matchDF = matchDF[matchDF['case_control'].isin(['case'])]
    # creates column to show matches. since it will contain the sample number it was matched too the null value will be 0
    matchDF['matched_to'] = '0'

    # loops though case samples and matches them to controls
    for case_index, case_row in case_for_matchDF.iterrows():
        #print('case index is %s'%(case_index))

        # set matchDF to be only the samples of masterDF that are control samples
        controlDF = matchDF[matchDF['case_control'].isin(['control'])]

        # loop though input columns to determine matches
        for conditions in conditions_for_match_lines:

            column_name = conditions.split('\t')[1].strip()

            # get the type of data for the given column. This determine how a match is determined
            if conditions.split('\t')[0] == 'range':
                num = conditions.split('\t')[2].strip()
                
                try:
                    row_num = float(case_row[column_name])
                except:
                    raise ValueError('%s is not a a valid number'%(case_row[column_name]))
                try:
                    fnum = float(num)
                except:
                    raise ValueError('input number for condition %s is not a a valid number'%(column_name))
                try:
                    nums_in_column = pd.to_numeric(controlDF[column_name])
                except:
                    raise ValueError('column %s contains a string that can not be converted to a numerical value'%(column_name))

                # filters controls based on if the value in the control is not within a given distance form the case
                controlDF = controlDF[
                                    ( nums_in_column >= ( row_num - fnum ) )
                                    &
                                    ( nums_in_column <= ( row_num + fnum ) )
                                    ]
            else:
                # filters controls if the strings for the control and case don't match
                controlDF = controlDF[controlDF[column_name].isin([case_row[column_name]])]

        case_dictionary.update({case_index:controlDF.index.values})
        case_match_count_dictionary.update({case_index:(controlDF.index.values.size)})

        for id_control in controlDF.index:
            if id_control not in control_match_count_dictionary:
                control_match_count_dictionary.update({id_control:0})
            control_match_count_dictionary.update({id_control:(control_match_count_dictionary[id_control]+1)})

    stable = Stable_Marriage()
    case_to_control_match = stable.stableMarriageRunner(verbose, case_dictionary, control_match_count_dictionary, case_match_count_dictionary)

    if verbose:
        print("%s sample pairs matched together"%(len(case_to_control_match.keys())))
        
    for key in case_to_control_match:
        key_value = case_to_control_match[key]
        matchDF.loc[ key, 'matched_to'] = key_value
        matchDF.loc[ key_value, 'matched_to'] = key

    return Metadata(matchDF)






def KeepOnly(verbose,inputdata,keep,output):
    '''
   
    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not. True outputs print statements.
    inputdata: string
        Name of file with sample metadata to analyze.
    keep: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    control: string
        name of file with sqlite lines used to determine what samples to label control
    case: string
        name of file with sqlite lines used to determine what samples to label case
    nullvalues: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    match: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    output: string
        Name of file to export data to.
   
    
    '''
    
    tstart = time.clock()
    inputDict = {"inputdata":inputdata, "keep":keep, "control":None, "case":None, "nullvalues":None, "match":None}
    #loads and opens input files
    inputDict = get_user_input_query_lines(verbose,inputDict)
    
    tloadedFiles = time.clock()
    if verbose:
        print('Time to load input files is %s'%(tloadedFiles - tstart))

    afterExclusionMD = keep_samples(verbose, inputDict["inputdata"], inputDict["keep"])
    afterExclusionMD.to_dataframe().to_csv(output, sep = '\t')

    tkeep = time.clock()
    tend = time.clock()

    if verbose:
        print('Time to filter out unwanted samples is %s'%(tkeep - tloadedFiles))
        print('Time to do everything %s'%(tend-tstart))




def ControlAndCaseOnly(verbose,inputdata,control,case,output):
    '''

    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not. True outputs print statements.
    inputdata: string
        Name of file with sample metadata to analyze.
    keep: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    control: string
        name of file with sqlite lines used to determine what samples to label control
    case: string
        name of file with sqlite lines used to determine what samples to label case
    nullvalues: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    match: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    output: string
        Name of file to export data to.
   
    
    '''
    
    tstart = time.clock()
    inputDict = {"inputdata":inputdata, "keep":None, "control":control, "case":case, "nullvalues":None, "match":None}
    #loads and opens input files
    inputDict = get_user_input_query_lines(verbose,inputDict)

    tloadedFiles = time.clock()
    if verbose:
        print('Time to load input files is %s'%(tloadedFiles - tstart))
        
    ids = inputDict["inputdata"].get_ids()
    case_control_Series = pd.Series( ['Unspecified'] * len(ids), ids)
    '''
    ['Unspecified'] * len(ids) creates a list of elements. The list is the
    same length as ids. All the elements are 'Unspecified'
    '''
    case_control_Series.index.name = inputDict["inputdata"].id_header
    case_controlDF = case_control_Series.to_frame('case_control')
    case_control_dict = {'case':inputDict["case"], 'control':inputDict["control"] }
    case_controlMD = determine_cases_and_controls(verbose, inputDict["inputdata"], case_control_dict, case_controlDF)

    case_controlMD.to_dataframe().to_csv(output, sep = '\t')

    tcase_control = time.clock()
    tend = time.clock()
    if verbose:
        print('Time to label case and control samples is %s'%(tcase_control - tloadedFiles))
        print('Time to do everything %s'%(tend-tstart))
        

def KeepAndControlCase(verbose,inputdata,keep,control,case,output):
    '''

    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not. True outputs print statements.
    inputdata: string
        Name of file with sample metadata to analyze.
    keep: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    control: string
        name of file with sqlite lines used to determine what samples to label control
    case: string
        name of file with sqlite lines used to determine what samples to label case
    nullvalues: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    match: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    output: string
        Name of file to export data to.
   
    
    '''
    
    tstart = time.clock()
    inputDict = {"inputdata":inputdata, "keep":keep, "control":control, "case":case, "nullvalues":None, "match":None}
    #loads and opens input files
    inputDict = get_user_input_query_lines(verbose,inputDict)

    tloadedFiles = time.clock()
    if verbose:
        print('Time to load input files is %s'%(tloadedFiles - tstart))
    afterExclusionMD = keep_samples(verbose, inputDict["inputdata"], inputDict["keep"])
    tkeep = time.clock()
    if verbose:
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

    case_controlMD = determine_cases_and_controls(verbose, afterExclusionMD, case_control_dict, case_controlDF)
    case_controlMD.to_dataframe().to_csv(output, sep = '\t')
    tcase_control = time.clock()
    tend = time.clock() 
    if verbose:
        print('Time to label case and control samples is %s'%(tcase_control - tkeep))
        print('Time to do everything %s'%(tend-tstart))

    
def ControlCaseAndMatch(verbose,inputdata,control,case,match,output):
    '''

    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not. True outputs print statements.
    inputdata: string
        Name of file with sample metadata to analyze.
    keep: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    control: string
        name of file with sqlite lines used to determine what samples to label control
    case: string
        name of file with sqlite lines used to determine what samples to label case
    nullvalues: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    match: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    output: string
        Name of file to export data to.
   
     
    '''
    
    tstart = time.clock()
    inputDict = {"inputdata":inputdata, "keep":None, "control":control, "case":case, "nullvalues":None, "match":match}
    #loads and opens input files
    inputDict = get_user_input_query_lines(verbose,inputDict)    
    
    tloadedFiles = time.clock()
    if verbose:
        print('Time to load input files is %s'%(tloadedFiles - tstart))

    ids = inputDict["inputdata"].get_ids()
    case_control_Series = pd.Series( ['Unspecified'] * len(ids), ids)
    '''
    ['Unspecified'] * len(ids) creates a list of elements. The list is the
    same length as ids. All the elements are 'Unspecified'
    '''
    case_control_Series.index.name = inputDict["inputdata"].id_header
    case_controlDF = case_control_Series.to_frame('case_control')
    case_control_dict = {'case':inputDict["case"], 'control':inputDict["control"] }
    case_controlMD = determine_cases_and_controls(verbose, inputDict["inputdata"], case_control_dict, case_controlDF)

    tcase_control = time.clock()
    if verbose:
        print('Time to label case and control samples is %s'%(tcase_control - tloadedFiles))

    matchedMD = match_samples(verbose, case_controlMD, inputDict["match"] )
    matchedMD.to_dataframe().to_csv(output, sep = '\t')

    tmatch = time.clock()
    tend = time.clock()
    if verbose:
        print('Time to match is %s'%(tmatch- tcase_control))
        print('Time to do everything %s'%(tend-tstart))






def ControlCaseNullAndMatch(verbose,inputdata,control,case,nullvalues,match,output):
    '''
    

    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not. True outputs print statements.
    inputdata: string
        Name of file with sample metadata to analyze.
    keep: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    control: string
        name of file with sqlite lines used to determine what samples to label control
    case: string
        name of file with sqlite lines used to determine what samples to label case
    nullvalues: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    match: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    output: string
        Name of file to export data to.
   
    
     
    '''
    
    tstart = time.clock()
    inputDict = {"inputdata":inputdata, "keep":None, "control":control, "case":case, "nullvalues":nullvalues, "match":match}
    #loads and opens input files
    inputDict = get_user_input_query_lines(verbose,inputDict)
    
    tloadedFiles = time.clock()
    if verbose:
        print('Time to load input files is %s'%(tloadedFiles - tstart))

    ids = inputDict["inputdata"].get_ids()
    case_control_Series = pd.Series( ['Unspecified'] * len(ids), ids)
    '''
    ['Unspecified'] * len(ids) creates a list of elements. The list is the
    same length as ids. All the elements are 'Unspecified'
    '''
    case_control_Series.index.name = inputDict["inputdata"].id_header
    case_controlDF = case_control_Series.to_frame('case_control')
    case_control_dict = {'case':inputDict["case"], 'control':inputDict["control"] }

    case_controlMD = determine_cases_and_controls(verbose, inputDict["inputdata"], case_control_dict, case_controlDF)

    tcase_control = time.clock()
    if verbose:
        print('Time to label case and control samples is %s'%(tcase_control - tloadedFiles))


    prepped_for_matchMD= filter_prep_for_matchMD(verbose, case_controlMD, inputDict["match"], inputDict["nullvalues"])

    tprepped = time.clock()
    if verbose:
        print('Time to filter Metadata information for samples with null values is %s'%(tprepped - tcase_control))

    if inputDict["match"] != False:
        matchedMD = match_samples(verbose, prepped_for_matchMD, inputDict["match"] )
        matchedMD.to_dataframe().to_csv(output, sep = '\t')

    tmatch = time.clock()
    tend = time.clock()
    if verbose:
        print('Time to match is %s'%(tmatch- tprepped))
        print('Time to do everything %s'%(tend-tstart))




def ExcludeControlCaseAndMatch(verbose,inputdata,keep,control,case,match,output):
    '''
    

    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not. True outputs print statements.
    inputdata: string
        Name of file with sample metadata to analyze.
    keep: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    control: string
        name of file with sqlite lines used to determine what samples to label control
    case: string
        name of file with sqlite lines used to determine what samples to label case
    nullvalues: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    match: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    output: string
        Name of file to export data to.
   
    
     
    '''
    
    tstart = time.clock()
    inputDict = {"inputdata":inputdata, "keep":keep, "control":control, "case":case, "nullvalues":None, "match":match}
    #loads and opens input files
    inputDict = get_user_input_query_lines(verbose,inputDict)
    tloadedFiles = time.clock()
    if verbose:
        print('Time to load input files is %s'%(tloadedFiles - tstart))
    afterExclusionMD = keep_samples(verbose, inputDict["inputdata"], inputDict["keep"])
    tkeep = time.clock()
    if verbose:
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

    case_controlMD = determine_cases_and_controls(verbose, afterExclusionMD, case_control_dict, case_controlDF)


    tcase_control = time.clock()
    if verbose:
        print('Time to label case and control samples is %s'%(tcase_control - tkeep))

    if inputDict["match"] != False:
        matchedMD = match_samples(verbose, case_controlMD, inputDict["match"] )
        matchedMD.to_dataframe().to_csv(output, sep = '\t')

    tmatch = time.clock()
    tend = time.clock()
    if verbose:
        print('Time to match is %s'%(tmatch- tcase_control))
        print('Time to do everything %s'%(tend-tstart))



def Everything(verbose,inputdata,keep,control,case,nullvalues,match,output):
    '''
    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not. True outputs print statements.
    inputdata: string
        Name of file with sample metadata to analyze.
    keep: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    control: string
        name of file with sqlite lines used to determine what samples to label control
    case: string
        name of file with sqlite lines used to determine what samples to label case
    nullvalues: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    match: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    output: string
        Name of file to export data to.


    '''
    
    tstart = time.clock()
    inputDict = {"inputdata":inputdata, "keep":keep, "control":control, "case":case, "nullvalues":nullvalues, "match":match}
    #loads and opens input files
    inputDict = get_user_input_query_lines(verbose,inputDict)
    
    tloadedFiles = time.clock()
    if verbose:
        print('Time to load input files is %s'%(tloadedFiles - tstart))
    afterExclusionMD = keep_samples(verbose, inputDict["inputdata"], inputDict["keep"])
    tkeep = time.clock()
    if verbose:
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

    case_controlMD = determine_cases_and_controls(verbose, afterExclusionMD, case_control_dict, case_controlDF)

    tcase_control = time.clock()
    if verbose:
        print('Time to label case and control samples is %s'%(tcase_control - tkeep))

    prepped_for_matchMD= filter_prep_for_matchMD(verbose, case_controlMD, inputDict["match"], inputDict["nullvalues"])

    tprepped = time.clock()
    if verbose:
        print('Time to filter Metadata information for samples with null values is %s'%(tprepped - tcase_control))

    if inputDict["match"] != False:
        matchedMD = match_samples(verbose, prepped_for_matchMD, inputDict["match"] )
        matchedMD.to_dataframe().to_csv(output, sep = '\t')
    tmatch = time.clock()
    tend = time.clock()
    if verbose:
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
def mainControler(verbose,inputdata,keep,control,case,nullvalues,match,output):
    '''
    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not. True outputs print statements.
    inputdata: string
        Name of file with sample metadata to analyze.
    keep: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    control: string
        name of file with sqlite lines used to determine what samples to label control
    case: string
        name of file with sqlite lines used to determine what samples to label case
    nullvalues: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    match: string
        name of file with sqlite lines used to determine what samples to exclude or keep
    output: string
        Name of file to export data to.
   
    Returns
    -------
    string
        string is the name of the function called

    '''
    
    if isinstance(keep, str):
        if isinstance(control, str) and isinstance(case, str):
                if isinstance(match, str):
                    if isinstance(nullvalues, str):
                        if verbose:
                            print("Calling Everything")
                            Everything(verbose,inputdata,keep,control,case,nullvalues,match,output)
                            return "Everything"
                    else:
                        if verbose:
                            print("Calling ExcludeControlCaseAndMatch")
                        ExcludeControlCaseAndMatch(verbose,inputdata,keep,control,case,match,output)
                        return "ExcludeControlCaseAndMatch"
                else:
                    if verbose:
                            print("Calling KeepAndControlCase")
                    KeepAndControlCase(verbose,inputdata,keep,control,case,output)
                    return "KeepAndControlCase"
        else:
            if verbose:
                print("Calling KeepOnly")
            KeepOnly(verbose,inputdata,keep,output)
            return "KeepOnly"
    elif isinstance(control, str) and isinstance(case, str):
        if isinstance(match, str):
            if isinstance(nullvalues, str):
                if verbose:
                    print("Calling ControlCaseNullAndMatch")
                ControlCaseNullAndMatch(verbose,inputdata,control,case,nullvalues,match,output)
                return "ControlCaseNullAndMatch"
            else:
                if verbose:
                    print("Calling ControlCaseAndMatch")
                ControlCaseAndMatch(verbose,inputdata,control,case,match,output)
                return "ControlCaseAndMatch"
        else:
            if verbose:
                print("Calling ControlAndCaseOnly")
            ControlAndCaseOnly(verbose,inputdata,control,case,output)
            return "ControlAndCaseOnly"
    elif verbose:
        print("No Functions Called")
        
    
    
    
if __name__ == '__main__':
    mainControler()

