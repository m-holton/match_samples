# ----------------------------------------------------------------------------
#
# by Mark Holton
#
# ----------------------------------------------------------------------------

import sys
import pandas as pd
import numpy as np

import math
import itertools
import time
import operator

from nose.tools import assert_almost_equal, assert_raises, assert_equals
from pandas.util.testing import assert_frame_equal

import analyser


test_indexs = ['a1','b2','c3','d4']
test_data1 = pd.DataFrame(data = {'sample_1': [1,2,3,4], 'sample_2': [1,2,3,0], 'sample_3': [1,1,2,3]} )


dfcolumns = ['K-OTU mers', 'Number of OTUs', 'Kmer Growth']
for sample in test_data1.columns:
    dfcolumns.append('Intersection'+' '+sample)
    dfcolumns.append('Union'+' '+sample)
    dfcolumns.append('Intersection over Union'+' '+sample)
for val in range(0,332):
    dfcolumns.append(val)



sample_kmer_list = []
sample_kmer_dict = {}
tie_length_list = []




def test_analyser_getKmers():
    outdataframe1 = pd.DataFrame(index = test_data1.columns.values, columns = dfcolumns)
    outdataframe2 = pd.DataFrame(index = test_data1.columns.values, columns = dfcolumns)
    assert_equals(analyser.getKmers(test_data1, 3, sample_kmer_list, outdataframe1, operator.le, 1), 11)
    assert_equals(analyser.getKmers(test_data1, 3, sample_kmer_list, outdataframe2, operator.lt, 1), 7)


def test_analyser_getKmersDict():
    outdataframe1 = pd.DataFrame(index = test_data1.columns.values, columns = dfcolumns)
    outdataframe2 = pd.DataFrame(index = test_data1.columns.values, columns = dfcolumns)
    assert_equals(analyser.getKmersDict(test_data1, 0, 3, sample_kmer_dict, outdataframe1, operator.le, 1), 11)
    assert_equals(analyser.getKmersDict(test_data1, 0, 3, sample_kmer_dict, outdataframe2, operator.lt, 1), 7)


def test_analyser_tie_counter():
    outdataframe1 = pd.DataFrame(index = test_data1.columns.values, columns = dfcolumns)
    assert_equals(analyser.tie_counter(test_data1, tie_length_list, outdataframe1, 1), 2)





def test_analyser_getDatabase():
    #set up answer dataset for with ties
    dfcolumns = ['K-OTU mers', 'Number of OTUs', 'Kmer Growth']
    for sample in test_data1.columns:
        dfcolumns.append('Intersection'+' '+sample)
        dfcolumns.append('Union'+' '+sample)
        dfcolumns.append('Intersection over Union'+' '+sample)
    for val in range(0,332):
        dfcolumns.append(val)
    outdataframe_answer_ties = pd.DataFrame(index = test_data1.columns.values, columns = dfcolumns)
    outdataframe_answer_noties = pd.DataFrame(index = test_data1.columns.values, columns = dfcolumns)

    outdataframe_answer_ties.iloc[0, 0] = 4
    outdataframe_answer_ties.iloc[0, 1] = 4
    outdataframe_answer_ties.iloc[0, 2] = 4
    outdataframe_answer_ties.iloc[1, 0] = 1
    outdataframe_answer_ties.iloc[1, 1] = 3
    outdataframe_answer_ties.iloc[1, 2] = 4
    outdataframe_answer_ties.iloc[2, 0] = 6
    outdataframe_answer_ties.iloc[2, 1] = 4
    outdataframe_answer_ties.iloc[2, 2] = 6

    outdataframe_answer_ties.iloc[0, 6] = 1
    outdataframe_answer_ties.iloc[0, 7] = 4
    outdataframe_answer_ties.iloc[0, 8] = 0.25
    outdataframe_answer_ties.iloc[0, 9] = 4
    outdataframe_answer_ties.iloc[0, 10] = 6
    outdataframe_answer_ties.iloc[0, 11] = 0.666666667

    outdataframe_answer_ties.iloc[1, 9] = 1
    outdataframe_answer_ties.iloc[1, 10] = 6
    outdataframe_answer_ties.iloc[1, 11] = 0.166666667

    outdataframe_answer_ties.iloc[2, 13] = 2



    outdataframe_answer_noties.iloc[0, 0] = 4
    outdataframe_answer_noties.iloc[0, 1] = 4
    outdataframe_answer_noties.iloc[0, 2] = 4

    outdataframe_answer_noties.iloc[1, 0] = 1
    outdataframe_answer_noties.iloc[1, 1] = 3
    outdataframe_answer_noties.iloc[1, 2] = 4

    outdataframe_answer_noties.iloc[2, 0] = 2
    outdataframe_answer_noties.iloc[2, 1] = 4
    outdataframe_answer_noties.iloc[2, 2] = 4

    outdataframe_answer_noties.iloc[0, 6] = 1
    outdataframe_answer_noties.iloc[0, 7] = 4
    outdataframe_answer_noties.iloc[0, 8] = 0.25

    outdataframe_answer_noties.iloc[0, 9] = 2
    outdataframe_answer_noties.iloc[0, 10] = 4
    outdataframe_answer_noties.iloc[0, 11] = 0.5

    outdataframe_answer_noties.iloc[1, 9] = 0
    outdataframe_answer_noties.iloc[1, 10] = 3
    outdataframe_answer_noties.iloc[1, 11] = 0

    outdataframe_answer_noties.iloc[2, 13] = 2

    assert_frame_equal(analyser.run_code_getDatabase(test_data1, 'output_unitTest_withTies', operator.le, 1), outdataframe_answer_ties)
    assert_frame_equal(analyser.run_code_getDatabase(test_data1, 'output_unitTest_noTies', operator.lt, 1), outdataframe_answer_noties)
    

#def test_analyser_getKmers():
    #assert_almost_equal()


if __name__ == '__main__':
    import nose
    print('started test')
    nose.runmodule()
