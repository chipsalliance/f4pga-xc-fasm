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
    parser.add_argument(
        '--partial_bitstream',
        action="store_true",
        help='Generate partial bitstream')

    args = parser.parse_args()

    frm_out = args.frm_out
    if frm_out is None:
        _, frm_out = tempfile.mkstemp()

    emit_pudc_b_pullup = args.emit_pudc_b_pullup and not args.partial_bitstream

    f_out = open(frm_out, 'w')
    cfg = fasm2frames(
        db_root=args.db_root,
        part=args.part,
        filename_in=args.fn_in,
        f_out=f_out,
        sparse=args.sparse,
        roi=args.roi,
        debug=args.debug,
        emit_pudc_b_pullup=emit_pudc_b_pullup)
    f_out.close()

    frm2bit_args = "{} --frm_file {} --output_file {} --part_name {}" \
                   " --part_file {}".format(args.frm2bit, frm_out,
                                           args.bit_out, args.part,
                                           args.part_file)

    if args.partial_bitstream:
        clb_io_clk_blocks = cfg.clb_start_address is not None and \
                            cfg.clb_end_address is not None
        bram_blocks = cfg.bram_start_address is not None and \
                      cfg.bram_end_address is not None
        frm2bit_args += " --partial_bitstream"
        if clb_io_clk_blocks:
            frm2bit_args += " --clb_start_addr {}".format(
                cfg.clb_start_address)
            frm2bit_args += " --clb_end_addr {}".format(cfg.clb_end_address)
        if bram_blocks:
            frm2bit_args += " --bram_start_addr {}".format(
                cfg.bram_start_address)
            frm2bit_args += " --bram_end_addr {}".format(cfg.bram_end_address)

    result = subprocess.check_output(frm2bit_args, shell=True)


if __name__ == '__main__':
    main()
