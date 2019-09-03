# ----------------------------------------------------------------------------
# 
#
# ----------------------------------------------------------------------------

from match_samples import match_samples
from qiime2.plugin import (Plugin, Metadata, Str, List, Citations, Range, Int,
                           Bool, Properties)
from q2_types.ordination import PCoAResults
from q2_types.feature_table import FeatureTable, Frequency, RelativeFrequency

plugin = Plugin(
    name='match-samples',
    version='1',
    package='match_samples',
    website='https://github.com/brainiac5mimic/match_samples',    
    description=('match_samples allows users to filter down a '
                 'metadata file, label samples case or control, and '
                 'match case to control samples.'),
    short_description=('Filter, label and match samples in a '
                      'metadata file')
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
    name='Interact with and save Metadata object',
    description=('Subset a metadata object '
                 'then saves a visualization '
                 'of the augmented metadata to a file')
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
    name='Interact with and visualizes a Metadata object',
    description=('Label samples in a metadata object '
                 'then saves a visualization '
                 'of the augmented metadata to a file')
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
    name='Interact with and visualizes a  Metadata object',
    description=('Subset and label samples in a '
                 'metadata object then saves a visualization '
                 'of the augmented metadata to a file')
)


plugin.visualizers.register_function(
    function=match_samples.matching_no_subset_null_filter,
    inputs={},
    parameters={ 
        'metadata': Metadata, 
        'control': Str, 'case': Str,
        'match': Str, 
        'one': Bool, 'only_matches': Bool
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
    name='Interact with and visualizes a Metadata object',
    description=('Label and match samples in a '
                 'metadata object then saves a visualization '
                 'of the augmented metadata to a file')
)



plugin.visualizers.register_function(
    function=match_samples.matching_no_subset,
    inputs={},
    parameters={ 
        'metadata': Metadata, 
        'control': Str, 'case': Str,
        'nullvalues': Str, 
        'match': Str, 
        'one': Bool, 'only_matches': Bool
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
    name='Interact with and visualizes a  Metadata object',
    description=('Label, filter, and match samples in a '
                 'metadata object then saves a visualization '
                 'of the augmented metadata to a file')
)


plugin.visualizers.register_function(
    function=match_samples.matching_no_null_filter,
    inputs={},
    parameters={ 
        'metadata': Metadata, 
        'keep': Str, 
        'control': Str, 'case': Str,
        'match': Str, 
        'one': Bool, 'only_matches': Bool    
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
    name='Interact with and visualizes a Metadata object',
    description=('Subset, label, and match samples in a '
                 'metadata object then saves a visualization '
                 'of the augmented metadata to a file')
)



plugin.visualizers.register_function(
    function=match_samples.complete_matcher,
    inputs={},
    parameters={ 
        'metadata': Metadata, 
        'keep': Str, 
        'control': Str, 'case': Str,
        'nullvalues': Str, 
        'match': Str, 
        'one': Bool, 'only_matches': Bool
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
    name='Interact with and visualizes a Metadata object',
    description=('Subset, label, filter, and match samples in a '
                 'metadata object then saves a visualization '
                 'of the augmented metadata to a file')
)
