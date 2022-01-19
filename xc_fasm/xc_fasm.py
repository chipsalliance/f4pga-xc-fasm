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

import argparse
import subprocess
import os
import tempfile

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
    parser.add_argument(
        '--frm2bit', default="xc7frames2bit", help="xc7frames2bit tool.")
    parser.add_argument('--fn_in', help='Input FPGA assembly (.fasm) file')
    parser.add_argument('--bit_out', help='Output FPGA bitstream (.bit) file')
    parser.add_argument(
        '--frm_out', default=None, help='Output FPGA frame (.frm) file')

    args = parser.parse_args()

    frm_out = args.frm_out
    if frm_out is None:
        _, frm_out = tempfile.mkstemp()

    f_out = open(frm_out, 'w')
    fasm2frames(
        db_root=args.db_root,
        part=args.part,
        filename_in=args.fn_in,
        f_out=f_out,
        sparse=args.sparse,
        roi=args.roi,
        debug=args.debug,
        emit_pudc_b_pullup=args.emit_pudc_b_pullup)
    f_out.close()

    result = subprocess.check_output(
        "{} --frm_file {} --output_file {} --part_name {} --part_file {}".
        format(args.frm2bit, frm_out, args.bit_out, args.part, args.part_file),
        shell=True)


if __name__ == '__main__':
    main()
