import click

import match_samples



@click.command()
@click.option("--verbose", is_flag=True,
    help="Make print statements appear.")
@click.option("--metadata", required = True, type = str,
   help="Name of file with sample metadata to analyze.")
@click.option("--keep", default=None, type = str,
    help="Name of file with sqlite lines used to determine "
         "what samples to exclude or keep.")
@click.option("--control", default=None, type = str,
    help="Name of file with sqlite lines used to determine "
         "what samples to label control.")
@click.option("--case", default=None, type = str,
    help="Name of file with sqlite lines used to determine "
         "what samples to label case.")
@click.option("--nullvalues", default=None, type = str,
    help="Name of file with list used to determine "
         "what values are null.")
@click.option("--match", default=None, type = str,
    help="Name of file with lines used to determine "
         "what categories to match upon and how to match "
         "samples based on each category.")
@click.option("--one", is_flag=True,
    help="When given as a parameter match_samples will do one to "
         "one matching instead of all matches.")
@click.option("--only_matches", is_flag=True,
    help="When given as a parameter match_samples will filter out"
         "non-matched samples from output file.")
@click.option("--unit", is_flag=True,
    help="When given as a parameter will print out statements used"
         " for unit tests of the mainControler function. These "
         "statements indicate what the program is doing.")
@click.option("--output", default=None, type = str,
    help="Path to file where metadata should be saved to")
def standMainControler(verbose, metadata, keep, control, case,
    nullvalues, match, one, only_matches, unit, output):
    '''
    Parameters
    ----------
    verbose: boolean
        Tells function if it should output print statements or not.
            True outputs print statements.
    metadata: string
        Name of file with sample metadata to analyze.
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
    unit: boolean
        When given as a parameter will print out statements used
            for unit tests of the mainControler function. These
            statements indicate what the program is doing.
    '''
    metadata = match_samples.mainControler(verbose, metadata, keep, control, 
        case, nullvalues, match, one, only_matches, unit)
    
    if output != None:
        metadata.save(output)

        
        
        
if __name__ == "__main__":
    standMainControler()
    
    
    
    