from qiime2.plugin import (Plugin, Int, Citations,
                           Str, Range, Metadata)
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
        'metadata': Metadata,
        'pcoa': PCoAResults,
        'individual_id_column': Str,
    },
    parameters={
        'number_of_dimensions': Int % Range(2, 3, inclusive_end=True),
    },
    outputs=[
        ('hulls', Metadata),
    ],
    input_descriptions={
        'metadata': (
            'Metadata table with samples matching the PCoA results.'
        ),
        'pcoa': (
            'Resulting dimensionality reduction for convex hull.'
        ),
        'individual_id_column': (
            'Metadata column containing IDs for individual subjects.'
        ),
    },
    parameter_descriptions={
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
