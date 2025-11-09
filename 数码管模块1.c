module seg_static
#(
    parameter CNT_MAX = 25'd24_999_999
)
(
    input wire sys_clk,
    input wire sys_rst_n,
    output reg [5:0] sel, //000000-111111
    output reg [7:0] seg //八段数码管
);

reg [24:0] cnt; //0-24999999
reg [3:0] data; //0-F(15)
reg cnt_flag; //标志脉冲

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
    /*    
    else if(cnt == (CNT_MAX - 25'd1))
        cnt_flag <= 1'b1;
    else
        cnt_flag <= 1'b0;    
    */
    //纯时序逻辑  路径简单  毛刺生成风险低☆
    else
        cnt_flag <= (cnt == (CNT_MAX - 25'd1));

always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        data <= 4'd0;
    else if((data == 4'd15) && (cnt_flag == 1'b1))
        data <= 4'd0;
    else if(cnt_flag == 1'b1)
        data <= data + 4'd1;
        
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        sel <= 6'b000_000;
    else
        sel <= 6'b111_111;
        
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        seg <= 8'h00; //全显示
    else
        //会延迟一周期
        case(data)
            4'd0:    seg <= 8'hc0;
            4'd1:    seg <= 8'hf9;
            4'd2:    seg <= 8'ha4;
            4'd3:    seg <= 8'hb0;
            4'd4:    seg <= 8'h99;
            4'd5:    seg <= 8'h92;
            4'd6:    seg <= 8'h82;
            4'd7:    seg <= 8'hf8;
            4'd8:    seg <= 8'h80;
            4'd9:    seg <= 8'h90;
            4'd10:    seg <= 8'h88;
            4'd11:    seg <= 8'h83;
            4'd12:    seg <= 8'hc6;
            4'd13:    seg <= 8'ha1;
            4'd14:    seg <= 8'h86;
            4'd15:    seg <= 8'h8e;
            default:    seg <= 8'h00;
        endcase    
                                        
endmodule