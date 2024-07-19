# q2-kmerizer

A [QIIME 2](https://qiime2.org) plugin [developed](https://develop.qiime2.org) by N. Bokulich (nbokulich@gmail.com). 🔌

## Installation instructions

**The following instructions are intended to be a starting point** and should be replaced when `q2-kmerizer` is ready to share with others.
They will enable you to install the most recent *development* version of `q2-kmerizer`.
Remember that *release* versions should be used for all "real" work (i.e., where you're not testing or prototyping) - if there aren't instructions for installing a release version of this plugin, it is probably not yet intended for use in practice.

### Install Prerequisites

[Miniconda](https://conda.io/miniconda.html) provides the `conda` environment and package manager, and is currently the only supported way to install QIIME 2.
Follow the instructions for downloading and installing Miniconda.

After installing Miniconda and opening a new terminal, make sure you're running the latest version of `conda`:

```bash
conda update conda
```

###  Install development version of `q2-kmerizer`

Next, you need to get into the top-level `q2-kmerizer` directory.
If you already have this (e.g., because you just created the plugin), this may be as simple as running `cd q2-kmerizer`.
If not, you'll need the `q2-kmerizer` directory on your computer.
How you do that will differ based on how the package is shared, and ideally the developer will update these instructions to be more specific (remember, these instructions are intended to be a starting point).
For example, if it's maintained in a GitHub repository, you can achieve this by [cloning the repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).
Once you have the directory on your computer, change (`cd`) into it.

If you're in a conda environment, deactivate it by running `conda deactivate`.


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

## Testing and using the most recent development version of `q2-kmerizer`

After completing the install steps above, confirm that everything is working as expected by running:

```shell
make test
```

You should get a report that tests were run, and you should see that all tests passed and none failed.
It's usually ok if some warnings are reported.

If all of the tests pass, you're ready to use the plugin.
Start by making QIIME 2's command line interface aware of `q2-kmerizer` by running:

```shell
qiime dev refresh-cache
```

You should then see the plugin in the list of available plugins if you run:

```shell
qiime info
```

You should be able to review the help text by running:

```shell
qiime kmerizer --help
```

Have fun! 😎

## About

The `q2-kmerizer` Python package was [created from template](https://develop.qiime2.org/en/latest/plugins/tutorials/create-from-template.html).
To learn more about `q2-kmerizer`, refer to the [project website](https://github.com/bokulich-lab/q2-kmerizer).
To learn how to use QIIME 2, refer to the [QIIME 2 User Documentation](https://docs.qiime2.org).
To learn QIIME 2 plugin development, refer to [*Developing with QIIME 2*](https://develop.qiime2.org).

`q2-kmerizer` is a QIIME 2 community plugin, meaning that it is not necessarily developed and maintained by the developers of QIIME 2.
Please be aware that because community plugins are developed by the QIIME 2 developer community, and not necessarily the QIIME 2 developers themselves, some may not be actively maintained or compatible with current release versions of the QIIME 2 distributions.
More information on development and support for community plugins can be found [here](https://library.qiime2.org).
If you need help with a community plugin, first refer to the [project website](https://github.com/bokulich-lab/q2-kmerizer).
If that page doesn't provide information on how to get help, or you need additional help, head to the [Community Plugins category](https://forum.qiime2.org/c/community-contributions/community-plugins/14) on the QIIME 2 Forum where the QIIME 2 developers will do their best to help you.
