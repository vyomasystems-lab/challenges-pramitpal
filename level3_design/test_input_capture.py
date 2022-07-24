# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_input_capture(dut):
    """Test for mux2"""

    cocotb.log.info('##### CTB: Develop your test here ########')