import cocotb
from cocotb.triggers import Timer

def alu_model(a, b, op):
    """Reference model"""
    carry = 0
    if op == 0:   # ADD
        tmp = a + b
        carry = (tmp >> 2) & 1
        res = tmp & 0b11
    elif op == 1: # SUB
        tmp = (a - b) & 0b111  # keep 3 bits for borrow
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
    """Test all ALU operations"""

    # Initialize signals
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.ena.value = 1
    dut.clk.value = 0
    dut.rst_n.value = 1

    await Timer(1, units="ns")

    # Loop through all combinations
    for op in range(8):
        for a in range(4):
            for b in range(4):

                # Pack inputs
                ui_val = (op << 4) | (b << 2) | a
                dut.ui_in.value = ui_val

                await Timer(1, units="ns")

                # Read output
                out = dut.uo_out.value.integer
                result = out & 0b11
                carry  = (out >> 2) & 1

                # Expected
                exp_res, exp_carry = alu_model(a, b, op)

                dut._log.info(
                    f"op={op} a={a} b={b} -> res={result} carry={carry}"
                )

                assert result == exp_res, f"Result FAIL op={op} a={a} b={b}"
                assert carry == exp_carry, f"Carry FAIL op={op} a={a} b={b}"

    dut._log.info("All ALU tests passed ✅")
