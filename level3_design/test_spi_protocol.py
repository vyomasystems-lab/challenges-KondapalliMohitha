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



@cocotb.test()
async def test(dut):
    passed_testcases = 0
    await Timer(1, units = 'ns')
   

    clock = Clock(dut.clk, 5, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start()) 
    cocotb.log.info('Hey Master send data to slave1')
    
    dut.reset.value = 0b0
    dut.MODE.value = 0b01
    input_vector = 0b10101010
    input_vector1 = 0b11100111
    input_vector2 = 0b11100111
    input_vector3 = 0b11100111
    dut.data_in_to_master.value =input_vector
    dut.data_in_slave1.value =input_vector1
    dut.data_in_slave2.value =input_vector2
    dut.data_in_slave3.value =input_vector3
    await Timer(1)
    cocotb.log.info(f'Current data in Master={(dut.data_in_to_master.value)}')
    cocotb.log.info(f'Current data in slave1={(dut.data_in_slave1.value)}')
    cocotb.log.info(f'expected data output from Master={bin(input_vector1)}')
    cocotb.log.info(f'expected data output from slave={bin(input_vector)}')
    
    
    await Timer(9, units = 'ns')
    dut.CS.value=0b01
    dut.RW.value=0b11
    await Timer(1)
    cocotb.log.info(f'clk = {dut.clk.value},cs1bar = {dut.CS1bar.value}')
    
    await Timer(200, units = 'ns') 
    cocotb.log.info(f'RX_temp_byte= {dut.MSTR.RX_temp_byte}, rx_done in master = {dut.MSTR.RX_done.value}')
    cocotb.log.info(f'clk = {dut.clk.value},exact output data from master={(dut.MSTR.data_out.value)} and exact output data from slave1 ={(dut.SLV_1.data_out.value)}');
    """
    if((dut.data_out_from_master.value == input_vector1) and (dut.data_out_slave1.value == input_vector)):
        cocotb.log.info(" testcase #1  passed successfuly")
        passed_testcases=passed_testcases+1
    else:
        cocotb.log.info("testcase #1 failed")
    
    #cocotb.fork(testcase1(dut, dut.clk, input_vector, input_vector1, input_vector1, input_vector))
    dut._log.info("dut.data_into_master = %d data_in_slave1 = %d, expected master output = %d, actualdata_out_from_master = %d, expected_slave1_output = %d, dut.data_out_slave1= %d", dut.data_in_to_master.value, dut.data_in_slave1.value, input_vector1, dut.data_out_from_master.value, input_vector, dut.data_out_slave1.value) 
    assert passed_testcases==1,"FAILED"   	
    """