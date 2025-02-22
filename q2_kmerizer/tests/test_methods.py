# ----------------------------------------------------------------------------
# Copyright (c) 2024, N. Bokulich.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pandas as pd
import pandas.testing as pdt

from qiime2.plugin.testing import TestPluginBase
from qiime2 import Artifact, Metadata

from q2_kmerizer._methods import seqs_to_kmers


class KmerizerTests(TestPluginBase):
    package = 'q2_kmerizer.tests'

    def setUp(self):
        super().setUp()
        self.core_metrics = self.plugin.pipelines['core_metrics']
        self.seqs = pd.Series(
            ['TACGGGAGGGTGCAAGCGTT', 'TACGAGAAGGGTTAGCGTTA'], index=['A', 'B'])
        self.table = pd.DataFrame([[1, 0], [2, 3], [1, 1]],
                                  columns=['A', 'B'], index=['s1', 's2', 's3'])

    def test_count_vectorizer(self):
        observed = seqs_to_kmers(self.seqs, self.table, kmer_size=7)

        expected = pd.DataFrame(
            [[1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1,
              0, 0, 1, 0, 1, 0],
             [2, 3, 3, 2, 3, 3, 2, 3, 2, 3, 2, 3, 3, 2, 2, 2, 2, 2, 3, 2, 3, 2,
              3, 3, 2, 3, 2, 3],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
              1, 1, 1, 1, 1, 1]],
            columns=['AAGCGTT', 'AAGGGTT', 'ACGAGAA', 'ACGGGAG', 'AGAAGGG',
                     'AGCGTTA', 'AGGGTGC', 'AGGGTTA', 'CAAGCGT', 'CGAGAAG',
                     'CGGGAGG', 'GAAGGGT', 'GAGAAGG', 'GAGGGTG', 'GCAAGCG',
                     'GGAGGGT', 'GGGAGGG', 'GGGTGCA', 'GGGTTAG', 'GGTGCAA',
                     'GGTTAGC', 'GTGCAAG', 'GTTAGCG', 'TACGAGA', 'TACGGGA',
                     'TAGCGTT', 'TGCAAGC', 'TTAGCGT'],
            index=['s1', 's2', 's3'])
        print(observed.to_dataframe().T)

        # note: observed df is transposed because it is transposed by biom
        pdt.assert_frame_equal(observed.to_dataframe().T, expected,
                               check_dtype=False)

    def test_tfidf_vectorizer(self):
        observed = seqs_to_kmers(
            self.seqs, self.table, tfidf=True, kmer_size=7)

        expected = pd.DataFrame(
            [[1.405465, 0.        , 0.        , 1.405465, 0.        ,
              0.        , 1.405465, 0.        , 1.405465, 0.        ,
              1.405465, 0.        , 0.        , 1.405465, 1.405465,
              1.405465, 1.405465, 1.405465, 0.        , 1.405465,
              0.        , 1.405465, 0.        , 0.        , 1.405465,
              0.        , 1.405465, 0.],
             [2.81093, 4.216395, 4.216395, 2.81093, 4.216395,
              4.216395, 2.81093, 4.216395, 2.81093, 4.216395,
              2.81093, 4.216395, 4.216395, 2.81093, 2.81093,
              2.81093, 2.81093, 2.81093, 4.216395, 2.81093,
              4.216395, 2.81093, 4.216395, 4.216395, 2.81093,
              4.216395, 2.81093, 4.216395],
             [1.405465, 1.405465, 1.405465, 1.405465, 1.405465,
              1.405465, 1.405465, 1.405465, 1.405465, 1.405465,
              1.405465, 1.405465, 1.405465, 1.405465, 1.405465,
              1.405465, 1.405465, 1.405465, 1.405465, 1.405465,
              1.405465, 1.405465, 1.405465, 1.405465, 1.405465,
              1.405465, 1.405465, 1.405465]],
            columns=['AAGCGTT', 'AAGGGTT', 'ACGAGAA', 'ACGGGAG', 'AGAAGGG',
                     'AGCGTTA', 'AGGGTGC', 'AGGGTTA', 'CAAGCGT', 'CGAGAAG',
                     'CGGGAGG', 'GAAGGGT', 'GAGAAGG', 'GAGGGTG', 'GCAAGCG',
                     'GGAGGGT', 'GGGAGGG', 'GGGTGCA', 'GGGTTAG', 'GGTGCAA',
                     'GGTTAGC', 'GTGCAAG', 'GTTAGCG', 'TACGAGA', 'TACGGGA',
                     'TAGCGTT', 'TGCAAGC', 'TTAGCGT'],
            index=['s1', 's2', 's3'])

        # note: observed df is transposed because it is transposed by biom
        pdt.assert_frame_equal(observed.to_dataframe().T, expected,
                               check_dtype=False)

    def test_error_on_non_matched_ids(self):
        new_seqs = pd.Series(
            ['AAAAAAAA', 'AAAATTTT'], index=['no', 'match'])
        with self.assertRaisesRegex(ValueError, "No feature IDs match*"):
            seqs_to_kmers(new_seqs, self.table, tfidf=True)

    # this test just tests that the pipeline runs, as the individual actions
    # are already tested.
    # TODO: inspect the scatterplot output to check that contents are correct?
    def test_core_metrics(self):
        metadata = Metadata(pd.DataFrame(
            [['blue'], ['red'], ['blue']], columns=['color'],
            index=pd.Index(['s1', 's2', 's3'], name='id')))
        seqs = Artifact.import_data('FeatureData[Sequence]', self.seqs)
        table = Artifact.import_data('FeatureTable[Frequency]', self.table)
        self.core_metrics(seqs, table, metadata=metadata,
                          sampling_depth=1, kmer_size=7,
                          color_by='color')
