import click




def get_user_input_query_lines(user_input_file_of_queries,input_catagory):
    '''
    converts user_input_file_of_queries file into a list of strings that represent the lines of the file

    Parameters
    ----------
    user_input_file_of_queries : string
        file that contains lines of stings

    Returns
    -------
     if user_input_file_of_queries is not ''
        list of strings that are the lines of the file
     if user_input_file_of_queries is ''
         returns False boolean
    '''
    if user_input_file_of_queries == '':
        if verbose:
            print('null query entered for %s'%(input_catagory))
        return False
    try:
        lines = open('./%s'%(user_input_file_of_queries),'r').readlines()
    except:
        if verbose:
            print('No samples fulfill keep queries. Exited while filtering out unwanted samples')
        return False
    return lines


def keep_samples(original_MD, keep_query_lines):
    '''
    Filters out unwanted rows based on values in chosen columns.

    Parameters
    ----------
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
    shrunk_MD = original_MD
    try:
        shrunk_MD = shrunk_MD.filter_ids(shrunk_MD.get_ids(' AND '.join(keep_query_lines)))
    except:
        print('No samples fulfill keep queries. Exited while filtering out unwanted samples')
        return
    return shrunk_MD




def ExcludeOnly(verbose,inputData,keep,output):
    tstart = time.clock()
    #read metadata file into metadata object
    try:
        originalMD = Metadata.load(inputData)
    except:
        if verbose:
            print('metadata file could not load. If you entered a valid path then try clearing the formating. The file must be a TSV metadata file.')
            print("metadata file path entered is %s"%(inputData))
        return
    #each line is a sqlite query to determine what samples to keep
    keep_query_lines_input = get_user_input_query_lines(keep,"keep")
    tloadedFiles = time.clock()
    if verbose:
        print('time to load input files is %s'%(tloadedFiles - tstart))


    afterExclusionMD = keep_samples(originalMD, keep_query_lines_input)
    afterExclusionMD.to_dataframe().to_csv(output, sep = '\t')

    tkeep = time.clock()
    tend = time.clock()

    if verbose:
        print('time to filter out unwanted samples is %s'%(tkeep - tloadedFiles))
        print('time to do everything %s'%(tend-tstart))



        
        
        
@click.command()
@click.option('--verbose', default=False, type=bool, help='Make print statements appear')
@click.option('--keep', type=str, help='name of file with sqlite lines used to determine what samples to exclude or keep')
@click.option('--control', type=str, help='name of file with sqlite lines used to determine what samples to exclude or keep')
@click.option('--case', type=str, help='Number of greetings.')
@click.option('--nullValues', type=str, help='name of file with sqlite lines used to determine what samples to exclude or keep')
@click.option('--match', type=str, help='name of file with sqlite lines used to determine what samples to exclude or keep')
@click.option('--inputData',  type=str,required = True, help='Name of file with sample metadata to analyze.')
@click.option('--output',  type=str,required = True, help='Name of file to export data to.')      
def master(verbose,inputData,keep,control,case,nullValues,match,output):
    tstart = time.clock()
    #read metadata file into metadata object
    try:
        originalMD = Metadata.load(inputData)
    except:
        if verbose:
            print('metadata file could not load. If you entered a valid path then try clearing the formating. The file must be a TSV metadata file.')
            print("metadata file path entered is %s"%(inputData))
        return

    #each line is a sqlite query to determine what samples to keep
    keep_query_lines_input = get_user_input_query_lines(keep,"keep")
    #each line is a sqlite query to determine what samples to label control
    control_query_lines_input = get_user_input_query_lines(control,"control")
    #each line is a sqlite query to determine what samples to label case
    case_query_lines_input = get_user_input_query_lines(case,"case")
    null_values_lines_input = get_user_input_query_lines(nullValues,"nullValues")
    match_condition_lines_input = get_user_input_query_lines(match,"match")
    tloadedFiles = time.clock()
    if verbose:
        print('time to load input files is %s'%(tloadedFiles - tstart))
    
    #
    
            
          
            
            
            
            
            
            
            
            
            
            
            
            
