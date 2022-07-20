# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""
    # -----------
    module = dut
    inputs = [attr for attr in dir(module) if not callable(getattr(module, attr)) and attr.startswith("inp")]
    sel_lines = [attr for attr in dir(module) if not callable(getattr(module, attr)) and attr.startswith("sel")]
    outputs = [attr for attr in dir(module) if not callable(getattr(module, attr)) and attr.startswith("out")]
    print (outputs)   
    # -----------------
    
    cocotb.log.info('##### CTB: Develop your test here ########')
