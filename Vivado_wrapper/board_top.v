`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company:
// Engineer:
//
// Create Date: 2026/10/07 14:58:50
// Design Name:
// Module Name: board_top
// Project Name:
// Target Devices:
// Tool Versions:
// Description:
//
// Dependencies:
//
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
//
//////////////////////////////////////////////////////////////////////////////////


module board_top(
    input [7:0] in,
    output led
    );

    generated_logic generated_logic(
        .A(in[0]),
        .B(in[1]),
        .C(in[2]),
        //.D(in[3]),
        //.E(in[4]),
        //.F(in[5]),
        //.G(in[6]),
        //.H(in[7]),
        .logic_out(led)
    );


endmodule
