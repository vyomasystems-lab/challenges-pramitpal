# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path
import uuid
import re
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge


@cocotb.test()
async def test_seq_bug1(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)


    test_sequence='11111111011000010101111011'
    # test_sequence='11011' # only this sequence is failing
    # test_sequence='101011' # also failing
    # cocotb.log.info('####Fixed Test Sequence={x} ######'.format(x=test_sequence))

    expected_output=[]
    expected_output_str=''
    output=[]
    output_str=''
    # get indexes of 1011 in test sequence
    index=[m.start() for m in re.finditer('(?=1011)',test_sequence)] #with overlap return indexes 

    # get expected output
    for i in range(len(test_sequence)):
            if i-3 in index:
                expected_output.append(1)    
            else:
                expected_output.append(0)

    # convert expected output to a string
    expected_output_str=''.join(map(str, expected_output))

    #loop through each bit in test_sequence
    for i in range(len(test_sequence)):
        dut.inp_bit.value=int(test_sequence[i])
        await FallingEdge(dut.clk)
        output.append(dut.seq_seen.value.integer)

    # convert output to a string
    output_str=''.join(map(str, output))

    # DEBUGGING PART---------------------------
    # cocotb.log.info('output expected={x}, output got={y}'.format(x=expected_output_str,y=output_str))
    assert output_str==expected_output_str,'Expected Output is not same as Output'
 
@cocotb.test()
async def random_test_seq_bug1(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    # Create random test sequence
    n=uuid.uuid1().int*198
    s=format(n, '0128b')
    test_sequence=s

    # cocotb.log.info('####Random Test Sequence={x} ######'.format(x=test_sequence))

    expected_output=[]
    expected_output_str=''
    output=[]
    output_str=''
    # get indexes of 1011 in test sequence
    index=[m.start() for m in re.finditer('(?=1011)',test_sequence)] #with overlap return indexes 

    # get expected output
    for i in range(len(test_sequence)):
            if i-3 in index:
                expected_output.append(1)    
            else:
                expected_output.append(0)

    # convert expected output to a string
    expected_output_str=''.join(map(str, expected_output))

    #loop through each bit in test_sequence
    for i in range(len(test_sequence)):
        dut.inp_bit.value=int(test_sequence[i])
        await FallingEdge(dut.clk)
        output.append(dut.seq_seen.value.integer)

    # convert output to a string
    output_str=''.join(map(str, output))

    # DEBUGGING PART---------------------------
    # cocotb.log.info('output expected={x}, output got={y}'.format(x=expected_output_str,y=output_str))
    assert output_str==expected_output_str,'Expected Output is not same as Output'
    

                