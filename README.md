# q2-kmerizer

A [QIIME 2](https://qiime2.org) plugin for generating and working with kmers from biological sequence information.

Note: this plugin is under active development during pre-release. The code should not be considered stable or ready for publication-ready analyses.

## Installation instructions

###  Install in an existing QIIME 2 environment

q2-kmerizer is compatible with QIIME 2 amplicon and metagenome distributions from release versions 2024.5+. To install in one of these environments, make sure that the relevant conda environment is activated and then install with:
```
pip install https://github.com/bokulich-lab/q2-kmerizer.git
```

The run the following to refresh the cache and test that the installation worked:
```
qiime dev refresh-cache
qiime kmerizer --help
```

### Install development version of `q2-kmerizer` "from scratch"

If you do not already have a QIIME 2 environment installed, you can follow these instructions to install a development version of q2-kmerizer.

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


## About

The `q2-kmerizer` Python package was [created from template](https://develop.qiime2.org/en/latest/plugins/tutorials/create-from-template.html).
To learn more about `q2-kmerizer`, refer to the [project website](https://github.com/bokulich-lab/q2-kmerizer).
To learn how to use QIIME 2, refer to the [QIIME 2 User Documentation](https://docs.qiime2.org).
To learn QIIME 2 plugin development, refer to [*Developing with QIIME 2*](https://develop.qiime2.org).

`q2-kmerizer` is a QIIME 2 plugin. For questions, comments, or feature requests about this plugin, please post in the [Community Plugins category](https://forum.qiime2.org/c/community-contributions/community-plugins/14) on the QIIME 2 Forum. The issue tracker on the GitHub repository is intended for use by the plugin developers and maintainers, not as a help forum.
