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
