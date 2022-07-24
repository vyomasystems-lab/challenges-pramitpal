# See LICENSE.iitm for details
# See LICENSE.vyoma for details

import random
import sys
import cocotb
from itertools import product

from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock

from model_mkbitmanip import *

def create_instr(func7,f3,opcode):
    return (func7<<25)|(f3<<12)|(opcode)

def create_test_instructions():
    opcode=[0b0110011,0b0010011]
    f3=[]
    f7=[]
    test_sequences=[]
    for i in range(pow(2,3)):
        f3.append(i)
    for i in range(pow(2,7)):
        f7.append(i)
    for each_opcode in opcode:
        for each_f3 in f3:
            for each_f7 in f7:
                # print(format(create_instr(each_f7,each_f3,each_opcode),'032b'))
                test_sequences.append(create_instr(each_f7,each_f3,each_opcode))
    return test_sequences

varied_instr_failed=[]
varied_input_failed=[]
instr=[]
# instr.append(create_instr(0b0000000,0b111,0b0110011))#AND* operation
# instr.append(create_instr(0b0000000,0b110,0b0110011))#OR* operation
# instr.append(create_instr(0b0000000,0b100,0b0110011))#XOR* operation
instr.append(create_instr(0b0100000,0b111,0b0110011))#ANDN operation======> error
instr.append(create_instr(0b0100000,0b110,0b0110011))#ORN operation
instr.append(create_instr(0b0100000,0b100,0b0110011))#XNORN operation

# instr.append(create_instr(0b0000000,0b001,0b0110011))#SLL* operation
# instr.append(create_instr(0b0000000,0b101,0b0110011))#SRL* operation
# instr.append(create_instr(0b0100000,0b101,0b0110011))#SRA* operation
instr.append(create_instr(0b0010000,0b001,0b0110011))#SLO operation
instr.append(create_instr(0b0010000,0b101,0b0110011))#SRO operation
instr.append(create_instr(0b0110000,0b001,0b0110011))#ROL operation
instr.append(create_instr(0b0110000,0b101,0b0110011))#ROR operation

instr.append(create_instr(0b0100100,0b001,0b0110011))#SBCLR operation
instr.append(create_instr(0b0010100,0b001,0b0110011))#SBSET operation
instr.append(create_instr(0b0110100,0b001,0b0110011))#SBINV operation
instr.append(create_instr(0b0100100,0b101,0b0110011))#SBEXT operation
instr.append(create_instr(0b0010100,0b101,0b0110011))#GORC operation
instr.append(create_instr(0b0110100,0b101,0b0110011))#GREV operation

# instr.append(create_instr(0b0000000,0b001,0b0010011))#SLLI* operation
# instr.append(create_instr(0b0000000,0b101,0b0010011))#SRLI* operation
# instr.append(create_instr(0b0100000,0b101,0b0010011))#SRAI* operation
instr.append(create_instr(0b0010000,0b001,0b0010011))#SLOI operation
instr.append(create_instr(0b0010000,0b101,0b0010011))#SROI operation
instr.append(create_instr(0b0110000,0b101,0b0010011))#RORI operation

instr.append(create_instr(0b0000011,0b001,0b0110011))#CMIX operation
instr.append(create_instr(0b0000011,0b101,0b0110011))#CMOV operation
instr.append(create_instr(0b0000010,0b001,0b0110011))#FSL operation
instr.append(create_instr(0b0000010,0b101,0b0110011))#FSR operation
instr.append(create_instr(0b0000010,0b101,0b0010011))#FSRI operation

# Clock Generation
@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(1) 
        signal.value <= 1
        yield Timer(1) 


# Sample Test
@cocotb.test()
def run_test_varied_instr(dut):

    f = open("test_varied_instr.log", "w")
    
    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    # input transaction
    # generate all combinations of instructions
    test_seq=create_test_instructions()

    error_counter=0
    passed_counter=0

    mav_putvalue_src1 = random.getrandbits(32)
    mav_putvalue_src2 = random.getrandbits(32)
    mav_putvalue_src3 = random.getrandbits(32)
    # mav_putvalue_instr = 0x101010B3
    
    for each_instr in test_seq:

        if each_instr !=create_instr(0b0100000,0b111,0b0110010):#excluding ANDN 

            mav_putvalue_instr=each_instr

            # expected output from the model
            expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

            # driving the input transaction
            dut.mav_putvalue_src1.value = mav_putvalue_src1
            dut.mav_putvalue_src2.value = mav_putvalue_src2
            dut.mav_putvalue_src3.value = mav_putvalue_src3
            dut.EN_mav_putvalue.value = 1
            dut.mav_putvalue_instr.value = mav_putvalue_instr
  
            yield Timer(1) 

            # obtaining the output
            dut_output = dut.mav_putvalue.value
            if dut_output != expected_mav_putvalue:
                if expected_mav_putvalue&1:

                    error_counter+=1
                    varied_instr_failed.append(each_instr) # append to list of failed instructions
                    f.write(f'\n{error_counter}. Failed instr: {hex(each_instr)}')
                    f.write(f' SRC_inp1 = {hex(mav_putvalue_src1)}, SRC_inp2 = {hex(mav_putvalue_src2)}, SRC_inp3 = {hex(mav_putvalue_src3)} ')
                    f.write(f'||DUT OUTPUT = {hex(dut_output)}, EXPECTED OUTPUT = {hex(expected_mav_putvalue)}')
                    cocotb.log.info("Failed instr={l}".format(l=hex(each_instr)))
                    cocotb.log.info(f'DUT OUTPUT     ={hex(dut_output)}')
                    cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
                    
            else:
                passed_counter+=1
 
    cocotb.log.info(f'PASSED Count={(passed_counter)}')
    f.close()
    # comparison
    # error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
    # assert dut_output == expected_mav_putvalue, error_message
    assert error_counter == 0, "Test Failed for {n} cases".format(n=error_counter)



def make_n_bitlist(n):
    l=[1<<i for i in range(n)]
    l.insert(0,0)
    return l

def make_src_inputs(n_bits):
    a=make_n_bitlist(n_bits)
    c = list(product(a,a,a))
    return c

@cocotb.test()
def run_test_varied_inputs(dut):

    f = open("test_varied_inputs.log", "w")
    src_inputs=make_src_inputs(32)
    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    # input transaction
    # generate all combinations of instructions

    error_counter=0
    passed_counter=0
    old_failed_instr=0   
    for each_instr in instr:#loop through all instructions from table

        for each_src_inputs in src_inputs:

            mav_putvalue_instr=each_instr
            cocotb.log.info(f'SRC_inp1={hex(each_src_inputs[0])},SRC_inp2={hex(each_src_inputs[1])},SRC_inp3={hex(each_src_inputs[2])}')
            # expected output from the model
            expected_mav_putvalue = bitmanip(mav_putvalue_instr, each_src_inputs[0], each_src_inputs[1], each_src_inputs[2])

            # driving the input transaction
            dut.mav_putvalue_src1.value = each_src_inputs[0]
            dut.mav_putvalue_src2.value = each_src_inputs[1]
            dut.mav_putvalue_src3.value = each_src_inputs[2]
            dut.EN_mav_putvalue.value = 1
            dut.mav_putvalue_instr.value = mav_putvalue_instr
  
            yield Timer(1) 

            # obtaining the output
            dut_output = dut.mav_putvalue.value

            if dut_output != expected_mav_putvalue:

                if expected_mav_putvalue&1:
                    error_counter+=1
                    varied_input_failed.append(each_instr) # append to list of failed instructions
                    
                    # LOGGING TO A LOG FILE
                    if each_instr == old_failed_instr:
                        f.write(f'\n\tSRC_inp1= {hex(each_src_inputs[0])}, SRC_inp2= {hex(each_src_inputs[1])}, SRC_inp3= {hex(each_src_inputs[2])}')
                        f.write(f'  ||DUT OUTPUT={hex(dut_output)}, EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
                    else:
                        f.write(f'\n{error_counter}. Failed instr: {hex(each_instr)}')
                        f.write(f'\n\tSRC_inp1= {hex(each_src_inputs[0])}, SRC_inp2= {hex(each_src_inputs[1])}, SRC_inp3= {hex(each_src_inputs[2])}')
                        f.write(f'  ||DUT OUTPUT={hex(dut_output)}, EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
                    # LOG FILE PART OVER

                    cocotb.log.info("Failed instr={l}".format(l=hex(each_instr)))
                    cocotb.log.info(f'DUT OUTPUT     ={hex(dut_output)}')
                    cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
                    old_failed_instr=each_instr
                    
            else:
                passed_counter+=1
        
    cocotb.log.info(f'PASSED Count={(passed_counter)}')
    f.close()
    # comparison
    # error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
    # assert dut_output == expected_mav_putvalue, error_message
    assert error_counter == 0, "Test Failed for {n} cases".format(n=error_counter)

