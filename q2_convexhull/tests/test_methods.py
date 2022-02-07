from unittest import TestCase
import pandas as pd
import numpy as np
from skbio import OrdinationResults
from q2_convexhull.convexhull import convex_hull
from pandas.util.testing import assert_frame_equal

# Where do I load the data from?

# https://github.com/qiime2/q2-emperor/blob/fdd1a8b56f93f161d0ca24630fcaec798a6ecf1c/q2_emperor/tests/test_plot.py


class TestConvexHull(TestCase):

    def setUp(self):
        self.unique_id = 'unique_id'
        self.metadata = pd.DataFrame(
            {'random_values': [1, 1, 1, 1, 2, 2, 2, 2],
             self.unique_id: ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'b']},
            index=['i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8'])

        samples = np.array([[1, 1], [1, 0], [0, 0], [0, 1],
                            [4, 4], [4, 3], [3, 3], [3, 4]])
        samples_df = pd.DataFrame(
            samples,
            index=['i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8'],
            columns=['PC1', 'PC2'])

        proportion_explained = pd.Series(
            [15.5, 12.2],
            index=['PC1', 'PC2'])

        values = pd.Series(
            np.array([0.8, 0.2]),
            index=['PC1', 'PC2'])

        self.pcoa = OrdinationResults(
            'PCoA',
            'Principal Coordinate Analysis',
            values,
            samples_df,
            proportion_explained=proportion_explained)

    def test_squares(self):

        hulls = convex_hull(self.metadata, self.pcoa, 'unique_id')
        expected = pd.DataFrame(
            {self.unique_id: ['a', 'b'],
             'convexhull_volume': [1.0, 1.0],
             'convexhull_area': [4.0, 4.0]})

        assert_frame_equal(hulls, expected)

    # def test_warnings(self):
    #   rows = [0, 4, 5, 6, 7]
    #   meta = self.metadata.loc[rows]
