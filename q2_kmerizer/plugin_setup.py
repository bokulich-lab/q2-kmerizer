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
from qiime2.plugin import (Int, Float, Bool, Range, Visualization, Metadata,
                           Str, Choices)
from q2_types.feature_data import (
    FeatureData, Sequence, RNASequence, ProteinSequence)
from q2_types.distance_matrix import DistanceMatrix
from q2_types.sample_data import AlphaDiversity, SampleData
from q2_types.ordination import PCoAResults

from q2_kmerizer._methods import seqs_to_kmers, core_metrics


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

n_jobs_description = (
    'The number of concurrent jobs to use in performing this calculation. '
    'May not exceed the number of available physical cores. If n_jobs = '
    '\'auto\', one job will be launched for each identified CPU core on the '
    'host.'
)

inputs = {
    'sequences': FeatureData[Sequence | RNASequence | ProteinSequence],
    'table': FeatureTable[Frequency]}

core_parameters = {
    'kmer_size': Int,
    'tfidf': Bool,
    'max_df': Float % Range(0, 1, inclusive_start=True,
                            inclusive_end=True) | Int,
    'min_df': Float % Range(0, 1, inclusive_start=True,
                            inclusive_end=False) | Int,
    'max_features': Int}

input_descriptions = {'sequences': 'Biological sequences to kmerize.',
                      'table': 'Frequencies of sequences per sample.'}

core_parameters_descriptions = {
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
                    'score).'}

plugin.methods.register_function(
    function=seqs_to_kmers,
    inputs=inputs,
    parameters=core_parameters,
    outputs=[('kmer_table', FeatureTable[Frequency])],
    input_descriptions=input_descriptions,
    parameter_descriptions=core_parameters_descriptions,
    output_descriptions={'kmer_table': 'Frequencies of kmers per sample.'},
    name='Generate kmers from sequences.',
    description="Generate kmers from biological sequences.",
    citations=[citations['pedregosa2011scikit']]
)

plugin.pipelines.register_function(
    function=core_metrics,
    inputs=inputs,
    parameters={**core_parameters,
                'sampling_depth': Int % Range(1, None),
                'metadata': Metadata,
                'with_replacement': Bool,
                'n_jobs': Int % Range(1, None) | Str % Choices(['auto']),
                'pc_dimensions': Int,
                'color_by': Str},
    outputs=[
        ('rarefied_table', FeatureTable[Frequency]),
        ('kmer_table', FeatureTable[Frequency]),
        ('observed_features_vector', SampleData[AlphaDiversity]),
        ('shannon_vector', SampleData[AlphaDiversity]),
        ('jaccard_distance_matrix', DistanceMatrix),
        ('bray_curtis_distance_matrix', DistanceMatrix),
        ('jaccard_pcoa_results', PCoAResults),
        ('bray_curtis_pcoa_results', PCoAResults),
        ('scatterplot', Visualization),
    ],
    input_descriptions=input_descriptions,
    parameter_descriptions={
        **core_parameters_descriptions,
        'sampling_depth': 'The total frequency that each sample should be '
        'rarefied to prior to computing diversity metrics.',
        'metadata': 'The sample metadata to use in the emperor plots.',
        'with_replacement': 'Rarefy with replacement by sampling from the '
                            'multinomial distribution instead of rarefying '
                            'without replacement.',
        'n_jobs': '[beta methods only] - %s' % n_jobs_description,
        'pc_dimensions': 'Number of principal coordinate dimensions to keep '
                         'for plotting.',
        'color_by': 'Categorical measure from the input Metadata that '
                    'should be used for color-coding the scatterplot.'},
    output_descriptions={
        'rarefied_table': 'The resulting rarefied feature table.',
        'kmer_table': 'Frequencies of kmers per sample.',
        'observed_features_vector': 'Vector of Observed Kmers values by '
                                    'sample.',
        'shannon_vector': 'Vector of Shannon diversity values by sample.',
        'jaccard_distance_matrix':
            'Matrix of Jaccard distances between pairs of samples.',
        'bray_curtis_distance_matrix':
            'Matrix of Bray-Curtis dissimilarities between pairs of samples.',
        'jaccard_pcoa_results':
            'PCoA matrix computed from Jaccard distances between samples.',
        'bray_curtis_pcoa_results':
            'PCoA matrix computed from Bray-Curtis dissimilarities between '
            'samples.',
        'scatterplot':
            'Scatterplot of results. Axes can be selected to display alpha '
            'diversity results or PCoA coordinates computed from Jaccard or '
            'Bray-Curtis.',
    },
    name='Kmer counting and core diversity metrics (non-phylogenetic)',
    description='Generate kmer counts from sequences and apply a collection '
                'of diversity metrics (non-phylogenetic) to compare samples.'
)
