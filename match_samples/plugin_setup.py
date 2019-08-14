# ----------------------------------------------------------------------------
# Based of the qiime2 q2-emperor plugin_setup.py file found at
# https://github.com/qiime2/q2-emperor/blob/master/q2_emperor/plugin_setup.py
#
# ----------------------------------------------------------------------------

import match_samples

from qiime2.plugin import (Plugin, Metadata, Str, List, Citations, Range, Int,
                           Bool, Properties)
from q2_types.ordination import PCoAResults



PARAMETERS = {'verbose': Bool, 'inputdata': Str, 'keep': Str, 
              'control': Str, 'case': Str,
              'nullvalues': Str, 'match': Str, 'one': Bool, 
              'only_matches': Bool, 'unit': Bool}

PARAMETERS_DESC = {
    'verbose': ('Tells function if it should output print statements or not.'
            'True outputs print statements.'), 
        'inputdata': ('Name of file with sample metadata to analyze.'), 
        'keep': ('Name of file with sqlite lines used to determine '
            'what samples to exclude or keep.'), 
        'control': ('Name of file with sqlite lines used to determine '
            'what samples to label control.'), 
        'case': ('Name of file with sqlite lines used to determine '
            'what samples to label case.'),
        'nullvalues': ('Name of file with list used to determine '
            'what values are null.'), 
        'match': ('Name of file with lines used to determine '
            'what categories to match upon and how to match '
            'samples based on each category.'), 
        'one': ('When given as a parameter match_samples will do one to '
            'one matching instead of all matches.'), 
        'only_matches': ('When given as a parameter match_samples will filter out'
            'non-matched samples from output file.'), 
        'unit': ('When given as a parameter will print out statements used '
            'for unit tests of the mainControler function. These '
            'statements indicate what the program is doing.')
}



plugin = Plugin(
    name='match_samples',
    version='1',
    package='match_samples',
    website='https://github.com/brainiac5mimic/match_samples',    
    description=('match_samples allows users to filter down a metadata file, '
                 'label samples case or control, and match case to control samples.'),
    short_description='Filter, label and match samples in a metadata file'
)


name='match_samples'
description='foobar'
function=match_samples.mainControler
parameters={
    'verbose': Bool,  
    'keep': Str, 
    'control': Str, 'case': Str,
    'nullvalues': Str, 'match': Str, 'one': Bool, 
    'only_matches': Bool, 'unit': Bool
}
inputs={'metadata': Metadata}
outputs=[('outputMD', Metadata)]
input_descriptions={'metadata': ('Name of file with sample metadata to analyze.')}
parameter_descriptions={
    'verbose': ('Tells function if it should output print statements or not.'
        'True outputs print statements.'), 
    'keep': ('Name of file with sqlite lines used to determine '
        'what samples to exclude or keep.'), 
    'control': ('Name of file with sqlite lines used to determine '
        'what samples to label control.'), 
    'case': ('Name of file with sqlite lines used to determine '
        'what samples to label case.'),
    'nullvalues': ('Name of file with list used to determine '
        'what values are null.'), 
    'match': ('Name of file with lines used to determine '
        'what categories to match upon and how to match '
        'samples based on each category.'), 
    'one': ('When given as a parameter match_samples will do one to '
        'one matching instead of all matches.'), 
    'only_matches': ('When given as a parameter match_samples will filter out'
        'non-matched samples from output file.'), 
    'unit': ('When given as a parameter will print out statements used '
        'for unit tests of the mainControler function. These '
        'statements indicate what the program is doing.')
}
output_descriptions={'outputMD': ('Metadata object that contains the filtered, labeled, and or matched samples')}

'''    
plugin.methods.register_function(
    name=name,
    description=description,
    function=function,
    inputs=inputs,
    input_descriptions=input_descriptions,
    parameters=parameters,
    parameter_descriptions=parameter_descriptions,
    outputs=outputs,
    output_descriptions=output_descriptions
)
'''

plugin.methods.register_function(
    name=name,
    description=description,
    function=function,
    inputs=inputs,
    outputs=outputs,
    parameters=parameters
)

