<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

The ALU takes two 2-bit inputs a and b, and a 3-bit control signal op.
Based on the opcode, it performs different operations such as addition, subtraction, AND, OR, XOR, NOT, and shift operations.

The result and carry are given as outputs.

🔹 Inputs
ui_in[1:0] → a
ui_in[3:2] → b
ui_in[6:4] → opcode
🔹 Outputs
uo_out[1:0] → result
uo_out[2] → carry
🔹 Operations
Opcode	Operation
000	ADD
001	SUB
010	AND
011	OR
100	XOR
101	NOT
110	Shift Left
111	Shift Right

## How to test



ui_in = (op << 4) | (b << 2) | a

Example:

a = 2, b = 1, op = 000 (ADD)
Output → result = 3, carry = 0

## External hardware

no external hardware used 
