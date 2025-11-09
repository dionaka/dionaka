module sample_fsm
(
    input wire sys_clk,
    input wire sys_rst_n,
    input wire pi_coin,
    output reg po_cola
);

//状态
parameter ZERO = 3'b001;
parameter ONE = 3'b010;
parameter TWO = 3'b100;
reg [2:0] state;

always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        state <= ZERO;
    else 
        case(state)
            ZERO:   if(pi_coin == 1'b1)
                        state <= ONE;
                    else    
                        state <= ZERO;
            ONE:    if(pi_coin == 1'b1)
                        state <= TWO;
                    else    
                        state <= ONE;    
            TWO:    if(pi_coin == 1'b1)
                        state <= ZERO;
                    else    
                        state <= TWO;
            default: state <= ZERO; // 确保任何异常情况下都能回到初始状态
        endcase

//时序逻辑电路延迟1周期 可选择组合逻辑         
always@(posedge sys_clk or negedge sys_rst_n)
    if(!sys_rst_n)
        po_cola <= 1'b0;
    else if((state == TWO) && (pi_coin == 1'b1))
        po_cola <= 1'b1;
    else
        po_cola <= 1'b0;
                                    
endmodule