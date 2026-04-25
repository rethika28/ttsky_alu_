import cocotb
from cocotb.triggers import Timer

def alu_model(a, b, op):
    carry = 0

    if op == 0:  # ADD
        tmp = a + b
        carry = (tmp >> 2) & 1
        res = tmp & 0b11

    elif op == 1:  # SUB
        tmp = (a - b) & 0b111
        carry = (tmp >> 2) & 1
        res = tmp & 0b11

    elif op == 2: res = a & b
    elif op == 3: res = a | b
    elif op == 4: res = a ^ b
    elif op == 5: res = (~a) & 0b11
    elif op == 6: res = (a << 1) & 0b11
    elif op == 7: res = (a >> 1) & 0b11

    return res, carry


@cocotb.test()
async def test_alu(dut):

    # Initialize
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.ena.value = 1
    dut.clk.value = 0
    dut.rst_n.value = 1

    await Timer(1, units="ns")

    for op in range(8):
        for a in range(4):
            for b in range(4):

                dut.ui_in.value = (op << 4) | (b << 2) | a
                await Timer(1, units="ns")

                out = dut.uo_out.value.integer
                result = out & 0b11
                carry  = (out >> 2) & 1

                exp_res, exp_carry = alu_model(a, b, op)

                assert result == exp_res, f"Result FAIL op={op} a={a} b={b}"
                assert carry == exp_carry, f"Carry FAIL op={op} a={a} b={b}"

    dut._log.info("All ALU tests passed ✅")
