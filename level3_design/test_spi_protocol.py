import random
import sys
import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock

# Clock Generation
@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(5) 
        signal.value <= 1
        yield Timer(5)

@cocotb.coroutine
async def testcase1(dut,input_vector, expected_vector, input_vector1, expected_vector1): 
    cocotb._log.info('Hey Master send data to slave1')
    cocotb.start(clock_gen(dut.clk))
    dut.reset= 0b1 
    dut.MODE= 0b01
    dut.data_in_to_master=input_vector;
    dut.data_in_slave1=input_vector1;
    cocotb.log.info(f'Current data in Master ={bin(dut.data_in_to_master)}')
	cocotb.log.info(f'current data in slave = {bin(dut.data_in_slave1)}')
	cocotb.log.info(f'expected data output from Master ={bin(expected_vector1)}')
    cocotb.log.info(f'expected data output from slave = {bin(expected_vector)}')
    
    await Timer(10, units = 'ns')
    dut.reset=0b0;
    await Timer(10, units = 'ns')
    dut.CS=0b01;
    dut.RW=0b11;
    
    await Timer(100, units = 'ns') 
    dut.CS=0b00;
 
    

@cocotb.test()
async def test(dut):
    passed_testcases = 0
    await Timer(1, units = 'ns')
    task1 = cocotb.start_soon(testcase1(input_vector,input_vector1, input_vector1,input_vector))
    cocotb.log.info(f'exact output data from master={bin(dut.data_out_from_master)}, exact output data from slave1 ={bin(dut.data_out_slave1)}');

	if ((data_out_from_master==expected_vector1)&&(data_out_slave1==expected_vector)):
        coctb.log.info(" testcase #1 is passed successfuly");
        print("//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//");
	    passed_testcases=passed_testcases+1;
assert passed_testcases == 1,"FAILED"	