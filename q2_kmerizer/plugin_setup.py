# ----------------------------------------------------------------------------
# Copyright (c) 2024, N. Bokulich.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import Citations, Plugin
from q2_types.feature_table import FeatureTable, Frequency
from q2_kmerizer import __version__
from q2_kmerizer._methods import seqs_to_kmers
from qiime2.plugin import Int, Float, Bool, Range
from q2_types.feature_data import (
    FeatureData, Sequence, RNASequence, ProteinSequence)


citations = Citations.load("citations.bib", package="q2_kmerizer")

plugin = Plugin(
    name="kmerizer",
    version=__version__,
    website="https://github.com/bokulich-lab/q2-kmerizer",
    package="q2_kmerizer",
    description="A plugin to generate kmers from biological sequences.",
    short_description="Kmer generation from sequences.",
    citations=[]
)

plugin.methods.register_function(
    function=seqs_to_kmers,
    inputs={'sequences': FeatureData[Sequence | RNASequence | ProteinSequence],
            'table': FeatureTable[Frequency]},
    parameters={'kmer_size': Int,
                'tfidf': Bool,
                'max_df': Float % Range(0, 1, inclusive_start=True,
                                        inclusive_end=True) | Int,
                'min_df': Float % Range(0, 1, inclusive_start=True,
                                        inclusive_end=False) | Int,
                'max_features': Int
                },
    outputs=[('kmer_table', FeatureTable[Frequency])],
    input_descriptions={'sequences': 'Biological sequences to kmerize.',
                        'table': 'Frequencies of sequences per sample.'},
    parameter_descriptions={
        'kmer_size': 'Length of kmers to generate.',
        'tfidf': 'If True, kmers will be scored using TF-IDF and output '
                 'frequencies will be weighted by scores. If False, kmers are '
                 'counted without TF-IDF scores.',
        'max_df': 'Ignore kmers that have a frequency strictly higher than '
                  'the given threshold. If float, the parameter represents a '
                  'proportion of sequences, if an integer it represents an '
                  'absolute count.',
        'min_df': 'Ignore kmers that have a frequency strictly lower than '
                  'the given threshold. If float, the parameter represents a '
                  'proportion of sequences, if an integer it represents an '
                  'absolute count.',
        'max_features': 'If not None, build a vocabulary that only considers '
                        'the top max_features ordered by frequency (or TF-IDF '
                        'score).'},
    output_descriptions={'kmer_table': 'Frequencies of kmers per sample.'},
    name='Generate kmers from sequences.',
    description="Generate kmers from biological sequences.",
    citations=['pedregosa2011scikit']
)
