module counter(clk,reset,count);
  input clk,reset;

  output reg [7:0] count;
  
  always@(posedge clk ) begin
    if(reset)    //Set Counter to Zero
      count <= 0;
    else
      count <= count - 1; //error should be count<=count+1
  end
  
endmodule

module input_capture(sig,clk,val,rst,rstVal,intFlag,rstIntFlag);
  input clk,rst,sig,rstVal,rstIntFlag;
  output reg [7:0] val;
  output reg intFlag;
  
  wire [7:0] tempCount;
  counter ct(.clk(clk),.count(tempCount),.reset(rst));
  initial intFlag=1'b0;
  
  always@(posedge sig or posedge rstVal or posedge rstIntFlag) begin
    if(rstVal)
      	val<= 1; //error should be zero
    else begin
    	//val<=tempCount;
      	intFlag<=1'b1;
    end
    //if(rstIntFlag) //error should be present
    //intFlag<=1'b0;//error should be present
    
  end
endmodule