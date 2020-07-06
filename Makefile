# Copyright (C) 2017-2020  The Project X-Ray Authors.
#
# Use of this source code is governed by a ISC-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/ISC
#
# SPDX-License-Identifier: ISC
SHELL=bash
ALL_EXCLUDE = third_party .git env build
FORMAT_EXCLUDE = $(foreach x,$(ALL_EXCLUDE),-and -not -path './$(x)/*')

PYTHON_SRCS=$(shell find . -name "*py" $(FORMAT_EXCLUDE))

IN_ENV = if [ -e env/bin/activate ]; then . env/bin/activate; fi;
env:
	virtualenv --python=python3 env
	$(IN_ENV) pip install --upgrade -r requirements.txt

.PHONY: env

format: ${PYTHON_SRCS}
	$(IN_ENV) yapf -i $?

check-license:
	@./.github/check_license.sh
	@./.github/check_python_scripts.sh

test-py:
	$(IN_ENV) cd tests; python -m unittest
