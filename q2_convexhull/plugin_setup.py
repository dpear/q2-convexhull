import importlib
from qiime2.plugin import (Plugin, Int, Citations,
                           Str, Range, Metadata)
from ._type import Hulls
from ._format import HullsDirectoryFormat
from q2_types.sample_data import SampleData
from q2_types.ordination import PCoAResults
from q2_convexhull.convexhull import convex_hull

citations = Citations.load('citations.bib', package='q2_convexhull')

plugin = Plugin(
    name='convexhull',
    version='0.1.1',
    website='https://github.com/dpear/q2-convexhull',
    package='q2_convexhull',
    description=('This QIIME 2 plugin supports exploring community '
                 'differences through convex hulls.'),
    short_description='Plugin for convex hulls.',
)

plugin.methods.register_function(
    function=convex_hull,
    inputs={
        'pcoa': PCoAResults,
    },
    parameters={
        'individual_id_column': Str,
        'metadata': Metadata,
        'number_of_dimensions': Int % Range(2, 3, inclusive_end=True),
    },
    outputs=[
        ('hulls', SampleData[Hulls]),
    ],
    input_descriptions={
        'pcoa': (
            'Resulting dimensionality reduction for convex hull.'
        ),
    },
    parameter_descriptions={
        'metadata': (
            'Metadata table with samples matching the PCoA results.'
        ),
        'individual_id_column': (
            'Metadata column containing IDs for individual subjects.'
        ),
        'number_of_dimensions': (
            'The number of components to use for convex hull calculations.'
        ),
    },
    output_descriptions={
        'hulls':
            'Metadata containing the convex hulls.'
    },
    name='convex-hull',
    description='Applies convex hulls to dimensionality reduction.',
    citations=[
        citations['Song2021-wu'],
    ]
)

plugin.register_semantic_types(Hulls)
plugin.register_semantic_type_to_format(
    SampleData[Hulls],
    artifact_format=HullsDirectoryFormat)
plugin.register_formats(HullsDirectoryFormat)
importlib.import_module('q2_convexhull._transformer')
