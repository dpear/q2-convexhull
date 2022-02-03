#!/usr/bin/env python

# ----------------------------------------------------------------------------
# Copyright (c) 2022--, convex-hull development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import setup, find_packages

setup(
    name="q2-convexhull",
    packages=find_packages(),
    version='0.0.1',
    author="Daniela Perry",
    author_email="dsperry@ucsd.edu",
    description="convex hull analysis for microbiome data",
    license='BSD-3',
    entry_points={
        'qiime2.plugins': ['q2-convexhull=q2_convexhull.plugin_setup:plugin']
    },
    package_data={
        "q2_convexhull": ['citations.bib'],
    },
    zip_safe=False,
    install_requires=['scikit-learn',
                      'scipy',
                      'scikit-bio',
                      'pandas']
)

