moduel hc595_ctrl
(
    input wire sys_clk,
    input wire sys_rst_n,
    input wire [5:0] sel, //位选信号
    input wire [7:0] seg, //段选信号
    output reg ds, //串行数据输入
    output reg shcp,  //移位寄存器时钟 上升沿到来ds数据传入
    output reg stcp,  //存储寄存器时钟
    output wire oe  //输出使能 低电平有效
);

wire [13:0] data; //组合seg与sel
reg [1:0] cnt; //四分频 hc595的时钟
reg [3:0] cnt_bit; //比特计数器 仅作列表索引

assign data = {seg[0],seg[1],seg[2],seg[3],seg[4],seg[5],seg[6],seg[7],sel};

//四分频
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        cnt <= 2'd0;
    else if(cnt == 2'd3)
        cnt <= 2'd0;
    else
        cnt <= cnt + 2'd1;

//比特计数器
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        cnt_bit <= 4'd0; 
    else if((cnt_bit == 4'd13) && (cnt == 2'd3))
        cnt_bit <= 4'd0;
    else if(cnt == 2'd3)
        cnt_bit <= cnt_bit + 4'd1;

//串行输入
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        ds <= 1'b0;
    else if(cnt == 2'd0)
        ds <= data[cnt_bit];

//移位时钟
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        shcp <= 1'b0;
    else if(cnt == 2'd2)
        shcp <= 1'b1;     
    else if(cnt == 2'd0)
        shcp <= 1'b0;

//存储寄存器时钟
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        stcp <= 1'b0;
    else if((cnt == 2'd0) && (cnt_bit ==  4'd0))
        stcp <= 1'b1;
    else if((cnt == 2'd2) && (cnt_bit ==  4'd0))
        stcp <= 1'b0;  
        
//输出使能信号               
assign oe = 1'b0;
                                                             
endmodule