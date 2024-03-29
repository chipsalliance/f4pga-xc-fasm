// Copyright 2017-2022 F4PGA Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// SPDX-License-Identifier: Apache-2.0

module top(input clk, stb, di, output do);
	localparam integer DIN_N = 6;
	localparam integer DOUT_N = 1;

	reg [DIN_N-1:0] din;
	wire [DOUT_N-1:0] dout;

	reg [DIN_N-1:0] din_shr;
	reg [DOUT_N-1:0] dout_shr;

	always @(posedge clk) begin
		din_shr <= {din_shr, di};
		dout_shr <= {dout_shr, din_shr[DIN_N-1]};
		if (stb) begin
			din <= din_shr;
			dout_shr <= dout;
		end
	end

	assign do = dout_shr[DOUT_N-1];

	roi roi (
		.clk(clk),
		.din(din),
		.dout(dout)
	);
endmodule

module roi(input clk, input [5:0] din, output [0:0] dout);
    (* LOC="SLICE_X12Y102", BEL="A6LUT", KEEP, DONT_TOUCH *)
    LUT6 #(
        .INIT(64'h8000_DEAD_0000_0001)
    ) lutd (
        .I0(din[0]),
        .I1(din[1]),
        .I2(din[2]),
        .I3(din[3]),
        .I4(din[4]),
        .I5(din[5]),
        .O(dout[0]));
endmodule

