`default_nettype none

module tt_um_alu (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    // Inputs
    wire [1:0] a  = ui_in[1:0];
    wire [1:0] b  = ui_in[3:2];
    wire [2:0] op = ui_in[6:4];

    // Internal signals
    reg [1:0] result;
    reg carry;

    always @(*) begin
        result = 2'b00;
        carry  = 1'b0;

        case (op)
            3'b000: {carry, result} = a + b; // ADD

            3'b001: begin                   // SUB (fixed)
                {carry, result} = {1'b0, a} - {1'b0, b};
            end

            3'b010: result = a & b;         // AND
            3'b011: result = a | b;         // OR
            3'b100: result = a ^ b;         // XOR
            3'b101: result = ~a;            // NOT
            3'b110: result = (a << 1) & 2'b11; // SHIFT LEFT
            3'b111: result = (a >> 1);      // SHIFT RIGHT
        endcase
    end

    // Single assignment (lint-safe)
    assign uo_out = {5'b00000, carry, result};

    // Unused IO
    assign uio_out = 8'b00000000;
    assign uio_oe  = 8'b00000000;

    wire _unused = &{ena, clk, rst_n, uio_in, 1'b0};

endmodule
