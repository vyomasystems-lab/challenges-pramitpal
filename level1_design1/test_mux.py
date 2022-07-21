# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import uuid

@cocotb.test()
async def random_test_mux(dut):
    """Randomized Test for mux2"""
    cocotb.log.info("RANDOM VALUE TEST")
    n=uuid.uuid1().int>>64
    s=format(n, '064b')
    chunk, chunk_size = len(s), 2
    inputs=[ int(s[i:i+chunk_size],2) for i in range(0, chunk, chunk_size) ]

    # -----------------
    dut.inp0.value=inputs[0]
    dut.inp1.value=inputs[1]
    dut.inp2.value=inputs[2]
    dut.inp3.value=inputs[3]
    dut.inp4.value=inputs[4]
    dut.inp5.value=inputs[5]
    dut.inp6.value=inputs[6]
    dut.inp7.value=inputs[7]
    dut.inp8.value=inputs[8]
    dut.inp9.value=inputs[9]
    dut.inp10.value=inputs[10]
    dut.inp11.value=inputs[11]
    dut.inp12.value=inputs[12]
    dut.inp13.value=inputs[13]
    dut.inp14.value=inputs[14]
    dut.inp15.value=inputs[15]
    dut.inp16.value=inputs[16]
    dut.inp17.value=inputs[17]
    dut.inp18.value=inputs[18]
    dut.inp19.value=inputs[19]
    dut.inp20.value=inputs[20]
    dut.inp21.value=inputs[21]
    dut.inp22.value=inputs[22]
    dut.inp23.value=inputs[23]
    dut.inp24.value=inputs[24]
    dut.inp25.value=inputs[25]
    dut.inp26.value=inputs[26]
    dut.inp27.value=inputs[27]
    dut.inp28.value=inputs[28]
    dut.inp29.value=inputs[29]
    dut.inp30.value=inputs[30]
    await Timer(2, units='ns')
    error_count=0;
    for i in range(31):
        dut.sel.value=i
        await Timer(2, units='ns')
            # print(dut.out.value.integer)
        if(dut.out.value!=inputs[i]):
            cocotb.log.info("ERROR!! for Sel= {sel},input={inp}--output={out}, is not correct".format(sel=dut.sel.value.integer,inp=inputs[i],out=dut.out.value.integer))
            error_count+=1
        # else:
            # cocotb.log.info("testing for sel line {sel} input={inp}--output={out} ..ok".format(sel=i,inp=inputs[i],out=dut.out.value.integer))
    assert error_count == 0, "There are {c} errors.".format(c=error_count)


@cocotb.test()
async def fixed_test_mux(dut):
    """Randomized Test for mux2"""
    cocotb.log.info("FIXED VALUE TEST")
    n=2
    # -----------------
    dut.inp0.value=n
    dut.inp1.value=n
    dut.inp2.value=n
    dut.inp3.value=n
    dut.inp4.value=n
    dut.inp5.value=n
    dut.inp6.value=n
    dut.inp7.value=n
    dut.inp8.value=n
    dut.inp9.value=n
    dut.inp10.value=n
    dut.inp11.value=n
    dut.inp12.value=n
    dut.inp13.value=n
    dut.inp14.value=n
    dut.inp15.value=n
    dut.inp16.value=n
    dut.inp17.value=n
    dut.inp18.value=n
    dut.inp19.value=n
    dut.inp20.value=n
    dut.inp21.value=n
    dut.inp22.value=n
    dut.inp23.value=n
    dut.inp24.value=n
    dut.inp25.value=n
    dut.inp26.value=n
    dut.inp27.value=n
    dut.inp28.value=n
    dut.inp29.value=n
    dut.inp30.value=n
    await Timer(2, units='ns')
    error_count=0;
    for i in range(31):
        dut.sel.value=i
        await Timer(2, units='ns')
            # print(dut.out.value.integer)
        if(dut.out.value!=n):
            cocotb.log.info("ERROR!! for Sel= {sel},input={inp}--output={out}, is not correct".format(sel=dut.sel.value.integer,inp=n,out=dut.out.value.integer))
            error_count+=1
        # else:
            # cocotb.log.info("testing for sel line {sel} input={inp}--output={out} ..ok".format(sel=i,inp=n,out=dut.out.value.integer))
    assert error_count == 0, "There are {c} errors.".format(c=error_count)
  
        
