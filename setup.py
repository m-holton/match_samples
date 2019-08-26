# ----------------------------------------------------------------------------
# Based of the qiime2 q2-emperor setup.py file found at
# https://github.com/qiime2/q2-emperor/blob/master/setup.py
#
# ----------------------------------------------------------------------------

from setuptools import setup, find_packages

setup(
    name="sample_matcher",
    version='1',
    packages=find_packages(),
    author="Mark Holton",
    author_email="mholton@ucsd.edu",
    description="Filter, label and match samples in a metadata file",
    url="https://github.com/brainiac5mimic/sample_matcher",
    entry_points={
        'qiime2.plugins':
        ['q2-match_samples=sample_matcher.plugin_setup:plugin']
    },
    zip_safe=False,
)