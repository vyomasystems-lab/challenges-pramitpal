# See LICENSE.vyoma for details

import random
import sys
import cocotb
from itertools import product

from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge,FallingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock

# Clock Generation
@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(1) 
        signal.value <= 1
        yield Timer(1) 

async def get_signal(clk, signal):
    await RisingEdge(clk)
    return signal.value

@cocotb.test()
async def test_counter_block(dut):
    """Test for mux2"""

    # clock
    clock = Clock(dut.ct.clk, 10, units="ns")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())  # Start the clock

    before_reset=dut.ct.count.value
    # reset the counter to start
    await RisingEdge(dut.ct.clk)
    dut.ct.reset.value = 1
    await RisingEdge(dut.ct.clk)
    dut.ct.reset.value = 0
    await RisingEdge(dut.ct.clk)
    first=dut.ct.count.value
    await RisingEdge(dut.ct.clk)
    second=dut.ct.count.value
    await RisingEdge(dut.ct.clk)
    third=dut.ct.count.value

    cocotb.log.info('##### Counter Test ########')

    reset_ok=0
    counter_ok=0
    errors=0
    if first == 0:
        reset_ok=1
        cocotb.log.info('Counter Reset OK')
    else:
        errors+=1
        cocotb.log.info('Counter Reset-- ERROR')
    if second-1==first and third-1==second:
        counter_ok=1
        cocotb.log.info('Increment counting OK')
    else:
        errors+=1
        cocotb.log.info('Decrement counting-- ERROR')

    assert errors == 0, f'There are {errors} faults, in Counter Module'

@cocotb.test()
async def test_input_capture_module(dut):
    """Test for mux2"""
    errors=0
    # clock
    clock = Clock(dut.ct.clk, 10, units="ns")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())  # Start the clock

    # checking input capture
    InterruptFlag_before_signal = dut.intFlag.value
    await RisingEdge(dut.ct.clk)
    dut.sig.value = 1
    await Timer(1) 
    current_count=dut.ct.count.value
    current_sig_val=dut.val.value
    InterruptFlag_after_signal = dut.intFlag.value
    await RisingEdge(dut.ct.clk)
    dut.sig.value = 0
    
    if current_count.binstr != current_sig_val.binstr:
        cocotb.log.info('Signal input Capture fault-- ERROR')
        errors+=1
    else: cocotb.log.info('Signal input Capture --OK')
    # print(f'{current_count.binstr},{current_sig_val.binstr}')
    # -----------------------

    # checking Val register reset
    await RisingEdge(dut.clk)
    dut.rstVal.value=1
    await Timer(1) 
    after_rstVal_reset=dut.val.value
    if after_rstVal_reset.value !=0:
        errors+=1
        cocotb.log.info('Val Register reset fault-- ERROR')
    else:
        cocotb.log.info('Val Register reset -- OK')
    #-----------------------------------

    # checking Interrupt Flag
    if InterruptFlag_before_signal ==0 and InterruptFlag_after_signal ==1:
        cocotb.log.info('Interrupt Flag functioning -- OK')
    else:
        cocotb.log.info('Interrupt Flag functioning fault -- ERROR')
        errors+=1
    # ----------------------

    # checking Interrupt Flag Reset
    await RisingEdge(dut.clk)
    dut.rstIntFlag.value=1
    await Timer(1)
    InterruptFlag_after_signal_after_reset=dut.intFlag.value

    if InterruptFlag_after_signal_after_reset ==0 :
        cocotb.log.info('Interrupt Flag Reset functioning -- OK')
    else:
        cocotb.log.info('Interrupt Flag Reset functioning -- ERROR')
        errors+=1
    # ----------------------

    assert errors ==0,f'There are {errors} faults for Signal Input Capture'

