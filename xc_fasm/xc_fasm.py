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

import argparse
import subprocess
import os

from prjxray import util
from .fasm2frames import fasm2frames


def main():
    parser = argparse.ArgumentParser(
        description=
        'Convert FPGA configuration description ("FPGA assembly") into binary frame equivalent'
    )

    util.db_root_arg(parser)
    util.part_arg(parser)
    parser.add_argument('--part_file', required=True, help="Part YAML file.")
    parser.add_argument(
        '--sparse', action='store_true', help="Don't zero fill all frames")
    parser.add_argument(
        '--roi',
        help="ROI design.json file defining which tiles are within the ROI.")
    parser.add_argument(
        '--emit_pudc_b_pullup',
        help="Emit an IBUF and PULLUP on the PUDC_B pin if unused",
        action='store_true')
    parser.add_argument(
        '--debug', action='store_true', help="Print debug dump")
    parser.add_argument('--fn_in', help='Input FPGA assembly (.fasm) file')
    parser.add_argument('--bit_out', help='Output FPGA bitstream (.bit) file')
    parser.add_argument(
        '--frm_out',
        default='/dev/stdout',
        nargs='?',
        help='Output FPGA frame (.frm) file')

    args = parser.parse_args()
    fasm2frames(
        db_root=args.db_root,
        part=args.part,
        filename_in=args.fn_in,
        f_out=open(args.frm_out, 'w'),
        sparse=args.sparse,
        roi=args.roi,
        debug=args.debug,
        emit_pudc_b_pullup=args.emit_pudc_b_pullup)

    result = subprocess.check_output(
        "xc7frames2bit --frm_file {} --output_file {} --part_name {} --part_file {}"
        .format(args.frm_out, args.bit_out, args.part, args.part_file),
        shell=True)


if __name__ == '__main__':
    main()
