# ----------------------------------------------------------------------------
# Copyright (c) 2022--, convex-hull development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import scipy
import skbio
import qiime2
import itertools # ???
import numpy as np 
import pandas as pd
import scipy.stats as ss
from qiime2.plugins import diversity, feature_table # ???
from scipy.spatial import ConvexHull
from convexhull._defaults import (DEFAULT_N_DIMENSIONS)

def validate(metadata, pcoa, column):

	meta_type = qiime2.metadata.metadata.Metadata
    pcoa_type = qiime2.sdk.result.Artifact     # Not sure if this is the right type 
    col_type  = str
    columns   = metadata.to_dataframe().columns

    if type(metadata) != meta_type:
        raise TypeError(f'Metadata is not of type {meta_type}')
    if type(pcoa) != pcoa_type:
        raise TypeError(f'PCoA result is not of type {pcoa_type}')
    if type(column) != col_type:
        raise TypeError(f'Invalid unique column id. Must be of type {col_type}.')
    if column not in columns:
        raise ValueError('Unique column id not found in metadata columns.')

def convex_hull(metadata: Metadata, 
				pcoa: Artifact, 
				column: str, 
				ndim=DEFAULT_N_DIMENSIONS: int): # Help with mypy format here
    """ Computes Convex Hull of a set of samples with multiple
    timepoints for each sample. 
    Parameters
    ----------
    metadata: qiime2.metadata.metadata.Metadata
        Metadata table associated with PCoA results.

    pcoa: qiime2.sdk.result.Artifact
        PCOA result.
        
    column: str
        Unique subject identifier column in `metadata`. Must
        be unique to each subject. Can be repeated for 
        multiple time points.
        
    ndim: int (Default 3)
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
    
    ### QUESTIONS ###
    # x1) What should all the input types be? (DataFrame for metadata??)
    # x2) Is there a better way to raise a KeyError (than try except)
    # 3) Is this code messy if so why?
    
	validate(metadata, pcoa, column)
    
    try:
        meta = metadata.loc[list(pcoa.samples.index)]
    except:
        KeyError('PCoA result indeces do not match metadata.')
        
    hulls = []

    meta_group = meta.groupby(column)
    for person, group in meta_group:
        
        n_timepts = len(group)
        if n_timepts <= ndim:
            continue

        coords = pcoa.samples.loc[group.index].values[:, :ndim]
        c_hull = ConvexHull(coords)
        hulls.append( [person, c_hull.volume, c_hull.area] )

    hulls = pd.DataFrame(hulls, columns=[column,
                                       'convexhull_volume', 
                                       'convexhull_area'])
    return hulls