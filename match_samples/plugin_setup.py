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


plugin.visualizers.register_function(
    function=match_samples.subsetting,
    inputs={},
    parameters={ 
        'metadata': Metadata, 
        'keep': Str, 
    },
    input_descriptions={},
    parameter_descriptions={
        'metadata': 'Sample metadata to analyze.',
        'keep': ('Path of file with sqlite lines used to determine '
            'what samples to exclude or keep.'), 
    },
    name='Visualize and Interact with Metadata object',
    description='Subset a metadata object then returns a visualization of the augmented metadata'
)


plugin.visualizers.register_function(
    function=match_samples.labeler_no_subset,
    inputs={},
    parameters={ 
        'metadata': Metadata, 
        'control': Str, 'case': Str,

    },
    input_descriptions={},
    parameter_descriptions={
        'metadata': 'Sample metadata to analyze.',
        'control': ('Path of file with sqlite lines used to determine '
            'what samples to label control.'), 
        'case': ('Path of file with sqlite lines used to determine '
            'what samples to label case.'),
    },
    name='Visualize and Interact with Metadata object',
    description='Label samples in a metadata object then returns a visualization of the augmented metadata'
)



plugin.visualizers.register_function(
    function=match_samples.complete_labeler,
    inputs={},
    parameters={ 
        'metadata': Metadata, 
        'keep': Str, 
        'control': Str, 'case': Str,
    },
    input_descriptions={},
    parameter_descriptions={
        'metadata': 'Sample metadata to analyze.',
        'keep': ('Path of file with sqlite lines used to determine '
            'what samples to exclude or keep.'), 
        'control': ('Path of file with sqlite lines used to determine '
            'what samples to label control.'), 
        'case': ('Path of file with sqlite lines used to determine '
            'what samples to label case.'),

    },
    name='Visualize and Interact with Metadata object',
    description='Subset and label samples in a metadata object then returns a visualization of the augmented metadata'
)



plugin.visualizers.register_function(
    function=match_samples.match_no_subset_null_filter,
    inputs={},
    parameters={ 
        'metadata': Metadata, 
        'control': Str, 'case': Str,
        'match': Str, 'one': Bool, 'only_matches': Bool
    },
    input_descriptions={},
    parameter_descriptions={
        'metadata': 'Sample metadata to analyze.',
        'control': ('Path of file with sqlite lines used to determine '
            'what samples to label control.'), 
        'case': ('Path of file with sqlite lines used to determine '
            'what samples to label case.'),
        'match': ('Path of file with lines used to determine '
            'what categories to match upon and how to match '
            'samples based on each category.'), 
        'one': ('When True match_samples will do one to '
            'one matching instead of all matches.'), 
        'only_matches': ('When True match_samples will filter out'
            'non-matched samples from output file.')
    },
    name='Visualize and Interact with Metadata object',
    description='Label and match samples in a metadata object then returns a visualization of the augmented metadata'
)




plugin.visualizers.register_function(
    function=match_samples.matching_no_subset,
    inputs={},
    parameters={ 
        'metadata': Metadata, 
        'control': Str, 'case': Str,
        'nullvalues': Str, 
        'match': Str, 'one': Bool, 'only_matches': Bool
    },
    input_descriptions={},
    parameter_descriptions={
        'metadata': 'Sample metadata to analyze.',
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
            'non-matched samples from output file.')
    },
    name='Visualize and Interact with Metadata object',
    description='Label, filter, and match samples in a metadata object then returns a visualization of the augmented metadata'
)



plugin.visualizers.register_function(
    function=match_samples.matching_no_null_filter,
    inputs={},
    parameters={ 
        'metadata': Metadata, 
        'keep': Str, 
        'control': Str, 'case': Str,
        'match': Str, 'one': Bool, 'only_matches': Bool
    },
    input_descriptions={},
    parameter_descriptions={
        'metadata': 'Sample metadata to analyze.',
        'keep': ('Path of file with sqlite lines used to determine '
            'what samples to exclude or keep.'), 
        'control': ('Path of file with sqlite lines used to determine '
            'what samples to label control.'), 
        'case': ('Path of file with sqlite lines used to determine '
            'what samples to label case.'),
        'match': ('Path of file with lines used to determine '
            'what categories to match upon and how to match '
            'samples based on each category.'), 
        'one': ('When True match_samples will do one to '
            'one matching instead of all matches.'), 
        'only_matches': ('When True match_samples will filter out'
            'non-matched samples from output file.')
    },
    name='Visualize and Interact with Metadata object',
    description='Subset, label, and match samples in a metadata object then returns a visualization of the augmented metadata'
)



plugin.visualizers.register_function(
    function=match_samples.complete_Matcher,
    inputs={},
    parameters={ 
        'metadata': Metadata, 
        'keep': Str, 
        'control': Str, 'case': Str,
        'nullvalues': Str, 
        'match': Str, 'one': Bool, 'only_matches': Bool
    },
    input_descriptions={},
    parameter_descriptions={
        'metadata': 'Sample metadata to analyze.',
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
            'non-matched samples from output file.')
    },
    name='Visualize and Interact with Metadata object',
    description='Subset, label, filter, and match samples in a metadata object then returns a visualization of the augmented metadata'
)

