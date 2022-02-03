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


def validate(metadata, pcoa, individual_id_column):

    try:
        meta = metadata.loc[list(pcoa.samples.index)]
    except KeyError:
        raise KeyError('PCoA result indeces do not match metadata.')
    columns = metadata.columns
    if individual_id_column not in columns:
        raise ValueError('Unique column id not found in metadata columns.')

    return meta


def convex_hull(metadata: pd.DataFrame,
                pcoa: OrdinationResults,
                individual_id_column: str,
                number_of_dimensions: int = DEFAULT_N_DIMENSIONS) \
                    -> (pd.DataFrame):
    """ Computes Convex Hull of a set of samples with multiple
    timepoints for each sample.

    Parameters
    ----------
    metadata: pd.DataFrame
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
    meta = validate(metadata, pcoa, individual_id_column)
    hulls = []
    for person, group in meta.groupby(individual_id_column):
        n_timepts = len(group)
        if n_timepts <= number_of_dimensions:
            # TODO add a warning
            continue
        coords = pcoa.samples.loc[group.index].values[:, :number_of_dimensions]
        c_hull = ConvexHull(coords)
        hulls.append([person, c_hull.volume, c_hull.area])
    hulls = pd.DataFrame(hulls, columns=[individual_id_column,
                                         'convexhull_volume',
                                         'convexhull_area'])
    return hulls
