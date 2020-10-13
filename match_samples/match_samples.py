import time
import pandas as pd

from q2_types.feature_table import FeatureTable, Frequency, RelativeFrequency
from qiime2 import Metadata
from match_samples import match_functions as mf



def subsetting(output_dir, metadata: Metadata, keep: str, extra) -> None:
    '''
    Parameters
    ----------
    output_dir: string
        directory where visualization will be output
    metadata: Metadata
        Metadata object to analyze.
    keep: string
        name of file with sqlite lines used to determine what samples 
            to exclude or keep
    extra: boolean
        Dictates if funtions that subset metadata do the subsetting
            in one or multiple steps
    '''
    from qiime2.plugins.metadata.visualizers import tabulate

    tstart = time.clock()
    inputDict = { "keep":keep}
    #loads and opens input files
    inputDict = mf.get_user_input_query_lines(inputDict)
    tloadedFiles = time.clock()

    print("Calling keep_samples")
    afterExclusionMD = mf.keep_samples(metadata,
            inputDict["keep"], extra)
    tkeep = time.clock()
    print("Time to filter out unwanted samples is %s"
          %(tkeep - tloadedFiles))

    vis = tabulate(afterExclusionMD)
    vis.visualization.export_data(output_dir)
    tend = time.clock()
    print("Time to do everything %s"%(tend - tstart))
    




def labeler_no_subset(output_dir, metadata: Metadata, control: str, 
                      case: str, extra) -> None:
    '''
    Parameters
    ----------
    output_dir: string
        directory where visualization will be output
    metadata: Metadata
        Metadata object to analyze.
    control: string
        name of file with sqlite lines used to determine what 
            samples to label control
    case: string
        name of file with sqlite lines used to determine what 
            samples to label case
    extra: boolean
        Dictates if funtions that subset metadata do the subsetting
            in one or multiple steps
    '''
    from qiime2.plugins.metadata.visualizers import tabulate
    #from qiime2.plugins import metadata as plugMD


    tstart = time.clock()
    inputDict = {"control":control, "case":case}
    #loads and opens input files
    inputDict = mf.get_user_input_query_lines(inputDict)
    tloadedFiles = time.clock()

    print("Calling determine_cases_and_controls")
    case_control_dict = {"case":inputDict["case"],
            "control":inputDict["control"]}
    case_controlMD = mf.determine_cases_and_controls(
            metadata, case_control_dict, extra)
    tcase_control = time.clock()
    print("Time to label case and control samples is %s"
          %(tcase_control - tloadedFiles))

    vis = tabulate(case_controlMD)
    vis.visualization.export_data(output_dir)
    tend = time.clock()
    print("Time to do everything %s"%(tend - tstart))










def complete_labeler(output_dir, metadata: Metadata, keep:str, 
                     control:str, case:str, extra) -> None:
    '''
    Parameters
    ----------
    output_dir: string
        directory where visualization will be output
    metadata: Metadata
        Metadata object to analyze.
    keep: string
        name of file with sqlite lines used to determine what 
            samples to exclude or keep
    control: string
        name of file with sqlite lines used to determine what 
            samples to label control
    case: string
        name of file with sqlite lines used to determine what 
            samples to label case
    extra: boolean
        Dictates if funtions that subset metadata do the subsetting
            in one or multiple steps

    '''
    from qiime2.plugins.metadata.visualizers import tabulate

    tstart = time.clock()
    inputDict = {"keep":keep, "control":control, "case":case}
    #loads and opens input files
    inputDict = mf.get_user_input_query_lines(inputDict)
    tloadedFiles = time.clock()

    print("Calling keep_samples")
    afterExclusionMD = mf.keep_samples(metadata, inputDict["keep"], 
                                       extra)
    tkeep = time.clock()
    print("Time to filter out unwanted samples is %s"
          %(tkeep - tloadedFiles))

    print("Calling determine_cases_and_controls")
    case_control_dict = {"case":inputDict["case"],
            "control":inputDict["control"]}
    case_controlMD = mf.determine_cases_and_controls(
            afterExclusionMD, case_control_dict, extra)
    tcase_control = time.clock()
    print("Time to label case and control samples is %s"
          %(tcase_control - tkeep))

    vis = tabulate(case_controlMD)
    vis.visualization.export_data(output_dir)
    tend = time.clock()
    print("Time to do everything %s"%(tend - tstart))







def matching_no_subset_null_filter(output_dir, metadata: Metadata,
                                control:str, case:str, match:str,
                                one:bool=False,
                                only_matches:bool=False,
                                extra) -> None:
    '''
    Parameters
    ----------
    output_dir: string
        directory where visualization will be output
    metadata: Metadata
        Metadata object to analyze.
    control: string
        name of file with sqlite lines used to determine what 
            samples to label control
    case: string
        name of file with sqlite lines used to determine what 
            samples to label case
    match: string
        name of file which contains information on what conditions
            must be met to constitue a match
    one: boolean
        When given as a parameter match_samples will do one to
             one matching instead of all matches
    only_matches: boolean
        When given as a parameter match_samples will filter out
            non-matched samples from output file
    extra: boolean
        Dictates if funtions that subset metadata do the subsetting
            in one or multiple steps
    '''
    from qiime2.plugins.metadata.visualizers import tabulate

    tstart = time.clock()
    inputDict = {"metadata":metadata, "control":control,
        "case":case, "match":match}
    #loads and opens input files
    inputDict = mf.get_user_input_query_lines(inputDict)
    tloadedFiles = time.clock()

    print("Calling determine_cases_and_controls")
    case_control_dict = {"case":inputDict["case"],
            "control":inputDict["control"]}
    case_controlMD = mf.determine_cases_and_controls(
            metadata, case_control_dict, extra)
    tcase_control = time.clock()
    print("Time to label case and control samples is %s"
          %(tcase_control - tloadedFiles))

    print("Calling matcher")
    matchedMD = mf.matcher(case_controlMD,
                        inputDict["match"], one, only_matches)
    tmatch = time.clock()
    print("Time to match is %s"%(tmatch - tcase_control))

    vis = tabulate(matchedMD)
    vis.visualization.export_data(output_dir)
    tend = time.clock()
    print("Time to do everything %s"%(tend - tstart))




def matching_no_subset(output_dir, metadata: Metadata,
                       control:str, case:str, nullvalues:str,
                       match:str, one:bool=False, 
                       only_matches:bool=False,
                       extra) -> None:
    '''
    Parameters
    ----------
    output_dir: string
        directory where visualization will be output
    metadata: Metadata
        Metadata object to analyze.
    control: string
        name of file with sqlite lines used to determine what 
            samples to label control
    case: string
        name of file with sqlite lines used to determine what 
            samples to label case
    nullvalues: string
        name of file with strings that represent null values so that
            samples where one of these null values are in a category
            that is used to determine matches are filtered out
    match: string
        name of file which contains information on what conditions
            must be met to constitue a match
    one: boolean
        When given as a parameter match_samples will do one to
             one matching instead of all matches
    only_matches: boolean
        When given as a parameter match_samples will filter out
            non-matched samples from output file
    extra: boolean
        Dictates if funtions that subset metadata do the subsetting
            in one or multiple steps
    '''
    from qiime2.plugins.metadata.visualizers import tabulate

    tstart = time.clock()
    inputDict = { "control":control,
        "case":case, "nullvalues":nullvalues, "match":match}
    #loads and opens input files
    inputDict = mf.get_user_input_query_lines(inputDict)
    tloadedFiles = time.clock()

    print("Calling determine_cases_and_controls")
    case_control_dict = {"case":inputDict["case"],
            "control":inputDict["control"]}
    case_controlMD = mf.determine_cases_and_controls(
            metadata, case_control_dict, extra)
    tcase_control = time.clock()
    print("Time to label case and control samples is %s"
          %(tcase_control - tloadedFiles))

    print("Calling filter_prep_for_matchMD")
    prepped_for_matchMD = mf.filter_prep_for_matchMD(
        case_controlMD, inputDict["match"], inputDict["nullvalues"])
    tprepped = time.clock()
    print("Time to filter Metadata information for samples "
          "with null values is %s"%(tprepped - tcase_control))

    print("Calling matcher")
    matchedMD = mf.matcher(prepped_for_matchMD,
                        inputDict["match"], one, only_matches)
    tmatch = time.clock()
    print("Time to match is %s"%(tmatch - tprepped))

    vis = tabulate(matchedMD)
    vis.visualization.export_data(output_dir)
    tend = time.clock()
    print("Time to do everything %s"%(tend - tstart))




def matching_no_null_filter(output_dir, metadata: Metadata, keep:str,
                            control:str, case:str, match:str, 
                            one:bool=False, 
                            only_matches:bool=False, 
                            extra) -> None:
    '''
    Parameters
    ----------
    output_dir: string
        directory where visualization will be output
    metadata: Metadata
        Metadata object to analyze.
    keep: string
        name of file with sqlite lines used to determine what 
            samples to exclude or keep
    control: string
        name of file with sqlite lines used to determine what 
            samples to label control
    case: string
        name of file with sqlite lines used to determine what 
            samples to label case
    match: string
        name of file which contains information on what conditions
            must be met to constitue a match
    one: boolean
        When given as a parameter match_samples will do one to
             one matching instead of all matches
    only_matches: boolean
        When given as a parameter match_samples will filter out
            non-matched samples from output file
    extra: boolean
        Dictates if funtions that subset metadata do the subsetting
            in one or multiple steps
    '''
    from qiime2.plugins.metadata.visualizers import tabulate

    tstart = time.clock()
    inputDict = { "keep":keep, "control":control,
        "case":case, "nullvalues":nullvalues, "match":match}
    #loads and opens input files
    inputDict = mf.get_user_input_query_lines(inputDict)
    tloadedFiles = time.clock()

    print("Calling keep_samples")
    afterExclusionMD = mf.keep_samples(metadata,
            inputDict["keep"], extra)
    tkeep = time.clock()
    print("Time to filter out unwanted samples is %s"
          %(tkeep - tloadedFiles))

    print("Calling determine_cases_and_controls")
    case_control_dict = {"case":inputDict["case"],
            "control":inputDict["control"]}
    case_controlMD = mf.determine_cases_and_controls(
            afterExclusionMD, case_control_dict, extra)
    tcase_control = time.clock()
    print("Time to label case and control samples is %s"
          %(tcase_control - tkeep))

    print("Calling matcher")
    matchedMD = mf.matcher(prepped_for_matchMD,
                        inputDict["match"], one, only_matches)
    tmatch = time.clock()
    print("Time to match is %s"%(tmatch - tcase_control))

    vis = tabulate(matchedMD)
    vis.visualization.export_data(output_dir)
    tend = time.clock()
    print("Time to do everything %s"%(tend - tstart))





def complete_matcher(output_dir, metadata: Metadata, keep:str, 
                     control:str, case:str, nullvalues:str, 
                     match:str, one:bool=False, 
                     only_matches:bool=True, extra) -> None:
    '''
    Parameters
    ----------
    output_dir: string
        directory where visualization will be output
    metadata: Metadata
        Metadata object to analyze.
    keep: string
        name of file with sqlite lines used to determine what 
            samples to exclude or keep
    control: string
        name of file with sqlite lines used to determine what 
            samples to label control
    case: string
        name of file with sqlite lines used to determine what 
            samples to label case
    nullvalues: string
        name of file with strings that represent null values so that
            samples where one of these null values are in a category
            that is used to determine matches are filtered out
    match: string
        name of file which contains information on what conditions
            must be met to constitue a match
    one: boolean
        When given as a parameter match_samples will do one to
             one matching instead of all matches
    only_matches: boolean
        When given as a parameter match_samples will filter out
            non-matched samples from output file
    extra: boolean
        Dictates if funtions that subset metadata do the subsetting
            in one or multiple steps
    '''
    from qiime2.plugins.metadata.visualizers import tabulate

    tstart = time.clock()
    inputDict = { "keep":keep, "control":control,
        "case":case, "nullvalues":nullvalues, "match":match}
    #loads and opens input files
    inputDict = mf.get_user_input_query_lines(inputDict)
    tloadedFiles = time.clock()

    print("Calling keep_samples")
    afterExclusionMD = mf.keep_samples(metadata,
            inputDict["keep"], extra)
    tkeep = time.clock()
    print("Time to filter out unwanted samples is %s"
          %(tkeep - tloadedFiles))

    print("Calling determine_cases_and_controls")
    case_control_dict = {"case":inputDict["case"],
            "control":inputDict["control"]}
    case_controlMD = mf.determine_cases_and_controls(
            afterExclusionMD, case_control_dict, extra)
    tcase_control = time.clock()
    print("Time to label case and control samples is %s"
          %(tcase_control - tkeep))

    print("Calling filter_prep_for_matchMD")
    prepped_for_matchMD = mf.filter_prep_for_matchMD(
        case_controlMD, inputDict["match"], inputDict["nullvalues"])
    tprepped = time.clock()
    print("Time to filter Metadata information for samples "
          "with null values is %s"%(tprepped - tcase_control))

    print("Calling matcher")
    matchedMD = mf.matcher(prepped_for_matchMD,
                        inputDict["match"], one, only_matches)
    tmatch = time.clock()
    print("Time to match is %s"%(tmatch - tprepped))

    vis = tabulate(matchedMD)
    vis.visualization.export_data(output_dir)
    tend = time.clock()
    print("Time to do everything %s"%(tend - tstart))
