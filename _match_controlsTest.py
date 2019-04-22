# ----------------------------------------------------------------------------
#
# by Mark Holton
#
# ----------------------------------------------------------------------------

import getopt, sys
import pandas as pd
import numpy as np
import qiime2
import time
import unittest
import click

from qiime2 import Metadata
from collections import defaultdict


import math
import itertools
import time
import operator

from nose.tools import assert_almost_equal, assert_raises, assert_equals
from pandas.util.testing import assert_frame_equal

import match_controls



class ExampleTest(unittest.TestCase):

    def test_get_user_input_query_lines(self):
        with self.assertRaises('metadata file could not load. The file must be a TSV metadata file.'): match_controls.get_user_input_query_lines("")
        with self.assertRaises('metadata file could not load. The file must be a TSV metadata file.'): match_controls.get_user_input_query_lines("")
            
        






@click.command()
@click.option('--verbose', is_flag=True, help='Make print statements appear')
@click.option('--keep', default=1, type = str, help='name of file with sqlite lines used to determine what samples to exclude or keep')
@click.option('--control', default=1, type = str, help='name of file with sqlite lines used to determine what samples to label control')
@click.option('--case', default=1, type = str, help='name of file with sqlite lines used to determine what samples to label case')
@click.option('--nullvalues', default=1, type = str, help='name of file with sqlite lines used to determine what samples to exclude or keep')
@click.option('--match', default=1, type = str, help='name of file with sqlite lines used to determine what samples to exclude or keep')
@click.option('--inputdata', required = True, type = str, help='Name of file with sample metadata to analyze.')
@click.option('--output', required = True, type = str, help='Name of file to export data to.')
def mainControler(verbose,inputdata,keep,control,case,nullvalues,match,output):
    
    
    return
    if isinstance(keep, str):
        if isinstance(control, str) and isinstance(case, str):
                if isinstance(match, str):
                    if isinstance(nullvalues, str):
                        if verbose:
                            print("Testing Everything")
                            Everything(verbose,inputdata,keep,control,case,nullvalues,match,output)
                    else:
                        if verbose:
                            print("Testing ExcludeControlCaseAndMatch")
                        ExcludeControlCaseAndMatch(verbose,inputdata,keep,control,case,match,output)
                else:
                    if verbose:
                            print("Testing KeepAndControlCase")
                    KeepAndControlCase(verbose,inputdata,keep,control,case,output)
        else:
            if verbose:
                print("Testing KeepOnly")
            KeepOnly(verbose,inputdata,keep,output)
    elif isinstance(control, str) and isinstance(case, str):
        if isinstance(match, str):
            if isinstance(nullvalues, str):
                if verbose:
                    print("Testing ControlCaseNullAndMatch")
                ControlCaseNullAndMatch(verbose,inputdata,control,case,nullvalues,match,output)
            else:
                if verbose:
                    print("Testing ControlCaseAndMatch")
                ControlCaseAndMatch(verbose,inputdata,control,case,match,output)
        else:
            if verbose:
                print("Testing ControlAndCaseOnly")
            ControlAndCaseOnly(verbose,inputdata,control,case,output)
    
    
    
if __name__ == '__main__':
    
    unittest.main()

