# ----------------------------------------------------------------------------
# Copyright (c) 2022--, convex-hull development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pandas as pd
from scipy.spatial import ConvexHull
from skbio import OrdinationResults
from q2_convexhull._defaults import (DEFAULT_N_DIMENSIONS)
from warnings import warn
from qiime2 import Metadata



def validate(metadata, pcoa, individual_id_column):

    meta = metadata.to_dataframe()

    if not all(z in meta.index for z in list(pcoa.samples.index)):
        raise KeyError('PCoA result indeces do not match metadata.')

    if individual_id_column not in metadata.columns:
        raise ValueError(f'Unique column id {individual_id_column} '
                         f'not found in metadata columns.')

    if len(pcoa.samples.columns) < 2:
        raise ValueError('PCoA result has too few dimensions.')

    meta = meta.loc[list(pcoa.samples.index)]

    return meta


def convex_hull(metadata: Metadata,
                pcoa: OrdinationResults,
                individual_id_column: str,
                number_of_dimensions: int = DEFAULT_N_DIMENSIONS) \
                    -> (pd.DataFrame):
    """ Computes Convex Hull of a set of samples with multiple
    timepoints for each sample.

    Parameters
    ----------
    metadata: qiime2.Metadata table
        Metadata table associated with PCoA results.

    pcoa: skbio.OrdinationResults
        PCoA result.

    individual_id_column: str
        Unique subject identifier column in `metadata`. Must
        be unique to each subject. Can be repeated for
        multiple time points.

    number_of_dimensions: int (Default 3)
        Number of dimensions along which to calculate the
        convex hull volume and area.

    Returns
    -------
    pandas.DataFrame
        Data frame with unique ID, convex hull volume,
        and convex hull area. Columns are
        `column`, convexhull_volume, convexhull_area.

    Raises
    ------
    TypeError, ValueError
        If inputs are of incorrect type. If column ID not
        found in metadata.
    """

    if number_of_dimensions > 3:
        warn(
            'Setting number_of_dimensions to 3.',
            Warning)
        number_of_dimensions = 3

    if len(pcoa.samples.columns) > 3:

        warn(
            (f'PCoA result has {len(pcoa.samples.columns)} '
             f"dimensions. Truncating to 3 PC's"),
            Warning)
        pcoa = OrdinationResults(pcoa.short_method_name,
                                 pcoa.long_method_name,
                                 pcoa.eigvals[:3],
                                 pcoa.samples[pcoa.samples.columns[:3]])

    meta = validate(metadata, pcoa, individual_id_column)
    hulls = []
    for person, group in meta.groupby(individual_id_column):
        n_timepts = len(group)
        if n_timepts <= number_of_dimensions:
            warn((f'Number of timepoints less than '
                  f'number of dimensions.'
                  f'Skipping individual {person}'),
                  Warning)
            continue
        coords = pcoa.samples.loc[group.index].values[:, :number_of_dimensions]
        c_hull = ConvexHull(coords)
        hulls.append([person, c_hull.volume, c_hull.area])
    hulls = pd.DataFrame(hulls, columns=[individual_id_column,
                                         'convexhull_volume',
                                         'convexhull_area'])
    return hulls
