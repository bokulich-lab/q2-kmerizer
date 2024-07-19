# ----------------------------------------------------------------------------
# Copyright (c) 2024, N. Bokulich.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import find_packages, setup

import versioneer

description = ("A template QIIME 2 plugin.")

setup(
    name="q2-kmerizer",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license="BSD-3-Clause",
    packages=find_packages(),
    author="N. Bokulich",
    author_email="nbokulich@gmail.com",
    description=description,
    url="https://github.com/bokulich-lab/q2-kmerizer",
    entry_points={
        "qiime2.plugins": [
            "q2_kmerizer="
            "q2_kmerizer"
            ".plugin_setup:plugin"]
    },
    package_data={
        "q2_kmerizer": ["citations.bib"],
        "q2_kmerizer.tests": ["data/*"],
    },
    zip_safe=False,
)
