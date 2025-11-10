//②动态显示驱动模块 内置二进制-8421转码
/*
module seg_dynamic
(

);
*/
module bcd_8421
(
    input wire sys_clk,
    input wire sys_rst_n,
    input wire [19:0] data,
    //生成8421码
    output reg [3:0] b1,
    output reg [3:0] b10,
    output reg [3:0] b100,
    output reg [3:0] b1000,
    output reg [3:0] b1w,
    output reg [3:0] b10w
);

//移位计数器 0(准备) + 1∽20(移20次) + 1(结束) = 0∽21共22周期
reg [4:0] cnt_shift; 

//中间数据 20位二进制码 + 4×6位BCD = 44位
reg [43:0] data_shift;

//移位标志信号 二分频
reg shift_flag;


//移位计数器cnt_shift赋值
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        cnt_shift <= 5'd0;
    else if(shift_flag == 1'b1 && cnt_shift == 5'd21)
        cnt_shift <= 5'd0;
    else if(shift_flag == 1'b1)
        cnt_shift <= cnt_shift + 5'd1;
        
//中间数据data_shift赋值
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        data_shift <= 44'd0;
    else if(shift_flag == 1'b0 && cnt_shift == 5'd0)
        data_shift <= {24'd0, data};  
    else if(shift_flag == 1'b0 && cnt_shift <= 5'd20)
        begin
            data_shift[23:20] <= ((data_shift[23:20] > 4) ? (data_shift[23:20] + 3) : data_shift[23:20]);
            data_shift[27:24] <= ((data_shift[27:24] > 4) ? (data_shift[27:24] + 3) : data_shift[27:24]); 
            data_shift[31:28] <= ((data_shift[31:28] > 4) ? (data_shift[31:28] + 3) : data_shift[31:28]);
            data_shift[35:32] <= ((data_shift[35:32] > 4) ? (data_shift[35:32] + 3) : data_shift[35:32]);        
            data_shift[39:36] <= ((data_shift[39:36] > 4) ? (data_shift[39:36] + 3) : data_shift[39:36]);
            data_shift[43:40] <= ((data_shift[43:40] > 4) ? (data_shift[43:40] + 3) : data_shift[43:40]);   
        end
    else if(shift_flag == 1'b1 && cnt_shift <= 5'd20)
        data_shift <= data_shift << 1; 
        
//移位标志信号shift_flag赋值
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        shift_flag <= 1'b0;
    else
        shift_flag <= ~shift_flag;
        
//输出6段8421BCD码            
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        begin
            b1 <= 4'd0;
            b10 <= 4'd0;
            b100 <= 4'd0;
            b1000 <= 4'd0;
            b1w <= 4'd0;
            b10w <= 4'd0;
        end
    else if(cnt_shift == 5'd21)
        begin
            b1 <= data_shift[23:20];
            b10 <= data_shift[27:24];
            b100 <= data_shift[31:28];
            b1000 <= data_shift[35:32];
            b1w <= data_shift[39:36];
            b10w <= data_shift[43:40]; 
        end              
         
endmodule