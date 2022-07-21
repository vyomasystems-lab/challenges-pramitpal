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

def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

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

    cocotb.log.info('#### CTB: Develop your test here! ######')

    seq='1011'
    sequences=[]
    for n in range(16):
        s=format(n, '04b')
        for m in range(16):
            s2=format(m, '04b')
            # print(s2+seq+s)
            sequences.append(s2+seq+s)

    
    output_seq=[]
    output_seq_expected=[]
    fail_count=0
    for check_sequence in sequences:
    # for jj in range(10):
        # check_sequence=sequences[jj]
        index=[m.start() for m in re.finditer('(?=1011)',check_sequence)] #with overlap return indexes 
        output_seq.clear()
        
        for i in range(len(check_sequence)):
            
            dut.inp_bit.value=int(check_sequence[i])
            await FallingEdge(dut.clk)
            output_seq.append(dut.seq_seen.value.integer)
            # cocotb.log.info('{ss}'.format(ss=dut.seq_seen.value.integer))
            # if i not in index: #non 1011 sequence
        output_seq_expected.clear()
        for iii in range(len(check_sequence)):
            if iii-3 in index:
                output_seq_expected.append(1)    
            else:
                output_seq_expected.append(0)   
        cocotb.log.info('random sequence= {ss},output={p},expected= {iii},indexes= {ii}'.format(iii=''.join(map(str, output_seq_expected)),ii=index,ss=check_sequence,p=''.join(map(str, output_seq))))
        if ''.join(map(str, output_seq_expected)) == ''.join(map(str, output_seq)):
            cocotb.log.info('passed')
        else:
            cocotb.log.info('failed')
            fail_count+=1
        # cocotb.log.info('expected= {ii}'.format())
    assert fail_count==0,'Failed with {x} errors'.format(x=fail_count)

                