# ----------------------------------------------------------------------------
# Copyright (c) 2024, N. Bokulich.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import numpy as np
import pandas as pd
import biom
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from skbio import OrdinationResults
from qiime2 import Metadata


def seqs_to_kmers(sequences: pd.Series, table: pd.DataFrame,
                  kmer_size: int = 16, tfidf: bool = False,
                  max_df: float = 1.0, min_df: float = 1,
                  max_features: float = None) -> biom.Table:
    # ngram_range = tuple
    # convert single kmer size to tuple (range is not enabled at this time)
    ngram_range = (kmer_size, kmer_size)

    # min_df should be an integer if ≥ 1.0 otherwise this would filter out all
    # kmers that are not found in every sequence, which probably almost nobody
    # would ever want.
    # TODO: is there a way to allow the user to choose min_df = 1.0?
    if min_df >= 1.0:
        min_df = int(min_df)

    # Align table and sequences to match order and intersection of features
    table, sequences = table.align(sequences, join='inner', axis=1)
    if len(sequences) < 1:
        raise ValueError('No feature IDs match between the inputs.')

    # vectorize
    if tfidf:
        _vectorizer = TfidfVectorizer
    else:
        _vectorizer = CountVectorizer
    cv = _vectorizer(ngram_range=ngram_range, analyzer='char', lowercase=False,
                     max_df=max_df, min_df=min_df, max_features=max_features)
    # derive table of kmer frequencies per sequence
    X = cv.fit_transform(sequences.apply(str).values.tolist())
    # matrix multiplication of sampleXsequence X sequenceXkmer = sampleXkmer
    frequencies = np.dot(table, X.toarray())
    # convert to biom Table for outputting as a FeatureTable[Frequency]
    # transpose inputs as biom expects observations as rows
    kmer_table = biom.table.Table(
        frequencies.T, observation_ids=cv.get_feature_names_out(),
        sample_ids=table.index)
    return kmer_table


def core_metrics(ctx, sequences, table, sampling_depth, metadata,
                 kmer_size=16, tfidf=False, max_df=1.0, min_df=1,
                 max_features=None, with_replacement=False, n_jobs=1,
                 pc_dimensions=3, color_by=None):

    rarefy = ctx.get_action('feature_table', 'rarefy')
    kmerize = ctx.get_action('kmerizer', 'seqs_to_kmers')
    observed_features = ctx.get_action('diversity_lib', 'observed_features')
    shannon = ctx.get_action('diversity_lib', 'shannon_entropy')
    braycurtis = ctx.get_action('diversity_lib', 'bray_curtis')
    jaccard = ctx.get_action('diversity_lib', 'jaccard')
    pcoa = ctx.get_action('diversity', 'pcoa')
    scatter = ctx.get_action('vizard', 'scatterplot_2d')

    results = []
    rarefied_table, = rarefy(table=table, sampling_depth=sampling_depth,
                             with_replacement=with_replacement)
    results.append(rarefied_table)

    kmer_table, = kmerize(sequences, rarefied_table, kmer_size, tfidf, max_df,
                          min_df, max_features)
    results.append(kmer_table)

    for metric in (observed_features, shannon):
        alpha_result = metric(table=kmer_table)
        results += alpha_result
        metadata = alpha_result.vector.view(Metadata).merge(metadata)

    dms = []
    for metric in (jaccard, braycurtis):
        beta_results = metric(table=kmer_table, n_jobs=n_jobs)
        results += beta_results
        dms += beta_results

    pcoas = []
    for dm in dms:
        pcoa_results = pcoa(distance_matrix=dm)
        results += pcoa_results
        pcoas += pcoa_results

    for pcoa, name in zip(pcoas, ['Jaccard', 'Bray-Curtis']):
        pc_result = pcoa.view(OrdinationResults)
        prop_explained = pc_result.proportion_explained[:pc_dimensions].values
        pc_result = pcoa.view(Metadata).to_dataframe().iloc[:, :pc_dimensions]
        pc_result.columns = ['{0} {1} ({2}%)'.format(name, c, int(p * 100)) for
                             c, p in zip(pc_result.columns, prop_explained)]
        metadata = Metadata(pc_result).merge(metadata)

    results += scatter(metadata=metadata,
                       # x_measure=pc_result.columns[0],
                       # y_measure=pc_result.columns[1],
                       color_by=color_by)

    return tuple(results)
