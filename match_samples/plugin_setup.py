# ----------------------------------------------------------------------------
# Based of the qiime2 q2-emperor plugin_setup.py file found at
# https://github.com/qiime2/q2-emperor/blob/master/q2_emperor/plugin_setup.py
#
# ----------------------------------------------------------------------------

from match_samples import match_samples


from qiime2.plugin import (Plugin, Metadata, Str, List, Citations, Range, Int,
                           Bool, Properties)
from q2_types.ordination import PCoAResults


plugin = Plugin(
    name='match-samples',
    version='1',
    package='match_samples',
    website='https://github.com/brainiac5mimic/match_samples',    
    description=('match_samples allows users to filter down a metadata file, '
                 'label samples case or control, and match case to control samples.'),
    short_description='Filter, label and match samples in a metadata file'
)

function=match_samples.mainControler
name='mainControler'
description='mainControler takes the inputs in, determines what needs to be run, and outputs a visialization of the processed metadata '
parameters={
    'verbose': Bool,  
    'keep': Str, 
    'control': Str, 'case': Str,
    'nullvalues': Str, 'match': Str, 'one': Bool, 
    'only_matches': Bool, 'unit': Bool, 'metadata': Metadata, 'stand': Bool
    
}
inputs={}
input_descriptions={}
parameter_descriptions={
    'metadata': 'Sample metadata to analyze.',
    'verbose': ('Tells function if it should output print statements or not.'
        'True outputs print statements.'), 
    'keep': ('Path of file with sqlite lines used to determine '
        'what samples to exclude or keep.'), 
    'control': ('Path of file with sqlite lines used to determine '
        'what samples to label control.'), 
    'case': ('Path of file with sqlite lines used to determine '
        'what samples to label case.'),
    'nullvalues': ('Path of file with list used to determine '
        'what values are null.'), 
    'match': ('Path of file with lines used to determine '
        'what categories to match upon and how to match '
        'samples based on each category.'), 
    'one': ('When True match_samples will do one to '
        'one matching instead of all matches.'), 
    'only_matches': ('When True match_samples will filter out'
        'non-matched samples from output file.'), 
    'unit': ('When True program will print out statements used '
        'for unit tests of the mainControler function. These '
        'statements indicate what the program is doing.'),
    'stand':'test'
}



plugin.visualizers.register_function(
    function=function,
    inputs=inputs,
    parameters=parameters,
    input_descriptions=input_descriptions,
    parameter_descriptions=parameter_descriptions,
    name=name,
    description=description
)

