`include "Master.v"
`include "slave.v"
`timescale 1ns / 1ps
module Spi_Protocol(clk, reset, data_in_to_master, data_out_from_master, data_in_slave1, data_in_slave2, data_in_slave3, data_out_slave1, data_out_slave2,data_out_slave3, CS, RW, MODE);
  
  input clk;
  input reset;

  input [7:0] data_in_to_master;
  output wire [7:0] data_out_from_master;

  input  [7:0] data_in_slave1;
  input  [7:0] data_in_slave2;
  input  [7:0] data_in_slave3;

  output wire [7:0] data_out_slave1;
  output wire [7:0] data_out_slave2;
  output wire [7:0] data_out_slave3;

  input    [1:0]CS;
  input    [1:0]RW;
  input    [1:0]MODE;

  wire MOSI;
  wire MISO;
  wire MISO1;
  wire MISO2;
  wire MISO3;

  wire CS1bar;
  wire CS2bar;
  wire CS3bar;

  wire sclk;
  wire sreset;
  wire[1:0]sMODE;

  SPI_Master  MSTR
  (.clk(clk),
   .reset(reset),
   .MODE(MODE),
   .MISO(MISO),
   .MOSI(MOSI),

   .sclk(sclk),
   .sreset(sreset),
   .sMODE,

   .CS(CS),
   .RW(RW),

   .data_in(data_in_to_master),
   .data_out(data_out_from_master),

   .CS1bar(CS1bar),
   .CS2bar(CS2bar),
   .CS3bar(CS3bar)
  );
  
  slave SLV_1
  (
    .MODE(sMODE),
    .data_in(data_in_slave1),
    .reset(sreset),
    .clk(sclk),
    .MOSI(MOSI),
    .MISO(MISO1),
    .CS(CS1bar),
    .data_out(data_out_slave1)
   );
  
  slave SLV_2
  (
    .MODE(sMODE),
    .data_in(data_in_slave2),
    .reset(sreset),
    .clk(sclk),
    .MOSI(MOSI),
    .MISO(MISO2),
    .CS(CS2bar),
    .data_out(data_out_slave2)
    );
  
  slave SLV_3
  (
    .MODE(sMODE),
    .data_in(data_in_slave3),
    .reset(sreset),
    .clk(sclk),
    .MOSI(MOSI),
    .MISO(MISO3),
    .CS(CS3bar),
    .data_out(data_out_slave3)
  );
  assign MISO =(CS1bar==0)?MISO1:
             (CS2bar==0)?MISO2:
             (CS3bar==0)?MISO3:1'bx;

endmodule