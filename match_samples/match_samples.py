
from qiime2 import Metadata

import match_functions as mf


def subsetting(output_dir, metadata: Metadata, keep: str):
    '''
    Parameters
    ----------
    output_dir: string
        directory where visualization will be output
    metadata: Metadata
        Metadata object to analyze.
    keep: string
        name of file with sqlite lines used to determine what samples to
            exclude or keep
            
    Returns
    -------
    Visualization of a Metadata object that contains the subset of metadata
        samples

    '''
    from qiime2.plugins.metadata.visualizers import tabulate
    
    tstart = time.clock()
    inputDict = { "keep":keep}
    #loads and opens input files
    inputDict = mf.get_user_input_query_lines(inputDict)
    print("The file parameters found are")
    print(", ".join(inputDict.keys()))
    tloadedFiles = time.clock()
    print("Time to load input files is %s"%(tloadedFiles - tstart))
        

    print("Calling keep_samples")
    afterExclusionMD = mf.keep_samples(metadata,
            inputDict["keep"])
    tkeep = time.clock()
    print("Time to filter out unwanted samples is %s"
          %(tkeep - tloadedFiles))

    tend = time.clock()
    print("Time to do everything %s"%(tend - tstart))
    return tabulate(afterExclusionMD)






def cc_labeler_without_inital_subsetting(output_dir, metadata: Metadata, control: str, case: str):
    '''
    Parameters
    ----------
    output_dir: string
        directory where visualization will be output
    metadata: Metadata
        Metadata object to analyze.
    control: string
        name of file with sqlite lines used to determine what samples to
            label control
    case: string
        name of file with sqlite lines used to determine what samples to
            label case
            
    Returns
    -------
    Visualization of a Metadata object that contains the filtered, labeled, and or matched
        samples

    '''
    from qiime2.plugins.metadata.visualizers import tabulate
    
    tstart = time.clock()
    inputDict = {"control":control, "case":case}
    #loads and opens input files
    inputDict = mf.get_user_input_query_lines(inputDict)
    print("The file parameters found are")
    print(", ".join(inputDict.keys()))
    tloadedFiles = time.clock()
    print("Time to load input files is %s"%(tloadedFiles - tstart))
        
    print("Calling determine_cases_and_controls")
    case_control_dict = {"case":inputDict["case"],
            "control":inputDict["control"]}
    case_controlMD = mf.determine_cases_and_controls(verbose,
            metadata, case_control_dict)
    tcase_control = time.clock()
    print("Time to label case and control samples is %s"
          %(tcase_control - tloadedFiles))

    tend = time.clock()
    print("Time to do everything %s"%(tend - tstart))
    return tabulate(case_controlMD)








def complete_cc_labeler(output_dir, metadata: Metadata, keep:str, control:str, case:str):
    '''
    Parameters
    ----------
    output_dir: string
        directory where visualization will be output
    metadata: Metadata
        Metadata object to analyze.
    keep: string
        name of file with sqlite lines used to determine what samples to
            exclude or keep
    control: string
        name of file with sqlite lines used to determine what samples to
            label control
    case: string
        name of file with sqlite lines used to determine what samples to
            label case

    Returns
    -------
    Visualization of a Metadata object that contains the filtered, labeled, and or matched
        samples

    '''
    from qiime2.plugins.metadata.visualizers import tabulate
    
    tstart = time.clock()
    inputDict = {"keep":keep, "control":control, "case":case}
    #loads and opens input files
    inputDict = mf.get_user_input_query_lines(inputDict)
    print("The file parameters found are")
    print(", ".join(inputDict.keys()))
    tloadedFiles = time.clock()
    print("Time to load input files is %s"%(tloadedFiles - tstart))
        
    print("Calling keep_samples")
    afterExclusionMD = mf.keep_samples(metadata, inputDict["keep"])
    tkeep = time.clock()
    print("Time to filter out unwanted samples is %s"
          %(tkeep - tloadedFiles))
    
    print("Calling determine_cases_and_controls")
    case_control_dict = {"case":inputDict["case"],
            "control":inputDict["control"]}
    case_controlMD = mf.determine_cases_and_controls(verbose,
            afterExclusionMD, case_control_dict)
    tcase_control = time.clock()
    print("Time to label case and control samples is %s"
          %(tcase_control - tkeep))

    tend = time.clock()
    print("Time to do everything %s"%(tend - tstart))
    return tabulate(case_controlMD)







def matching_without_subsetting_and_null_filtering(output_dir, metadata: Metadata, 
                                                   control:str, case:str, match:str, 
                                                   one:bool, only_matches:bool):
    '''
    Parameters
    ----------
    output_dir: string
        directory where visualization will be output
    metadata: Metadata
        Metadata object to analyze.
    control: string
        name of file with sqlite lines used to determine what samples to
            label control
    case: string
        name of file with sqlite lines used to determine what samples to
            label case
    match: string
        name of file which contains information on what conditions
            must be met to constitue a match
    one: boolean
        When given as a parameter match_samples will do one to
             one matching instead of all matches
    only_matches: boolean
        When given as a parameter match_samples will filter out
            non-matched samples from output file

    Returns
    -------
    Visualization of a Metadata object that contains the filtered, labeled, and or matched
        samples

    '''
    from qiime2.plugins.metadata.visualizers import tabulate
    
    tstart = time.clock()
    inputDict = {"metadata":metadata, "control":control,
        "case":case, "match":match}
    #loads and opens input files
    inputDict = mf.get_user_input_query_lines(inputDict)
    print("The file parameters found are")
    print(", ".join(inputDict.keys()))
    tloadedFiles = time.clock()
    print("Time to load input files is %s"%(tloadedFiles - tstart))
        
    print("Calling determine_cases_and_controls")
    case_control_dict = {"case":inputDict["case"],
            "control":inputDict["control"]}
    case_controlMD = mf.determine_cases_and_controls(verbose,
            metadata, case_control_dict)
    tcase_control = time.clock()
    print("Time to label case and control samples is %s"
          %(tcase_control - tloadedFiles))

    print("Calling matcher")
    matchedMD = mf.matcher(case_controlMD,
                        inputDict["match"], one, only_matches)
        
    tmatch = time.clock()
    tend = time.clock()
    print("Time to match is %s"%(tmatch - tcase_control))
    print("Time to do everything %s"%(tend - tstart))
    return tabulate(matchedMD)





def matching_without_initial_subsetting(output_dir, metadata: Metadata, 
                                        control:str, case:str, nullvalues:str, 
                                        match:str, one:bool, only_matches:bool):
    '''
    Parameters
    ----------
    output_dir: string
        directory where visualization will be output
    metadata: Metadata
        Metadata object to analyze.
    control: string
        name of file with sqlite lines used to determine what samples to
            label control
    case: string
        name of file with sqlite lines used to determine what samples to
            label case
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

    Returns
    -------
    Visualization of a Metadata object that contains the filtered, labeled, and or matched
        samples

    '''
    from qiime2.plugins.metadata.visualizers import tabulate
    
    tstart = time.clock()
    inputDict = { "control":control,
        "case":case, "nullvalues":nullvalues, "match":match}
    #loads and opens input files
    inputDict = mf.get_user_input_query_lines(inputDict)
    print("The file parameters found are")
    print(", ".join(inputDict.keys()))
    tloadedFiles = time.clock()
    print("Time to load input files is %s"%(tloadedFiles - tstart))
        
    print("Calling determine_cases_and_controls")
    case_control_dict = {"case":inputDict["case"],
            "control":inputDict["control"]}
    case_controlMD = mf.determine_cases_and_controls(verbose,
            metadata, case_control_dict)
    tcase_control = time.clock()
    print("Time to label case and control samples is %s"
          %(tcase_control - tloadedFiles))

    print("Calling filter_prep_for_matchMD")
    prepped_for_matchMD = mf.filter_prep_for_matchMD(verbose,
                case_controlMD, inputDict["match"], inputDict["nullvalues"])
    tprepped = time.clock()
    print("Time to filter Metadata information for samples "
                      "with null values is %s"%(tprepped - tcase_control))
    
    print("Calling matcher")
    matchedMD = mf.matcher(prepped_for_matchMD,
                        inputDict["match"], one, only_matches)
    
    tmatch = time.clock()
    tend = time.clock()
    print("Time to match is %s"%(tmatch- tprepped))
    print("Time to do everything %s"%(tend - tstart))
    return tabulate(matchedMD)






def matching_without_null_filtering(output_dir, metadata: Metadata, keep:str,
                                    control:str, case:str, match:str, one:bool,
                                    only_matches:bool):
    '''
    Parameters
    ----------
    output_dir: string
        directory where visualization will be output
    metadata: Metadata
        Metadata object to analyze.
    keep: string
        name of file with sqlite lines used to determine what samples to
            exclude or keep
    control: string
        name of file with sqlite lines used to determine what samples to
            label control
    case: string
        name of file with sqlite lines used to determine what samples to
            label case
    match: string
        name of file which contains information on what conditions
            must be met to constitue a match
    one: boolean
        When given as a parameter match_samples will do one to
             one matching instead of all matches
    only_matches: boolean
        When given as a parameter match_samples will filter out
            non-matched samples from output file
            
    Returns
    -------
    Visualization of a Metadata object that contains the filtered, labeled, and or matched
        samples

    '''
    from qiime2.plugins.metadata.visualizers import tabulate
    
    tstart = time.clock()
    inputDict = { "keep":keep, "control":control,
        "case":case, "nullvalues":nullvalues, "match":match}
    #loads and opens input files
    inputDict = mf.get_user_input_query_lines(inputDict)
    print("The file parameters found are")
    print(", ".join(inputDict.keys()))
    tloadedFiles = time.clock()
    print("Time to load input files is %s"%(tloadedFiles - tstart))
    
    print("Calling keep_samples")
    afterExclusionMD = mf.keep_samples(metadata,
            inputDict["keep"])
    tkeep = time.clock()
    print("Time to filter out unwanted samples is %s"
          %(tkeep - tloadedFiles))

    print("Calling determine_cases_and_controls")
    case_control_dict = {"case":inputDict["case"],
            "control":inputDict["control"]}
    case_controlMD = mf.determine_cases_and_controls(verbose,
            afterExclusionMD, case_control_dict)
    tcase_control = time.clock()
    print("Time to label case and control samples is %s"
          %(tcase_control - tkeep))

    print("Calling matcher")
    matchedMD = mf.matcher(prepped_for_matchMD,
                        inputDict["match"], one, only_matches)
 
    tmatch = time.clock()
    tend = time.clock()
    print("Time to match is %s"%(tmatch- tcase_control))
    print("Time to do everything %s"%(tend - tstart))
    return tabulate(matchedMD)





def complete_Matcher(output_dir, metadata: Metadata, keep:str, control:str, case:str,
    nullvalues:str, match:str, one:bool, only_matches:bool):
    '''
    Parameters
    ----------
    output_dir: string
        directory where visualization will be output
    metadata: Metadata
        Metadata object to analyze.
    keep: string
        name of file with sqlite lines used to determine what samples to
            exclude or keep
    control: string
        name of file with sqlite lines used to determine what samples to
            label control
    case: string
        name of file with sqlite lines used to determine what samples to
            label case
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
            
    Returns
    -------
    Visualization of a Metadata object that contains the filtered, labeled, and or matched
        samples

    '''
    from qiime2.plugins.metadata.visualizers import tabulate
    
    tstart = time.clock()
    inputDict = { "keep":keep, "control":control,
        "case":case, "nullvalues":nullvalues, "match":match}
    #loads and opens input files
    inputDict = mf.get_user_input_query_lines(inputDict)
    print("The file parameters found are")
    print(", ".join(inputDict.keys()))
    tloadedFiles = time.clock()
    print("Time to load input files is %s"%(tloadedFiles - tstart))
        

    print("Calling keep_samples")
    afterExclusionMD = mf.keep_samples(metadata,
            inputDict["keep"])
    tkeep = time.clock()
    print("Time to filter out unwanted samples is %s"
          %(tkeep - tloadedFiles))
    
    print("Calling determine_cases_and_controls")
    case_control_dict = {"case":inputDict["case"],
            "control":inputDict["control"]}
    case_controlMD = mf.determine_cases_and_controls(verbose,
            afterExclusionMD, case_control_dict)
    tcase_control = time.clock()
    print("Time to label case and control samples is %s"
          %(tcase_control - tkeep))

    print("Calling filter_prep_for_matchMD")
    prepped_for_matchMD = mf.filter_prep_for_matchMD(verbose,
                case_controlMD, inputDict["match"], inputDict["nullvalues"])
    tprepped = time.clock()
    print("Time to filter Metadata information for samples "
                      "with null values is %s"%(tprepped - tcase_control))

    print("Calling matcher")
    matchedMD = mf.matcher(prepped_for_matchMD,
                        inputDict["match"], one, only_matches)
        
    tmatch = time.clock()
    tend = time.clock()
    print("Time to match is %s"%(tmatch- tprepped))
    print("Time to do everything %s"%(tend - tstart))
    return tabulate(matchedMD)







