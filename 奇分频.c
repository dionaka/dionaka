//占空比为50%的五分频
module divider_five
(
    input wire sys_clk,
    input wire sys_rst_n,
    output wire clk_out
);

reg [2:0] cnt;
reg clk1;
reg clk2;

always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        cnt <= 3'd0;
    else if(cnt == 3'd4)    
        cnt <= 3'd0;
    else
        cnt <= cnt + 3'd1;    

always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        clk1 <= 1'b0;
    else if(cnt == 3'd2)    
        clk1 <= 1'b1;
    else if(cnt == 3'd4)
        clk1 <= 1'b0;
        
always@(negedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        clk2 <= 1'b0;
    else if(cnt == 3'd2)    
        clk2 <= 1'b1;
    else if(cnt == 3'd4)
        clk2 <= 1'b0;

//阻塞赋值 组合逻辑电路 防止延迟1拍
assign clk_out = (clk1 | clk2);
         
endmodule


//使用标志脉冲方法同偶分屏