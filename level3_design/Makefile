# See LICENSE.vyoma for details

TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)

VERILOG_SOURCES = $(PWD)/Spi_Protocol.v             # provide your design path

TOPLEVEL := Spi_Protocol           # design file
MODULE   := test_spi_protocol   # test file

include $(shell cocotb-config --makefiles)/Makefile.sim

clean_all: clean
	rm -rf *.xml sim_build __pycache__ 
