module complex_fsm
(
    input wire sys_clk,
    input wire sys_rst_n,
    input wire pi_coin_half,
    input wire pi_coin_one,
    output reg po_cola,
    output reg po_coin
);

parameter ZERO = 5'b00001;
parameter HALF = 5'b00010;
parameter ONE = 5'b00100;
parameter ONEHALF = 5'b01000;
parameter TWO = 5'b10000;
reg [4:0] state;
//计数器  组合逻辑  00 01 10分别代表不投币、投五毛、投一元，我觉得也不是非得要这一项, 视频里面他这个只做一个用来比较的中间变量，而且他还没有考虑同时投的情况，我感觉这玩意儿完全多余啊
wire [1:0] pi_coin;
assign pi_coin = {pi_coin_one,pi_coin_half};

always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        state <= ZERO;
    else
        case(state)
            ZERO:    if(pi_coin == 2'b01)
                         state <= HALF;
                     else if(pi_coin == 2'b10)
                         state <= ONE;     
                     else    //else不能省略会出现锁存器
                         state <= ZERO;    
            HALF:    if(pi_coin == 2'b01)
                         state <= ONE;
                     else if(pi_coin == 2'b10)
                         state <= ONEHALF;     
                     else
                         state <= HALF; 
            ONE:     if(pi_coin == 2'b01)
                         state <= ONEHALF;
                     else if(pi_coin == 2'b10)
                         state <= TWO;     
                     else
                         state <= ONE;         
            ONEHALF: if(pi_coin == 2'b01)
                         state <= TWO;
                     else if(pi_coin == 2'b10)
                         state <= ZERO;     
                     else
                         state <= ONEHALF;
            TWO:     if((pi_coin == 2'b01) || (pi_coin == 2'b10))
                         state <= ZERO;
                     else
                         state <= TWO;
            default: state <= ZERO; 
        endcase  

always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        po_cola <= 1'b0;
    else if((state == ONEHALF && pi_coin == 2'b10) || 
            (state == TWO && pi_coin == 2'b01) || 
            (state == TWO && pi_coin == 2'b10))
        po_cola <= 1'b1;
    else
        po_cola <= 1'b0;

always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        po_coin <= 1'b0;
    else if((state == TWO) && (pi_coin == 2'b10))
        po_coin <= 1'b1;
    else
        po_coin <= 1'b0;
        
                                                                                           
endmodule