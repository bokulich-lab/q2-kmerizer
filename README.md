# q2-kmerizer

A [QIIME 2](https://qiime2.org) plugin for generating and working with kmers from biological sequence information.

## Installation instructions

The easiest way to install q2-kmerizer is to install it directly into an existing installation of [QIIME 2](https://qiime2.org/) (amplicon distribution version 2024.10 or later). If you have the QIIME 2 amplicon distribution installed, activate your environment and run the following to install q2-kmerizer into this environment:
```
pip install q2_kmerizer@git+https://github.com/bokulich-lab/q2-kmerizer.git@main
```

And refresh your cache:
```
qiime dev refresh-cache
```

If the installation worked correctly, the following command should display a description of the plugin in your terminal:
```
qiime kmerizer --help
```



### Installation of stable release

If you do not already have QIIME 2 installed, you can follow these instructions to install the QIIME 2 amplicon distribution as well as the latest stable version of q2-kmerizer.

[Miniconda](https://conda.io/miniconda.html) provides the `conda` environment and package manager, and is currently the only supported way to install QIIME 2.
Follow the instructions for downloading and installing Miniconda.

After installing Miniconda and opening a new terminal, make sure you're running the latest version of `conda`:

```bash
conda update conda
```

Now use conda to install q2-kmerizer and QIIME 2:

```shell
conda env create -n kmerizer-stable --file https://raw.githubusercontent.com/bokulich-lab/q2-kmerizer/main/environment-files/q2-kmerizer-qiime2-amplicon-2025.4.yml
```

After this completes, activate the new environment you created by running:

```shell
conda activate kmerizer-stable
```

Then refresh your cache and test as shown above.


### Install development version of `q2-kmerizer`

If you wish to use the development version of q2-kmerizer, e.g., to develop new features in your fork or to contribute to the main branch, follow these instructions.

First, you must have conda installed, as described above.

Next, clone the repository and move into the top-level `q2-kmerizer` directory. NOTE: make sure your current working directory is a location where you want to install this plugin!

```
git clone https://github.com/bokulich-lab/q2-kmerizer.git
cd q2-kmerizer
```

Then, run:

```shell
conda env create -n q2-kmerizer-dev --file ./environment-files/q2-kmerizer-qiime2-amplicon-2025.4.yml
```

After this completes, activate the new environment you created by running:

```shell
conda activate q2-kmerizer-dev
```

Finally, run:

```shell
make install
```

Then refresh your cache and test as shown above.



## Examples

As an example test, we will use data from [Sampson et al, 2016](https://www.ncbi.nlm.nih.gov/pubmed/27912057), a study testing whether the fecal microbiome contributed to the development of Parkinson’s Disease (PD).

First we will download the test data:

```
wget https://data.qiime2.org/2024.10/tutorials/pd-mice/sample_metadata.tsv
wget https://docs.qiime2.org/2024.10/data/tutorials/pd-mice/dada2_table.qza
wget https://docs.qiime2.org/2024.10/data/tutorials/pd-mice/dada2_rep_set.qza
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

Bokulich NA. 2024. Integrating sequence composition information into microbial diversity analyses with k-mer frequency counting. mSystems:e01550-24. https://doi.org/10.1128/msystems.01550-24 
