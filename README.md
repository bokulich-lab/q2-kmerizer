# q2-kmerizer

A [QIIME 2](https://qiime2.org) plugin for generating and working with kmers from biological sequence information.

Note: this plugin is under active development during pre-release. The code should not be considered stable or ready for publication-ready analyses.

## Installation instructions

### Install into an existing QIIME 2 environment

The simplest and recommended way to install q2-kmerizer is into an existing QIIME 2 conda environment. You can install QIIME 2 following the instructions at https://docs.qiime2.org/.

Next, activate that conda environment, clone the q2-kmerizer repository and move into the top-level `q2-kmerizer` directory.

```
git clone https://github.com/bokulich-lab/q2-kmerizer.git
git cd q2-kmerizer
```

Finally, to install q2-kmerizer run:

```shell
make install
qiime dev refresh-cache
```

If the installation worked correctly, the following command should display a description of the plugin in your terminal:
```
qiime kmerizer --help
```

### Install development version of `q2-kmerizer` "from scratch"

If you do not already have a QIIME 2 environment installed and wish to install a development version of q2-kmerizer, you can follow these instructions to install a development version of q2-kmerizer.

[Miniconda](https://conda.io/miniconda.html) provides the `conda` environment and package manager, and is currently the only supported way to install QIIME 2.
Follow the instructions for downloading and installing Miniconda.

After installing Miniconda and opening a new terminal, make sure you're running the latest version of `conda`:

```bash
conda update conda
```

Next, clone the repository and move into the top-level `q2-kmerizer` directory. NOTE: make sure your current working directory is a location where you want to install this plugin!

```
git clone https://github.com/bokulich-lab/q2-kmerizer.git
git cd q2-kmerizer
```

Then, run:

```shell
conda env create -n q2-kmerizer-dev --file ./environments/q2-kmerizer-qiime2-amplicon-2024.10.yml
```

After this completes, activate the new environment you created by running:

```shell
conda activate q2-kmerizer-dev
```

Finally, run:

```shell
make install
```


## Examples

As an example test, we will use data from [Sampson et al, 2016](https://www.ncbi.nlm.nih.gov/pubmed/27912057), a study testing whether the fecal microbiome contributed to the development of Parkinson’s Disease (PD).

First we will download the test data:

```
wget https://data.qiime2.org/2024.5/tutorials/pd-mice/sample_metadata.tsv
wget https://docs.qiime2.org/2024.5/data/tutorials/pd-mice/dada2_table.qza
wget https://docs.qiime2.org/2024.5/data/tutorials/pd-mice/dada2_rep_set.qza
```

We can count kmer frequencies per sample with this command:
```
qiime kmerizer seqs-to-kmers \
    --i-sequences dada2_rep_set.qza \
    --i-table dada2_table.qza \
    --o-kmer-table kmer_table.qza \
    --p-max-features 5000
```

Or run this pipeline to count kmer frequencies, calculate diversity metrics, and create an interactive scatterplot with the results:

```
qiime kmerizer core-metrics \
    --i-sequences dada2_rep_set.qza \
    --i-table dada2_table.qza \
    --p-sampling-depth 1000 \
    --m-metadata-file sample_metadata.tsv \
    --p-color-by-group donor \
    --p-max-features 5000 \
    --output-dir core-metrics/
```

Both of these actions output a frequency table that contains kmer counts per sample. This can be used like any other frequency table and passed to any action in QIIME 2 that accepts a frequency table (except for those that also require additional inputs that must match the features in the table, e.g., that require a taxonomy). For example, we can run a pipeline to train a Random Forest classifier and test on a hold-out subset of the dataset (note: this analysis is done purely for demonstrative purposes; the sample size in this test dataset is much smaller than would be required for a robust supervised learning analysis, and proper replicate handling should be done to avoid data leakage).


```
qiime sample-classifier classify-samples \
    --i-table kmer_table.qza \
    --m-metadata-file sample_metadata.tsv \
    --m-metadata-column donor \
    --output-dir sample-classifier/
```

## About

The `q2-kmerizer` Python package was [created from a template](https://develop.qiime2.org/en/latest/plugins/tutorials/create-from-template.html).
To learn more about `q2-kmerizer`, refer to the [project website](https://github.com/bokulich-lab/q2-kmerizer).
To learn how to use QIIME 2, refer to the [QIIME 2 User Documentation](https://docs.qiime2.org).
To learn QIIME 2 plugin development, refer to [*Developing with QIIME 2*](https://develop.qiime2.org).

`q2-kmerizer` is a QIIME 2 plugin. For questions, comments, or feature requests about this plugin, please post in the [Community Plugins category](https://forum.qiime2.org/c/community-contributions/community-plugins/14) on the QIIME 2 Forum. The issue tracker on the GitHub repository is intended for use by the plugin developers and maintainers, not as a help forum.

## Citation

If you use q2-kmerizer in your work, please cite the following article:

Bokulich, N.A. 2024. Integrating sequence composition information into microbial diversity analyses with k-mer frequency counting. bioRxiv 2024.08.13.607770; doi: https://doi.org/10.1101/2024.08.13.607770 
