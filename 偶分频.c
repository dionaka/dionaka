//法一  作为时钟被直接调用
module divider_six
(
    input wire sys_clk,
    input wire sys_rst_n,
    output reg clk_out
);

reg [1:0] cnt;
always@(posedge sys_clk or negedge sys_rst_n)
    if(sys_rst_n == 1'b0)
        cnt <= 2'd0;
    else if(cnt == 2'd2)
        cnt <= 2'd0;     
    else
        cnt <= cnt + 2'd1;

always@(posedge sys_clk or negedge sys_rst_n)
    if(sys_rst_n == 1'b0)
        clk_out <= 1'b0;
    else if(cnt == 2'd2)
        clk_out <= ~clk_out;     
    else
        clk_out <= clk_out;
                    
endmodule


//法二, 使用标志脉冲信号 在系统时钟控制下 通过判断clk_flagy高电平计时(推荐)
module divider_six
(
    input wire sys_clk,
    input wire sys_rst_n,
    output reg clk_flag
);

reg [2:0] cnt;
always@(posedge sys_clk or negedge sys_rst_n)
    if(sys_rst_n == 1'b0)
        cnt <= 3'd0;
    else if(cnt == 3'd5)
        cnt <= 3'd0;     
    else
        cnt <= cnt + 3'd1;

always@(posedge sys_clk or negedge sys_rst_n)
    if(sys_rst_n == 1'b0)
        clk_flag <= 1'b0;
    else if(cnt == 3'd4)
        clk_flag <= 1'b1;     
    else
        clk_flag <= 1'b0;
                    
endmodule