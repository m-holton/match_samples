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
    version=match_samples.__version__,
    package='match_samples',
    website='https://github.com/brainiac5mimic/match_samples',    
    description=('match_samples allows users to filter down a metadata file, '
                 'label samples case or control, and match case to control samples.'),
    short_description='Filter, label and match samples in a metadata file'
)


plugin.methods.register_function(
    function=mainControler,
    parameters={
        'verbose': Bool, 'inputdata': Str, 'keep': Str, 
        'control': Str, 'case': Str,
        'nullvalues': Str, 'match': Str, 'one': Bool, 
        'only_matches': Bool, 'unit': Bool,
    },
    outputs=[
        ('*MD', Metadata)
    ],
    parameter_descriptions={
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
            'statements indicate what the program is doing.'),
    },
    output_descriptions={
        '*MD': ('Metadata object that contains the filtered, labeled, '
                'and or matched samples')

    },
    name='match_samples',
    description=('match_samples allows users to filter down a metadata file, '
                 'label samples case or control, and match case to control '
                 'samples.')
)





