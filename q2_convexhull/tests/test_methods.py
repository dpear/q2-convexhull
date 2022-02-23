from unittest import TestCase
import pandas as pd
import numpy as np
from skbio import OrdinationResults
from q2_convexhull.convexhull import convex_hull
from q2_convexhull.convexhull import validate
from pandas.testing import assert_frame_equal
from qiime2 import Metadata


class TestConvexHull(TestCase):

    def setUp(self):
        self.individual_id_column = 'unique_id'
        self.number_of_dimensions = 3

        index = pd.Index(
                    ['i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8',
                     'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8'],
                    name='sampleid')

        samples_df = pd.DataFrame(
            {'PC1': [0, 0, 0, 0, 1, 1, 1, 1,
                     3, 3, 3, 3, 4, 4, 4, 4],
             'PC2': [0, 0, 1, 1, 0, 0, 1, 1,
                     3, 3, 4, 4, 3, 3, 4, 4],
             'PC3': [0, 1, 0, 1, 0, 1, 0, 1,
                     3, 4, 3, 4, 3, 4, 3, 4]},
            index=index)

        proportion_explained = pd.Series(
            [15.5, 12.2, 8.7],
            index=['PC1', 'PC2', 'PC3'])

        values = pd.Series(
            np.array([0.7, 0.2, 0.1]),
            index=['PC1', 'PC2', 'PC3'])

        self.pcoa = OrdinationResults(
            'PCoA',
            'Principal Coordinate Analysis',
            values,
            samples_df,
            proportion_explained=proportion_explained)

        metadata = pd.DataFrame(
            {self.individual_id_column:
                ['s1', 's1', 's1', 's1', 's1', 's1', 's1', 's1',
                 's2', 's2', 's2', 's2', 's2', 's2', 's2', 's2']},
            index=index)

        self.metadata = Metadata(metadata)

    def test_squares(self):

        hulls = convex_hull(self.metadata,
                            self.pcoa,
                            self.individual_id_column,
                            self.number_of_dimensions)
        expected = pd.DataFrame(
            {self.individual_id_column: ['s1', 's2'],
             'convexhull_volume': [1.0, 1.0],
             'convexhull_area': [6.0, 6.0]})

        assert_frame_equal(hulls, expected)

    def test_ndim_warning(self):

        number_of_dimensions = 4
        # with self.assertRaisesRegex(
        #     Warning,
        #     f'Number of dimensions {number_of_dimensions} '
        #     f'not supported. Setting to default (3).'):
        # with self.assertWarns(Warning):
        with self.assertWarnsRegex(
                Warning,
                'Setting number_of_dimensions to 3.'):

            convex_hull(
                self.metadata,
                self.pcoa,
                self.individual_id_column,
                number_of_dimensions)

    def test_len_pcoa_samples_columns(self):

        index = pd.Index(
                    ['i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8',
                     'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8'],
                    name='sampleid')

        samples_df = pd.DataFrame(
            {'PC1': [0, 0, 0, 0, 1, 1, 1, 1,
                     3, 3, 3, 3, 4, 4, 4, 4],
             'PC2': [0, 0, 1, 1, 0, 0, 1, 1,
                     3, 3, 4, 4, 3, 3, 4, 4],
             'PC3': [0, 1, 0, 1, 0, 1, 0, 1,
                     3, 4, 3, 4, 3, 4, 3, 4],
             'PC4': [5, 6, 7, 8, 5, 6, 7, 8,
                     8, 7, 6, 5, 8, 7, 6, 5]},
            index=index)

        proportion_explained = pd.Series(
            [15.5, 12.2, 8.7, 5.4],
            index=['PC1', 'PC2', 'PC3', 'PC4'])

        values = pd.Series(
            np.array([0.65, 0.15, 0.15, .5]),
            index=['PC1', 'PC2', 'PC3', 'PC4'])

        pcoa = OrdinationResults(
            'PCoA',
            'Principal Coordinate Analysis',
            values,
            samples_df,
            proportion_explained=proportion_explained)

        with self.assertWarnsRegex(
                Warning,
                "PCoA result has 4 dimensions. Truncating to 3 PC's"):

            convex_hull(
                self.metadata,
                pcoa,
                self.individual_id_column,
                self.number_of_dimensions)

    def test_pcoa_samples_not_in_metadata(self):
        # WORKS

        index = pd.Index(
                    ['i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8',
                     'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x99999'],
                    name='sampleid')

        samples_df = pd.DataFrame(
            {'PC1': [0, 0, 0, 0, 1, 1, 1, 1,
                     3, 3, 3, 3, 4, 4, 4, 4],
             'PC2': [0, 0, 1, 1, 0, 0, 1, 1,
                     3, 3, 4, 4, 3, 3, 4, 4],
             'PC3': [0, 1, 0, 1, 0, 1, 0, 1,
                     3, 4, 3, 4, 3, 4, 3, 4],
             'PC4': [5, 6, 7, 8, 5, 6, 7, 8,
                     8, 7, 6, 5, 8, 7, 6, 5]},
            index=index)

        proportion_explained = pd.Series(
            [15.5, 12.2, 8.7, 5.4],
            index=['PC1', 'PC2', 'PC3', 'PC4'])

        values = pd.Series(
            np.array([0.65, 0.15, 0.15, .5]),
            index=['PC1', 'PC2', 'PC3', 'PC4'])

        pcoa = OrdinationResults(
            'PCoA',
            'Principal Coordinate Analysis',
            values,
            samples_df,
            proportion_explained=proportion_explained)

        with self.assertRaisesRegex(
                KeyError,
                'PCoA result indeces do not match metadata.'):

            convex_hull(
                self.metadata,
                pcoa,
                self.individual_id_column,
                self.number_of_dimensions)

    def test_individual_id_column_not_in_metadata(self):

        index = pd.Index(
                    ['i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8',
                     'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8'],
                    name='sampleid')

        metadata = pd.DataFrame(
            {'other_column':
                ['s1', 's1', 's1', 's1', 's1', 's1', 's1', 's1', 
                 's2', 's2', 's2', 's2', 's2', 's2', 's2', 's2']},
            index=index)

        metadata = Metadata(metadata)

        with self.assertRaisesRegex(
                ValueError,
                f'Unique column id {self.individual_id_column} '
                f'not found in metadata columns.'):

            convex_hull(
                metadata,
                self.pcoa,
                self.individual_id_column,
                self.number_of_dimensions)

    def test_pcoa_too_few_dimensions(self):

        index = pd.Index(
                    ['i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8',
                     'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8'],
                    name='sampleid')

        samples_df = pd.DataFrame(
            {'PC1': [0, 0, 0, 0, 1, 1, 1, 1,
                     3, 3, 3, 3, 4, 4, 4, 4]},
            index=index)

        proportion_explained = pd.Series(
            [15.5],
            index=['PC1'])

        values = pd.Series(
            np.array([1.0]),
            index=['PC1'])

        pcoa = OrdinationResults(
            'PCoA',
            'Principal Coordinate Analysis',
            values,
            samples_df,
            proportion_explained=proportion_explained)

        with self.assertRaisesRegex(
                ValueError,
                'PCoA result has too few dimensions.'):

            validate(
                self.metadata,
                pcoa,
                self.individual_id_column)

    def test_meta(self):

        meta = validate(
            self.metadata,
            self.pcoa,
            self.individual_id_column)

        assert(meta.index.equals(self.pcoa.samples.index))

    def test_n_timepoints(self):

        index = pd.Index(
                    ['i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8',
                     'x1', 'x2'],
                    name='sampleid')

        samples_df = pd.DataFrame(
            {'PC1': [0, 0, 0, 0, 1, 1, 1, 1,
                     3, 3],
             'PC2': [0, 0, 1, 1, 0, 0, 1, 1,
                     3, 3],
             'PC3': [0, 1, 0, 1, 0, 1, 0, 1,
                     3, 4]},
            index=index)

        proportion_explained = pd.Series(
            [15.5, 12.2, 8.7],
            index=['PC1', 'PC2', 'PC3'])

        values = pd.Series(
            np.array([0.7, 0.2, 0.1]),
            index=['PC1', 'PC2', 'PC3'])

        pcoa = OrdinationResults(
            'PCoA',
            'Principal Coordinate Analysis',
            values,
            samples_df,
            proportion_explained=proportion_explained)

        metadata = pd.DataFrame(
            {self.individual_id_column:
                ['s1', 's1', 's1', 's1', 's1', 's1', 's1', 's1', 
                 's2', 's2']},
            index=index)

        metadata = Metadata(metadata)

        with self.assertWarnsRegex(
            Warning,
            ('Number of timepoints less than '
             'number of dimensions.'
             'Skipping individual s2')):

            convex_hull(
                metadata,
                pcoa,
                self.individual_id_column,
                self.number_of_dimensions)
