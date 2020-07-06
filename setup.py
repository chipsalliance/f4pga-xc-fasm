#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017-2020  The Project X-Ray Authors.
#
# Use of this source code is governed by a ISC-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/ISC
#
# SPDX-License-Identifier: ISC

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xc-fasm",
    version="0.0.1",
    author="SymbiFlow Authors",
    author_email="symbiflow@lists.librecores.org",
    description="XC FASM libraries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SymbiFlow/xc-fasm",
    packages=['xc_fasm'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "intervaltree",
        "simplejson",
        "textx",
        "prjxray@git+git://github.com/SymbiFlow/prjxray.git#egg=prjxray",
        "fasm@git+git://github.com/SymbiFlow/fasm.git#egg=fasm",
    ],
    entry_points={
        'console_scripts': ['xcfasm=xc_fasm.xc_fasm:main'],
    })
