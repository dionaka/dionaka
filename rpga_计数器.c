//法一
module counter
#(
    parameter CNT_MAX = 25'd24_999_999
)
(
    input wire sys_clk,
    input wire sys_rst_n,
    output reg led_out
);

reg [24:0] cnt;
always@(posedge sys_clk or negedge sys_rst_n)
    if(sys_rst_n == 1'b0)    //更常用if(!sys_rst_n) 以下同理
        cnt <= 25'd0;
    else if(cnt == CNT_MAX)    
        cnt <= 25'd0;
    else
        cnt <= cnt + 1;    

always@(posedge sys_clk or negedge sys_rst_n)
    if(sys_rst_n == 1'b0)
        led_out <= 1'b0;
    else if(cnt == CNT_MAX)    
        led_out <= ~led_out;
    else
        led_out <= led_out;    //这个分支可以省略, reg类型未赋值会保持原值, 以下同理 
                
endmodule


//法二, 标志脉冲信号
module counter
#(
    parameter CNT_MAX = 25'd24_999_999
)
(
    input wire sys_clk,
    input wire sys_rst_n,
    output reg led_out
);

reg [24:0] cnt;
reg cnt_flag;

always@(posedge sys_clk or negedge sys_rst_n)
    if(sys_rst_n == 1'b0)
        cnt <= 25'd0;
    else if(cnt == CNT_MAX)    
        cnt <= 25'd0;
    else
        cnt <= cnt + 1;    
        
always@(posedge sys_clk or negedge sys_rst_n)
    if(sys_rst_n == 1'b0)
        cnt_flag <= 1'b0;
    else if(cnt == (CNT_MAX - 25'd1))    
        cnt_flag <= 1'b1;
    else
        cnt_flag <= 1'b0;
            
always@(posedge sys_clk or negedge sys_rst_n)
    if(sys_rst_n == 1'b0)
        led_out <= 1'b0;
    else if(cnt_flag == 1'b1)    
        led_out <= ~led_out;
    else
        led_out <= led_out;
                
endmodule