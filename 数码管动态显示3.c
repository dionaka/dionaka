//②动态显示驱动模块 整合bcd模块
module seg_dynamic
#(
    parameter CNT_MAX = 16'd49_999
)
(
    input wire sys_clk,
    input wire sys_rst_n,
    input wire [19:0] data,
    input wire [5:0] point,
    input wire sign,
    input wire seg_en,
    output reg [5:0] sel,
    output reg [7:0] seg
);

wire [3:0] b1; //个位
wire [3:0] b10; //十位
wire [3:0] b100; //百位
wire [3:0] b1000; //千位
wire [3:0] b1w; //万位
wire [3:0] b10w; //十万位
reg [23:0] data_reg; //数据处理寄存器 还是有用的因为有符号和小数点暂存
reg [15:0] cnt_1ms; //1ms计数器
reg flag_1ms; //1ms标志脉冲
reg [3:0] data_disp; //位显数据寄存器
reg dot_disp; //小数点寄存器
reg [2:0] cnt_sel; //位选 我感觉也没意义,直接sel左移加判断就可以了,此变量还要二进制转码
reg [5:0] sel_reg; //寄存器, 延迟1时钟周期得到的sel与seg同步

localparam NEG = 4'd10; //负号
localparam BLANK = 4'd11; //不使用

//data_reg
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        data_reg <= 24'b0;
    else if(b10w || point[5])
        data_reg <= {b10w, b1w, b1000, b100, b10, b1};
    else if(b1w || point[4])
        data_reg <= {sign ? NEG : BLANK, b1w, b1000, b100, b10, b1};
    else if(b1000 || point[3])
        data_reg <= {BLANK, sign ? NEG : BLANK, b1000, b100, b10, b1};
    else if(b100 || point[2])
        data_reg <= {BLANK, BLANK, sign ? NEG : BLANK, b100, b10, b1};      
    else if(b10 || point[1])
        data_reg <= {BLANK, BLANK, BLANK, sign ? NEG : BLANK, b10, b1}; 
    else
        data_reg <= {BLANK, BLANK, BLANK, BLANK, sign ? NEG : BLANK, b1};                

//cnt_1ms 50×10⁶×10⁻³=5×10⁴ (16位)
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        cnt_1ms <= 16'b0;
    else if(cnt_1ms == CNT_MAX)
        cnt_1ms <= 16'b0;
    else
        cnt_1ms <= cnt_1ms + 16'b1;        
        
//flag_1ms
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        flag_1ms <= 1'b0;
    else if(cnt_1ms == CNT_MAX - 1'b1)
        flag_1ms <= 1'b1;
    else
        flag_1ms <= 1'b0;

//cnt_sel
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        cnt_sel <= 3'd0;
    else if(cnt_sel == 3'd5 && flag_1ms == 1'b1)
        cnt_sel <= 3'd0;
    else if(flag_1ms == 1'b1)
        cnt_sel <= cnt_sel + 3'd1;

//sel_reg
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        sel_reg <= 6'b000_000;
    else if(!cnt_sel && flag_1ms)
        sel_reg <= 6'b000_001;
    else if(flag_1ms)
         sel_reg <= sel_reg << 1;

//data_disp
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        data_disp <= 4'd0;
    else if(seg_en && flag_1ms)
        case(cnt_sel)
            3'd0:    data_disp <= data_reg[3:0];
            3'd1:    data_disp <= data_reg[7:4];
            3'd2:    data_disp <= data_reg[11:8]; 
            3'd3:    data_disp <= data_reg[15:12];
            3'd4:    data_disp <= data_reg[19:16];
            3'd5:    data_disp <= data_reg[23:20];
            default  data_disp <= 4'd0;          
        endcase     
        
//dot_disp
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        dot_disp <= 1'b1;
    else if(flag_1ms)
        dot_disp <= ~point[cnt_sel];

//sel[5:0] <- sel_reg延迟1周期
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        sel <= 6'b000_000;
    else
        sel <= sel_reg;
           
//seg[7:0] 
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        seg <= 8'b1111_1111;
    else if(seg_en)
        case(data_disp)
            4'd0:    seg <= {dot_disp,7'b100_0000};
            4'd1:    seg <= {dot_disp,7'b111_1001};
            4'd2:    seg <= {dot_disp,7'b010_0100};
            4'd3:    seg <= {dot_disp,7'b011_0000};
            4'd4:    seg <= {dot_disp,7'b001_1001};
            4'd5:    seg <= {dot_disp,7'b001_0010};
            4'd6:    seg <= {dot_disp,7'b000_0010};
            4'd7:    seg <= {dot_disp,7'b111_1000};
            4'd8:    seg <= {dot_disp,7'b000_0000};
            4'd9:    seg <= {dot_disp,7'b001_0000};
            4'd10:   seg <= 8'b1011_1111;
            4'd11:   seg <= 8'b1111_1111;
            default: seg <= 8'b1100_0000;
        endcase    


                          
bcd_8421 bcd_8421_inst
(
    .sys_clk(sys_clk),
    .sys_rst_n(sys_rst_n),
    .data(data),
    .b1(b1),
    .b10(b10),
    .b100(b100),
    .b1000(b1000),
    .b1w(b1w),
    .b10w(b10w)
);
endmodule