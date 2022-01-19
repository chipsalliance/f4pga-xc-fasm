#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2017-2022 F4PGA Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
'''
Take bitstream .bit files and decode them to FASM.
'''

import argparse
import contextlib
import os
import subprocess
import sys
import tempfile

import fasm
import fasm.output
from prjxray import fasm_disassembler, bitstream, util
from prjxray.db import Database


def bit_to_bits(bitread, part_yaml, bit_file, bits_file, frame_range=None):
    """ Calls bitread to create bits (ASCII) from bit file (binary) """
    if frame_range:
        frame_range_arg = '-F {}'.format(frame_range)
    else:
        frame_range_arg = ''

    subprocess.check_output(
        '{} --part_file {} {} -o {} -z -y {}'.format(
            bitread, part_yaml, frame_range_arg, bits_file, bit_file),
        shell=True)


def bits_to_fasm(db_root, part, bits_file, verbose, canonical, fasm_file):
    db = Database(db_root, part)
    grid = db.grid()
    disassembler = fasm_disassembler.FasmDisassembler(db)

    with open(bits_file) as f:
        bitdata = bitstream.load_bitdata(f)

    model = fasm.output.merge_and_sort(
        disassembler.find_features_in_bitstream(bitdata, verbose=verbose),
        zero_function=disassembler.is_zero_feature,
        sort_key=grid.tile_key,
    )

    print(
        fasm.fasm_tuple_to_string(model, canonical=canonical),
        end='',
        file=fasm_file)


def main():

    parser = argparse.ArgumentParser(
        description='Convert 7-series bit file to FASM.')

    util.db_root_arg(parser)
    util.part_arg(parser)
    parser.add_argument(
        '--bits-file',
        help="Output filename for bitread output (default: tempfile)",
        default=None)
    parser.add_argument(
        '--bitread', help="Name of part being targetted", default='bitread')
    parser.add_argument(
        '--frame_range', help="Frame range to use with bitread.")
    parser.add_argument('bit_file', help='Input bitstream file')
    parser.add_argument(
        '--verbose',
        help='Print lines for unknown tiles and bits',
        action='store_true')
    parser.add_argument(
        '--canonical', help='Output canonical bitstream.', action='store_true')
    parser.add_argument(
        '--fasm_file',
        type=argparse.FileType('w'),
        help='Output FASM file',
        default=sys.stdout)

    args = parser.parse_args()

    with contextlib.ExitStack() as stack:
        if args.bits_file:
            bits_file = stack.enter_context(open(args.bits_file, 'wb'))
        else:
            bits_file = stack.enter_context(tempfile.NamedTemporaryFile())

        bit_to_bits(
            bitread=args.bitread,
            part_yaml=os.path.join(args.db_root, args.part, "part.yaml"),
            bit_file=args.bit_file,
            bits_file=bits_file.name,
            frame_range=args.frame_range,
        )

        bits_to_fasm(args.db_root, args.part, bits_file.name, args.verbose,
                     args.canonical, args.fasm_file)


if __name__ == '__main__':
    main()
