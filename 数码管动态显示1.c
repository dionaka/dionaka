//①数据生成模块
module data_gen
#(
    parameter CNT_MAX = 23'd4_999_999,
    parameter DATA_MAX = 20'd999_999
)
(
    input wire sys_clk,
    input wire sys_rst_n,
    
    output reg [19:0] data, //数码管显示0 ∽ 999999 → 2^19 ∽ 2^20 = 20'b
    output wire [5:0] point, //小数点
    output wire sign, //符号位 设低电平为正数
    output reg seg_en //使能信号 设高电平有效
);

//0.1s时钟计数器 → 50M/10 = 5M = 5_000_000 = 2^22 ∽ 2^23 = 23'b
reg [22:0] cnt_100ms;
//标志脉冲 便于记录0.1s周期次数 简洁清晰 
reg cnt_flag;

//0.1s时钟计数器赋值
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        cnt_100ms <= 23'd0;
    else if(cnt_100ms == CNT_MAX)
        cnt_100ms <= 23'd0;
    else
        cnt_100ms <= cnt_100ms + 23'd1;        
    
//标志脉冲赋值
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        cnt_flag <= 1'b0;
    else if(cnt_100ms == CNT_MAX - 23'd1)
        cnt_flag <= 1'b1;
    else
        cnt_flag <= 1'b0;          

//输出data赋值
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        data <= 20'd0;
    else if(cnt_flag == 1'b1 && data == DATA_MAX)
        data <= 20'd0;    
    else if(cnt_flag == 1'b1)
        data <= data + 20'd1;
        
//输出point赋值
assign point = 6'b000_000;

//输出sign赋值
assign sign = 1'b0;

//输出seg_en赋值
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        seg_en <= 1'b0;
    else
        seg_en <= 1'b1;      
        
endmodule