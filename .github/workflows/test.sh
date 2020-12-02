#!/bin/bash

make test-py
test $(git status --porcelain | wc -l) -eq 0 || { git diff; false; }
