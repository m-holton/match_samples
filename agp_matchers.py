import pandas as pd
import numpy as np


def match(focus, background, category_type, tolerance=None,
          on_failure='raise'):
    """Get matched samples for a category

    Parameters
    ----------
    focus : pd.Series
        A Series of the samples that should be matched
    background : pd.Series
        The Series metadata to match against
    category_type : {'continuous', 'discrete'}
        How to interpret the category
    tolerance : numeric, optional
        If the category is numeric, a tolerance can be provided for matching
        within a range (e.g., +/- a value)
    on_failure : str, optional
        If a match cannot be found for a sample, either 'ignore' or 'raise'

    Returns
    -------
    dict of set
        Keyed by each index value in focus, with a set of the index values in background

    Raises
    ------
    ValueError
        If focus and background are not disjoint
        If the category is discrete but the the set of values are disjoint between focus/background
    """
    if set(focus.index) & set(background.index):
        raise ValueError("Not disjoint")

    if category_type == 'discrete' and not (set(focus.unique()) & set(background.unique())):
        raise ValueError("No overlap in category values")

    if category_type == 'continuous':
        focus = pd.to_numeric(focus, errors='coerce')
        background = pd.to_numeric(background, errors='coerce')

    if category_type == 'continuous':
        if tolerance is None:
            tolerance = 1e-08  # default atol for isclose

        def matcher(fv, bvalues):
            return np.isclose(bvalues, fv, atol=tolerance)

    elif category_type == 'discrete':
        def matcher(fv, bvalues):
            return fv == bvalues

    else:
        raise ValueError("Unrecognized category type")

    matches = {}
    for f_idx, f_val in zip(focus.index, focus.values):
        hits = matcher(f_val, background.values)
        if hits.any():
            matches[f_idx] = set(background.index[hits])
        else:
            if on_failure == 'raise':
                raise ValueError("No matches for %s" % f_idx)
            else:
                matches[f_idx] = set()

    return matches


def match_multiple(focus, background, categories, category_types,
                   tolerances=None, on_failure='raise'):
    """Match over multiple categories

    Parameters
    ----------
    focus : pd.DataFrame
        Focus set of samples
    background : pd.DataFrame
        The background to select against
    categories : list of str
        The columns to match against
    category_types : list of {'continuous', 'discrete'}
        The types of the columns
    tolerances : dict of {category: tolerance}, optional
        Any tolerances per category, categories not represented are assumed to
        have no tolerance.
    on_failures : {'raise', 'ignore'}, optional
        Whether to raise or not

    Returns
    -------
    dict of set
        Keyed by the index in focus, and valued by the samples which match

    Raises
    ------
    ValueError
        If focus and background are not disjoint
        If the categories don't exist in both
        If the length of categories, category_types and tolerances are not equal
    """
    if not set(categories).issubset(set(focus.columns)):
        raise ValueError("Categories requested are missing from focus")

    if not set(categories).issubset(set(background.columns)):
        raise ValueError("Categories requested are missing from background")

    if len(categories) != len(category_types):
        raise ValueError("Categories and category types are mismatched")

    if tolerances is None:
        tolerances = {}

    # match everyone at first
    matches = {i: set(background.index) for i in focus.index}

    for c, ctype in zip(categories, category_types):
        tol = tolerances.get(c)
        observed = match(focus[c], background[c], ctype, tol, on_failure)
        for fidx, fhits in observed.items():
            # reduce the matches with successive categories
            matches[fidx] = matches[fidx] & fhits

    return matches


import unittest
import pandas.testing as pdt

class MatchTests(unittest.TestCase):
    def test_match_discrete(self):
        focus = pd.Series(['a', 'b', 'c', 'd'],
                           index=[1, 2, 3, 4])
        background = pd.Series(['d', 'a', 'a', 'x', 'c', 'y'],
                               index=[5, 6, 7, 8, 9, 10])
        exp = {1: {6, 7},
               2: set(),
               3: {9, },
               4: {5, }}
        obs = match(focus, background, 'discrete', on_failure='ignore')
        self.assertEqual(obs, exp)

    def test_match_continuous_no_tol(self):
        focus = pd.Series([-1, '2', 3, 10],
                           index=[1, 2, 3, 4])
        background = pd.Series([5., '-1', -1.5, 2, 3, 2],
                               index=[5, 6, 7, 8, 9, 10])
        exp = {1: {6, },
               2: {8, 10},
               3: {9, },
               4: set()}
        obs = match(focus, background, 'continuous', on_failure='ignore')
        self.assertEqual(obs, exp)

    def test_match_continuous_tol(self):
        focus = pd.Series([-1, '2', 3, 10],
                           index=[1, 2, 3, 4])
        background = pd.Series([5., '-1', -1.5, 2, 3, 2],
                               index=[5, 6, 7, 8, 9, 10])
        exp = {1: {6, 7},
               2: {8, 9, 10},
               3: {8, 9, 10},
               4: set()}
        obs = match(focus, background, 'continuous', tolerance=1.1,
                    on_failure='ignore')
        self.assertEqual(obs, exp)

    def test_match_raises_disjoint(self):
        focus = pd.Series(['a', 'b', 'c', 'd'],
                           index=[1, 2, 3, 4])
        background = pd.Series(['d', 'a', 'a', 'x', 'c', 'y'],
                               index=[5, 6, 4, 8, 9, 10])
        with self.assertRaisesRegex(ValueError, "Not disjoint"):
            match(focus, background, 'discrete')

    def test_match_handles_not_numeric(self):
        focus = pd.Series([1, 'b', 2, 'd'],
                           index=[1, 2, 3, 4])
        background = pd.Series([1, 'a', 'a', 2, 'c', 'y'],
                               index=[5, 6, 7, 8, 9, 10])
        exp = {1: {5, },
               2: set(),
               3: {8, },
               4: set()}
        obs = match(focus, background, 'continuous', on_failure='ignore')

    def test_match_raises_bad_category_type(self):
        focus = pd.Series(['a', 'b', 'c', 'd'],
                           index=[1, 2, 3, 4])
        background = pd.Series(['d', 'a', 'a', 'x', 'c', 'y'],
                               index=[5, 6, 7, 8, 9, 10])
        with self.assertRaisesRegex(ValueError, "Unrecognized category type"):
            match(focus, background, 'continuous foo')

    def test_match_raises_disjoint_values(self):
        focus = pd.Series(['a', 'b', 'c', 'd'],
                           index=[1, 2, 3, 4])
        background = pd.Series(['x', 'x', 'y', 'y', 'z', 'z'],
                               index=[5, 6, 7, 8, 9, 10])
        with self.assertRaisesRegex(ValueError, "No overlap"):
            match(focus, background, 'discrete')

    def test_match_raise_on_failure(self):
        focus = pd.Series(['a', 'b', 'c', 'd'],
                           index=[1, 2, 3, 4])
        background = pd.Series(['d', 'a', 'a', 'x', 'c', 'y'],
                               index=[5, 6, 7, 8, 9, 10])

        # no matches for focus index 2
        with self.assertRaisesRegex(ValueError, "No matches for 2"):
            match(focus, background, 'discrete', on_failure='raise')


class MultipleMatchTests(unittest.TestCase):
    def setUp(self):
        self.focus = pd.DataFrame([[1, 'a', 2],
                                  [1, 'b', 30],
                                  [2, 'c', 31]],
                                 columns=['A', 'B', 'C'],
                                 index=['x', 'y', 'z'])
        self.background = pd.DataFrame([[9, 'foo', 'a', 3],
                                        [1, 'baz', 'b', 29.5],
                                        [10, 'bar', 'a', 5],
                                        [1, 'foo', 'x', 35],
                                        [1, 'oof', 'x', 30.5],
                                        [2, 'baz', 'x', 29]],
                                        columns=['A', 'Z', 'B', 'C'],
                                        index=list('efghij'))

    def test_match_multiple(self):
        tests = [(['A', ], ['discrete'], None),
                 (['A', ], ['continuous'], None),
                 (['A', ], ['continuous'], {'A': 3.0}),
                 (['B', ], ['discrete'], None),
                 (['A', 'C'], ['discrete', 'continuous'], {'C': 4.999})]
        exp = [{'x': {'f', 'h', 'i'},
                'y': {'f', 'h', 'i'},
                'z': {'j', }},
               {'x': {'f', 'h', 'i'},
                'y': {'f', 'h', 'i'},
                'z': {'j', }},
               {'x': {'f', 'h', 'i', 'j'},
                'y': {'f', 'h', 'i', 'j'},
                'z': {'f', 'h', 'i', 'j'}},
               {'x': {'e', 'g'},
                'y': {'f', },
                'z': set()},
               {'x': set(),
                'y': {'f', 'i'},
                'z': {'j',},}]
        for test, ex in zip(tests, exp):
            obs = match_multiple(self.focus, self.background, *test,
                                 on_failure='ignore')
            self.assertEqual(obs, ex)

    def test_match_multiple_raise_missing_focus(self):
        focus = self.focus.copy()
        background = self.background.copy()
        focus.columns = ['A', 'B', 'Z']
        with self.assertRaisesRegex(ValueError, "Categories.*focus$"):
            match_multiple(focus, background,
                           ['A', 'B', 'C'],
                           ['discrete', 'discrete', 'discrete'],
                           on_failure='ignore')

    def test_match_multiple_raise_missing_background(self):
        focus = self.focus.copy()
        background = self.background.copy()
        background.columns = ['A', 'B', 'X', 'Z']
        with self.assertRaisesRegex(ValueError, "Categories.*background$"):
            match_multiple(focus, background,
                           ['A', 'B', 'C'],
                           ['discrete', 'discrete', 'discrete'],
                           on_failure='ignore')

    def test_match_multiple_raise_mismatch(self):
        with self.assertRaisesRegex(ValueError, "Categories.*mismatched"):
            match_multiple(self.focus, self.background,
                           ['A', 'B'],
                           ['discrete', 'discrete', 'discrete'],
                           on_failure='ignore')

        with self.assertRaisesRegex(ValueError, "Categories.*mismatched"):
            match_multiple(self.focus, self.background,
                           ['A', 'B', 'C'],
                           ['discrete', 'discrete'],
                           on_failure='ignore')


if __name__ == '__main__':
    unittest.main()
