import random
import sys
import cocotb
from pathlib import Path
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock
from cocotb.binary import BinaryValue
import os
import operator


# Clock Generation
@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(5) 
        signal.value <= 1
        yield Timer(5)

@cocotb.test()
async def test(dut):
    passed_testcases = 0
    await Timer(1, units = 'ns')
   

    cocotb.fork(clock_gen(dut.clk))
    cocotb.log.info('Hey Master send data to slave1')
    

    dut.MODE.value = 0b01
    input_vector = 0b10101010
    input_vector1 = 0b11100111
    dut.data_in_to_master.value =input_vector
    dut.data_in_slave1.value =input_vector1
    
    await Timer(1)
    cocotb.log.info(f'Current data in Master={(dut.data_in_to_master.value)}')
    cocotb.log.info(f'Current data in slave1={(dut.data_in_slave1.value)}')
    cocotb.log.info(f'expected data output from Master={bin(input_vector1)}')
    cocotb.log.info(f'expected data output from slave={bin(input_vector)}')
    
    await Timer(10, units = 'ns')
    dut.reset.value=0b0
    await Timer(10, units = 'ns')
    dut.CS.value=0b01
    await Timer(1)
    cocotb.log.info(f'cs1bar = {(dut.CS1bar)}')
    dut.RW.value=0b11
    await Timer(110, units = 'ns') 

 
    cocotb.log.info(f'exact output data from master={(dut.data_out_from_master.value)} and exact output data from slave1 ={(dut.data_out_slave1.value)}');
     
    if(({bin(dut.data_out_from_master.value)} == input_vector1) and ({bin(dut.data_out_slave1.value)} == input_vector)):
        cocotb.log.info(" testcase #1 is passed successfuly")
        print("//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//")
        passed_testcases=passed_testcases+1
    else:
        cocotb.log.info("testcase #1 is failed")
    
    #cocotb.fork(testcase1(dut, dut.clk, input_vector, input_vector1, input_vector1, input_vector))
    dut._log.info("dut.data_into_master = %d data_in_slave1 = %d, expected master output = %d, actualdata_out_from_master = %d, expected_slave1_output = %d, dut.data_out_slave1= %d", dut.data_in_to_master.value, dut.data_in_slave1.value, input_vector1, dut.data_out_from_master.value, input_vector, dut.data_out_slave1.value) 
    assert passed_testcases==1,"FAILED"   	