#!/bin/bash

set -ex

make format
test $(git status --porcelain | wc -l) -eq 0 || { git diff; false; }
