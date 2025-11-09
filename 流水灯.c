module water_led
#(
    parameter CNT_MAX = 25'd24_999_999
)
(
    input wire sys_clk,
    input wire sys_rst_n,
    output reg [3:0] led_out
);

reg [24:0] cnt;
//标志脉冲
reg cnt_flag;

always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        cnt <= 25'd0;
    else if(cnt == CNT_MAX)    
        cnt <= 25'd0;
    else 
        cnt <= cnt + 25'd1;
        
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        cnt_flag <= 1'b0;
    else if(cnt == (CNT_MAX - 1))
        cnt_flag <= 1'b1;
    else 
        cnt_flag <= 1'b0;

always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        led_out <= 4'b1110;
    else if(cnt_flag)
        begin
            if(led_out == 4'b0111)
                led_out <= 4'b1110;
            else
                led_out <= {led_out[2:0], 1'b1};   
        end
       
        
endmodule