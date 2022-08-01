module SPI_Master // Mode 0 -> CPOL=0,CPHA=0 -> data sampled on rising edge and shifted on falling edge, leading edge is the rising edge
 // default value is MODE=0
// MODE|CPOL | CPHA  | data sampled on ...edge  | data shifted out on ... edge
// 0   | 0   |	0    |		Rising		|	Falling
// 1   | 0   |	1    |		Falling		|	Rising
// 2   | 1   |	0    |		Falling		|	Rising
// 3   | 1   |	1    |		Rising		|	Falling
  (clk,reset, MISO, MOSI, CS1bar, CS2bar, CS3bar, sclk, sreset, sMODE, data_in, data_out, CS, RW, MODE);
  
  input clk,reset;
  input [1:0]MODE;

	input MISO;
	output reg MOSI;
	output CS1bar;
	output CS2bar;
	output CS3bar;
  output wire sclk; 
	output wire sreset;
  output wire[1:0]sMODE;
  input  [7:0]data_in; 
  output reg[7:0]data_out;
  input  [1:0]CS; 
  input      [1:0]RW; 




  reg start_writting=0;


  integer RX_bit_count=0;
  reg [7:0]RX_temp_byte; 
  reg [7:0]RX_byte; 
  reg RX_done=0;  
//TX
reg [2:0]TX_bit_count; 
  reg [7:0]TX_temp_byte; 
//reg [7:0]Tx_byte;
  reg TX_done=0; 

  assign sclk= (MODE==0||MODE==3)?clk:~clk; 
  assign sreset=reset;
  assign sMODE=MODE;

  assign CS1bar=(CS==2'b01)?0:1; 
  assign CS2bar=(CS==2'b10)?0:1; 
  assign CS3bar=(CS==2'b11)?0:1;
  assign data_out=RX_done?RX_byte:8'bz;

  always @(posedge sclk,posedge reset)
    begin
      if (reset==1)
        begin
          RX_bit_count<=0;
		  RX_temp_byte<=0;
		  RX_done<=0;
        end // if (reset==1)
      else if (CS&&(RW==2'b10||RW==2'b11)) 
        begin
          if(RX_bit_count>=8&&RX_done==1'b0) 
            begin
              if (MISO!==1'bx)
                begin
                  RX_done<=1'b1;
                  RX_byte<=RX_temp_byte;
                  RX_temp_byte <= {7'b0000000,MISO};
                  RX_bit_count <= 1;
                end
            end
          
          else
            begin
              if (MISO!==1'bx)
                begin
                  RX_done<=0;
                  RX_temp_byte <= {RX_temp_byte[6:0],MISO};
                  RX_bit_count <= RX_bit_count+1;
                end
            end 
        end 
    end 

  always @(posedge sclk,posedge reset)
    begin
      start_writting=1;
      if (reset==1)
        begin
          TX_temp_byte<=data_in;
          TX_done<=0;
          TX_bit_count<=3'b000;
        end 
      else if (TX_done==1)
        begin
          TX_temp_byte<=data_in;
		  TX_done<=0;
		  TX_bit_count<=3'b000;
        end 
    end 
  always @ (negedge sclk)
    begin
      if (start_writting)
        begin
          if (CS&&(RW==2'b01||RW==2'b11)) 
            begin
              if (TX_bit_count==3'b111&&TX_done==0)
                begin
                  MOSI<=TX_temp_byte[0];
                  TX_done<=1;
                end
              else 
                begin
                  MOSI<=TX_temp_byte[0];//LSB : [data_in ->(MSB) TX_temp_byte (LSB)-> MOSI]
			      TX_temp_byte={1'b0,TX_temp_byte[7:1]};
			      TX_bit_count<=(TX_bit_count+1);
			      TX_done<=0;
                end
            end 
          else
            begin
              MOSI<=1'bx;
            end
        end
    end 
endmodule