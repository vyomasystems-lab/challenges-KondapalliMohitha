module slave (MODE, data_in, reset, clk, MOSI, MISO, CS, data_out);
  
  input[1:0] MODE;
  input [7:0] data_in;
  input reset;
  input clk;
  input MOSI;
  output reg MISO;
  input CS;
  output reg [7:0] data_out;
  reg entered=0;

  reg [7:0] R_data;
  reg [7:0] T_data; 
  reg done;
  integer count=0;
  reg is_read=0;
  always@(posedge clk)
    begin
      if((reset||!is_read))
        begin
          T_data=data_in;
          count=0;
          entered=0;
          done=0;
        end
      if(!CS)
        begin
          if(entered)
            begin
              R_data={MOSI,R_data[7:1]};
              count=count+1;  
              if(count==8)
                begin 
                  count=0;
                  entered=0; 
                  data_out=R_data;
                  is_read=0;
                  done=1; 
                end
            end 
        end
    end
  always@(negedge clk)
    begin
      if((reset||!is_read))
        begin
          T_data=data_in;
          count=0;
          entered=0;
          done=0;
        end
      if(!CS)
        begin 
          if(!done)
            begin       
              MISO=T_data[7];
              T_data={T_data[6:0],1'bx};   
              entered=1;
              is_read=1; 
            end
          end
    end

endmodule