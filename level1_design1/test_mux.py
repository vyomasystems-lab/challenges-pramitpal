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
    # print (type(inputs[0]))   
    # -----------------
    dut.inp0.value=2
    dut.inp1.value=2
    dut.inp2.value=2
    dut.inp3.value=2
    dut.inp4.value=2
    dut.inp5.value=2
    dut.inp6.value=2
    dut.inp7.value=2
    dut.inp8.value=2
    dut.inp9.value=2
    dut.inp10.value=2
    dut.inp11.value=2
    dut.inp12.value=2
    dut.inp13.value=2
    dut.inp14.value=2
    dut.inp15.value=2
    dut.inp16.value=2
    dut.inp17.value=2
    dut.inp18.value=2
    dut.inp19.value=2
    dut.inp20.value=2
    dut.inp21.value=2
    dut.inp22.value=2
    dut.inp23.value=2
    dut.inp24.value=2
    dut.inp25.value=2
    dut.inp26.value=2
    dut.inp27.value=2
    dut.inp28.value=2
    dut.inp29.value=2
    dut.inp30.value=2
    await Timer(2, units='ns')
    i=28
    dut.sel.value=i
    await Timer(2, units='ns')
    print(dut.out.value.integer)
    # cocotb.log.info(dut.out.value == 2, "Output not match {OUT}".format(OUT=int(dut.out.value)))
    assert dut.out.value == 2, "Output not match {OUT}".format(OUT=dut.out.value.integer)
    # print("Output not match {OUT}".format(OUT=2))
        
